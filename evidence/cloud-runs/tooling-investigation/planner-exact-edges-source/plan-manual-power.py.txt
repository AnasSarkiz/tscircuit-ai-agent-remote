"""Plan wide distribution with separately recorded short native pad escapes.

Each neck remains a visible source trace, never hidden in a fabricated cache.
Electrical/current and native copper validation are required before acceptance.
"""
import argparse
import json
import math
import runpy
from pathlib import Path

from shapely.geometry import LineString, Point

Planner = runpy.run_path(str(Path(__file__).with_name("plan-manual-signals.py")))["ManualSignalPlanner"]


def path_record(planner, specification):
    start = specification["start"]
    component = planner.components[start["pcb_component_id"]]
    rotation = math.radians(-component["rotation"])
    positions = specification["positions"]
    layers = specification["layers"]
    local = []
    limit = len(positions) if specification["to"].startswith("net.") else len(positions) - 1
    for index, (x, y) in enumerate(positions[1:limit], 1):
        dx, dy = x - component["display_offset_x"], y - component["display_offset_y"]
        waypoint = {"x": round(dx * math.cos(rotation) - dy * math.sin(rotation), 6),
                    "y": round(dx * math.sin(rotation) + dy * math.cos(rotation), 6)}
        local.append(waypoint)
        if index < len(layers) - 1 and layers[index] != layers[index + 1]:
            local.append({**waypoint, "via": True, "fromLayer": layers[index], "toLayer": layers[index + 1]})
            local.append(dict(waypoint))
    net_root = specification["net_root"]
    width = specification["width"]
    for index, (first, second) in enumerate(zip(positions, positions[1:])):
        planner.copper.append((net_root, layers[index + 1], LineString([first, second]).buffer(width / 2)))
    for via_position in specification.get("vias", []):
        planner.holes.append(Point(via_position).buffer(0.15))
        for layer in ("top", "inner1", "inner2", "bottom"):
            planner.copper.append((net_root, layer, Point(via_position).buffer(0.35)))
    return {"net": specification["net"], "from": planner.port_name(start), "to": specification["to"],
            "width": width, "pcbPath": local, "global_path_mm": positions, "segment_layers": layers,
            "classification": specification["classification"]}


def plan_distribution(planner, net):
    root = planner.root(net["source_net_id"])
    ports = [port for port in planner.ports.values() if planner.root(port["source_port_id"]) == root
             and planner.source_ports[port['source_port_id']].get('source_component_id') in planner.source_components
             and not planner.port_name(port).startswith((".J3 >", ".J7 >"))]
    ports.sort(key=lambda port: (not planner.port_name(port).startswith(".C"), planner.port_name(port)))
    if len(ports) < 2:
        return [], []
    width = net["trace_width"]
    obstacles = planner.obstacles(root, "top", width)
    def wide_exit_score(port):
        origin = (port["x"], port["y"])
        if Point(origin).intersects(obstacles):
            return -1
        return sum(not LineString([origin, (origin[0] + distance * dx, origin[1] + distance * dy)]).intersects(obstacles)
                   for distance in (0.6, 0.9, 1.2, 1.5)
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    ports.sort(key=wide_exit_score, reverse=True)
    foundation = ports.pop(0)
    joined, paths, unresolved = [foundation], [], []
    width = net["trace_width"]
    while ports:
        _, start, end = min(((math.dist((a["x"], a["y"]), (b["x"], b["y"])), a, b)
                            for a in joined for b in ports), key=lambda edge: edge[0])
        ports.remove(end)
        first, last = (start["x"], start["y"]), (end["x"], end["y"])
        wide_obstacles = planner.obstacles(root, "top", width)
        narrow_width = min(width, 0.275)
        narrow_obstacles = planner.obstacles(root, "top", narrow_width)
        destinations = [(last, None)]
        if Point(last).intersects(wide_obstacles):
            destinations = []
            for distance in (0.6, 0.8, 1.0, 1.2):
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    target = last[0] + distance * dx, last[1] + distance * dy
                    if not Point(target).intersects(wide_obstacles) and not LineString([last, target]).intersects(narrow_obstacles):
                        destinations.append((target, [last, target]))
        accepted = False
        for target, neck in destinations:
            route = planner.grid_route((first, target, wide_obstacles))
            layers, vias = (["top"] * len(route), []) if route else ([], [])
            if route is None:
                result = planner.multilayer_route((first, target), (root, width))
                if result is None:
                    continue
                route, layers, vias = result
            paths.append(path_record(planner, {"start": start,
                "to": f"net.{net['name']}" if neck else planner.port_name(end), "width": width,
                "net": net["name"], "net_root": root, "positions": route, "layers": layers, "vias": vias,
                "classification": "manual native power distribution"}))
            if neck:
                paths.append(path_record(planner, {"start": end, "to": f"net.{net['name']}",
                    "width": narrow_width, "net": net["name"], "net_root": root,
                    "positions": neck, "layers": ["top", "top"], "classification": "manual short pad escape; current qualification pending"}))
            if neck is None:
                joined.append(end)
            accepted = True
            break
        if not accepted:
            unresolved.append({"net": net["name"], "port": planner.port_name(end),
                               "reason": "No qualified wide path with a pad escape at most 1.2 mm from pad centre"})
    return paths, unresolved


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("circuit_json")
    parser.add_argument("output_json")
    parser.add_argument("nets", nargs="+")
    parser.add_argument('--reserve-proposals',action='append',default=[])
    args = parser.parse_args()
    circuit = json.loads(Path(args.circuit_json).read_text())
    planner = Planner(circuit)
    for path in args.reserve_proposals:
        planner.reserve_proposals(json.loads(Path(path).read_text()))
    paths, unresolved = [], []
    for name in args.nets:
        net = next(r for r in circuit if r["type"] == "source_net" and r["name"] == name)
        proposed, failures = plan_distribution(planner, net)
        paths.extend(proposed)
        unresolved.extend(failures)
        print(json.dumps({"net": name, "paths": len(proposed), "unresolved": failures}), flush=True)
        Path(args.output_json).write_text(json.dumps({"classification": "manual power proposals, not solver caches",
            "source_circuit_json": args.circuit_json, "paths": paths, "unresolved": unresolved}, indent=2) + "\n")


if __name__ == "__main__":
    main()
