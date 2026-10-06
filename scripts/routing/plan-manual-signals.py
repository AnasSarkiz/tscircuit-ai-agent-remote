"""Plan explicit native traces against preserved copper; never create autorouter caches.

Exact supported pad and drill contours retain the actual clearances. A plan is not accepted until native
replay and independent copper/drill/plane checks succeed.
"""
import argparse
import heapq
import json
import math
import runpy
from pathlib import Path

import numpy as np
from shapely import contains_xy
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

geometry_helpers = runpy.run_path(str(Path(__file__).with_name('audit-copper.py')))


def point(record):
    return record["x"], record["y"]


def outline_shape(record):
    return geometry_helpers['pad_contour'](record)


def connected_grid_labels(blocked):
    """Label four-connected free cells with a scanline union, without A*."""
    labels = np.zeros(blocked.shape, dtype=np.int32)
    parents = [0]

    def root(identifier):
        while parents[identifier] != identifier:
            parents[identifier] = parents[parents[identifier]]
            identifier = parents[identifier]
        return identifier

    previous = []
    for y, row in enumerate(blocked):
        changes = np.diff(np.pad((~row).astype(np.int8), (1, 1)))
        starts, ends = np.flatnonzero(changes == 1), np.flatnonzero(changes == -1)
        current, cursor = [], 0
        for start, end in zip(starts, ends):
            identifier = len(parents)
            parents.append(identifier)
            labels[y, start:end] = identifier
            while cursor < len(previous) and previous[cursor][1] <= start:
                cursor += 1
            index = cursor
            while index < len(previous) and previous[index][0] < end:
                parents[root(identifier)] = root(previous[index][2])
                index += 1
            current.append((start, end, identifier))
        previous = current
    return np.take(np.array([root(identifier) for identifier in range(len(parents))]), labels)


class ManualSignalPlanner:
    def __init__(self, circuit, planning_changes=None):
        planning_changes = planning_changes or {}
        retired_feature_ids = set(planning_changes.get('retired_feature_ids', ()))
        relocated_trace_layers = planning_changes.get('relocated_trace_layers', {})
        self.circuit = circuit
        self.parent = {}
        for record in circuit:
            identifiers = []
            if record["type"] == "source_trace":
                identifiers = record.get("connected_source_port_ids", []) + record.get("connected_source_net_ids", [])
            elif record["type"] == "source_component_internal_connection":
                identifiers = record["source_port_ids"]
            for identifier in identifiers[1:]:
                self.parent[self.root(identifier)] = self.root(identifiers[0])
        self.source_traces = {r["source_trace_id"]: r for r in circuit if r["type"] == "source_trace"}
        self.source_ports = {r["source_port_id"]: r for r in circuit if r["type"] == "source_port"}
        self.source_components = {r["source_component_id"]: r for r in circuit if r["type"] == "source_component"}
        self.source_vias = {r["source_manually_placed_via_id"]: r for r in circuit if r["type"] == "source_manually_placed_via"}
        for source_port in self.source_ports.values():
            via_source = self.source_vias.get(source_port.get("source_component_id"))
            if via_source and via_source.get("source_net_id"):
                self.parent[self.root(source_port["source_port_id"])] = self.root(via_source["source_net_id"])
        self.pcb_traces = {r["pcb_trace_id"]: r for r in circuit if r["type"] == "pcb_trace"}
        self.reflow_ground_roots = {self.root(r["source_net_id"]) for r in circuit if r["type"] == "source_net" and r["name"] == "GND"}
        self.components = {r["pcb_component_id"]: r for r in circuit if r["type"] == "pcb_component"}
        self.ports = {r["pcb_port_id"]: r for r in circuit if r["type"] == "pcb_port"}
        copper_audit = runpy.run_path(str(Path(__file__).with_name('audit-copper.py')))['audit'](circuit)
        self.physical_parent = {identifier: identifier for identifier in self.ports}
        representatives = {}
        for identifier, groups in copper_audit['physical_port_groups'].items():
            if len(groups) == 1:
                representative = representatives.setdefault(groups[0], identifier)
                self.physical_parent[identifier] = representative
        self.pads = [(r, outline_shape(r)) for r in circuit if r["type"] in ("pcb_smtpad", "pcb_plated_hole")]
        self.holes = []
        self.plated_hole_roots = {}
        for record in circuit:
            if record.get('pcb_via_id') in retired_feature_ids:
                continue
            if record["type"] in ("pcb_hole", "pcb_via"):
                hole = geometry_helpers['drill_contour'](record)
                self.holes.append(hole)
                if record['type'] == 'pcb_via':
                    self.plated_hole_roots[hole.wkb] = self.via_root(record)
            elif record["type"] == "pcb_plated_hole":
                hole = geometry_helpers['drill_contour'](record)
                self.holes.append(hole)
                port = self.ports.get(record.get('pcb_port_id'))
                if port:
                    self.plated_hole_roots[hole.wkb] = self.root(port['source_port_id'])
        # The pinned native trace checker evaluates keepouts as rectangles.
        # Reserve their envelopes during planning so actual contours and the
        # required native check both pass; the audit still measures true shapes.
        self.keepouts = [(r, outline_shape(r).envelope) for r in circuit if r["type"] == "pcb_keepout"]
        board = next(r for r in circuit if r["type"] == "pcb_board")
        self.board = Polygon([point(p) for p in board["outline"]])
        self.copper = []
        self.off_top_nets = set()
        self.copper_clearance = 0.21
        self.via_copper_clearance = 0.21
        for record in circuit:
            if record["type"] == "pcb_trace":
                source = self.source_traces[record["source_trace_id"]]
                net_root = self.root((source.get("connected_source_port_ids", []) + source.get("connected_source_net_ids", []))[0])
                for start, end in zip(record["route"], record["route"][1:]):
                    if start["route_type"] == end["route_type"] == "wire":
                        radius = (max(start["width"], end["width"]) if record.get("route_thickness_mode") == "interpolated" else start["width"]) / 2
                        planned_layer = relocated_trace_layers.get(record['pcb_trace_id'], {}).get(start['layer'], start['layer'])
                        if planned_layer is not None:
                            self.copper.append((net_root, planned_layer, LineString([point(start), point(end)]).buffer(radius)))
            elif record["type"] == "pcb_via":
                if record['pcb_via_id'] in retired_feature_ids:
                    continue
                net_root = self.via_root(record)
                for layer in record["layers"]:
                    self.copper.append((net_root, layer, Point(point(record)).buffer(record["outer_diameter"] / 2)))
            elif record["type"] == "pcb_copper_pour":
                # Retire explicitly selected authored regions during replacement
                # planning only. The original native scene remains immutable.
                if record['pcb_copper_pour_id'] in retired_feature_ids:
                    continue
                net_root = self.root(record["source_net_id"])
                # This board regenerates its GND pours around every new route.
                # Power regions must remain obstacles to protect their width.
                if net_root in self.reflow_ground_roots:
                    continue
                if record["shape"] != "brep":
                    raise ValueError(f"Unsupported copper pour: {record['shape']}")
                brep = record["brep_shape"]
                shape = Polygon([point(p) for p in brep["outer_ring"]["vertices"]],
                                [[point(p) for p in ring["vertices"]] for ring in brep["inner_rings"]])
                if not shape.is_valid:
                    raise ValueError("Invalid native power region")
                self.copper.append((net_root, record["layer"], shape))
        self.set_grid(0.1)

    def set_grid(self, step):
        if step not in (0.05, 0.1):
            raise ValueError('Supported routing grids are 0.05 mm and 0.1 mm')
        self.grid_step = step
        self.x_coordinates = np.arange(-24.5, 24.50001, self.grid_step)
        self.y_coordinates = np.arange(-32.0, 32.00001, self.grid_step)
        self.grid_x, self.grid_y = np.meshgrid(self.x_coordinates, self.y_coordinates)
        self.grid_cache = []
        self.layer_component_cache = []
        self.grid_edge_cache = []

    def grid_data(self, obstacles):
        for cached_obstacles, blocked, labels in self.grid_cache:
            if cached_obstacles is obstacles or cached_obstacles.equals_exact(obstacles, 0):
                return blocked, labels
        blocked = contains_xy(obstacles, self.grid_x, self.grid_y)
        labels = connected_grid_labels(blocked)
        self.grid_cache.append((obstacles, blocked, labels))
        if len(self.grid_cache) > 6:
            self.grid_cache.pop(0)
        return blocked, labels

    def set_copper_reserve(self, reserve):
        if reserve not in (0.0001, 0.01, 0.07):
            raise ValueError('Supported extra copper planning reserves are 0.0001 mm, 0.01 mm and 0.07 mm')
        # The board requirement remains 0.20 mm. A 0.01 mm extra reserve
        # blocks the actual 0.2021 mm USB pad-exit gap; native/audit gates
        # still independently enforce the unchanged 0.20 mm requirement.
        # The 0.07 mm reserve also protects existing regions from the native
        # 0.26 mm pour cutout margin, with 0.01 mm planning headroom.
        self.copper_clearance = 0.2 + reserve

    def grid_edge_clear(self, first, last, obstacles, blocked):
        context = next((entry for entry in self.grid_edge_cache if entry[0] is blocked), None)
        if context is None:
            padded = np.pad(blocked, 1)
            near = np.zeros_like(blocked)
            for dy in range(3):
                for dx in range(3):
                    near |= padded[dy:dy+blocked.shape[0], dx:dx+blocked.shape[1]]
            context = (blocked, near, {})
            self.grid_edge_cache.append(context)
            if len(self.grid_edge_cache) > 6:
                self.grid_edge_cache.pop(0)
        _, near, checked = context
        if not near[first] and not near[last]:
            return True
        key = tuple(sorted((first, last)))
        if key not in checked:
            positions = [(float(self.x_coordinates[node[1]]), float(self.y_coordinates[node[0]])) for node in key]
            checked[key] = not LineString(positions).intersects(obstacles)
        return checked[key]

    def root(self, identifier):
        self.parent.setdefault(identifier, identifier)
        if self.parent[identifier] != identifier:
            self.parent[identifier] = self.root(self.parent[identifier])
        return self.parent[identifier]

    def port_name(self, port):
        source_port = self.source_ports[port["source_port_id"]]
        name = self.source_components[source_port["source_component_id"]]["name"]
        port_selector = f"pin{source_port['pin_number']}" if "pin_number" in source_port else source_port["name"]
        return f".{name} > .{port_selector}"

    def via_root(self, via):
        if via.get("pcb_trace_id"):
            source = self.source_traces[self.pcb_traces[via["pcb_trace_id"]]["source_trace_id"]]
        elif via.get("source_trace_id"):
            source = self.source_traces[via["source_trace_id"]]
        elif via.get("source_net_id"):
            return self.root(via["source_net_id"])
        else:
            raise ValueError(f"Unassigned native via: {via}")
        return self.root((source.get("connected_source_port_ids", []) + source.get("connected_source_net_ids", []))[0])

    def physical_root(self, identifier):
        if self.physical_parent[identifier] != identifier:
            self.physical_parent[identifier] = self.physical_root(self.physical_parent[identifier])
        return self.physical_parent[identifier]

    def reserve_proposals(self, proposals):
        nets = {r['name']: r for r in self.circuit if r['type'] == 'source_net'}
        selectors = {self.port_name(port): port for port in self.ports.values()
                     if self.source_ports[port['source_port_id']].get('source_component_id') in self.source_components}
        for path in proposals.get('paths', []):
            root = self.root(nets[path['net']]['source_net_id'])
            positions, layers = path['global_path_mm'], path['segment_layers']
            start = selectors[path['from']]
            if self.root(start['source_port_id']) != root or math.dist(point(start), positions[0]) > 1e-5 or layers[0] != 'top':
                raise ValueError('Proposed path does not start on its real assigned top-side terminal')
            end = selectors.get(path['to'])
            if end and (self.root(end['source_port_id']) != root or math.dist(point(end), positions[-1]) > 1e-5 or layers[-1] != 'top'):
                raise ValueError('Proposed path does not end on its real assigned top-side terminal')
            via_positions = []
            for index, (first, last) in enumerate(zip(positions, positions[1:])):
                self.copper.append((root, layers[index+1], LineString([first,last]).buffer(path['width']/2)))
                if index and layers[index] != layers[index+1]:
                    via_positions.append(first)
            if path['pcbPath'] and path['pcbPath'][-1].get('via'):
                via_positions.append(positions[-1])
            for position in via_positions:
                hole = Point(position).buffer(.15)
                self.holes.append(hole)
                self.plated_hole_roots[hole.wkb] = root
                for layer in ('top','inner1','inner2','bottom'):
                    self.copper.append((root,layer,Point(position).buffer(.35)))
            if end:
                # Planning-only connectivity follows verified terminal geometry,
                # avoiding duplicate reroutes when reserving a prior proposal.
                # It never substitutes for the subsequent native copper audit.
                self.physical_parent[self.physical_root(start['pcb_port_id'])] = self.physical_root(end['pcb_port_id'])
        for via in proposals.get('vias', []):
            root = self.root(nets[via['net']]['source_net_id'])
            position = (via['x'],via['y'])
            hole = Point(position).buffer(via['hole_mm']/2)
            self.holes.append(hole)
            self.plated_hole_roots[hole.wkb] = root
            for layer in ('top','inner1','inner2','bottom'):
                self.copper.append((root,layer,Point(position).buffer(via['outer_mm']/2)))

    def obstacles(self, net_root, layer, width):
        radius = width / 2
        shapes = []
        for record, shape in self.pads:
            if layer not in record.get("layers", [record.get("layer")]):
                continue
            port = self.ports.get(record.get("pcb_port_id"))
            if port and self.root(port["source_port_id"]) == net_root:
                continue
            shapes.append(shape.buffer(self.copper_clearance + radius))
        shapes.extend(shape.buffer(self.copper_clearance + radius) for root, copper_layer, shape in self.copper if root != net_root and copper_layer == layer)
        # A trace may join an intended same-net plated terminal. Rebuild the
        # union from individual holes so no foreign obstacle is erased.
        shapes.extend(shape.buffer(0.26 + radius) for shape in self.holes
                      if self.plated_hole_roots.get(shape.wkb) != net_root)
        shapes.extend(shape.buffer(0.21 + radius) for record, shape in self.keepouts if layer in record["layers"])
        shapes.append(box(-26, -34, 26, 34).difference(self.board.buffer(-0.26 - radius)))
        return unary_union(shapes)

    def grid_route(self, endpoints):
        start, end, obstacles = endpoints
        blocked, labels = self.grid_data(obstacles)

        def coordinate(node):
            return float(self.x_coordinates[node[1]]), float(self.y_coordinates[node[0]])

        first_anchor, last_anchor = self.grid_anchor((start, end), (blocked, obstacles))
        if first_anchor is None or last_anchor is None:
            return None
        first, start_escape = first_anchor
        last, end_escape = last_anchor
        # Diagonal steps already require both orthogonal neighbours to be free,
        # so they cannot connect separate four-connected grid components.
        # Segment geometry checks and the clearance requirements stay intact.
        if labels[first] != labels[last]:
            return None
        heap = [(math.dist(first, last), 0, first)]
        costs = {first: 0}
        previous = {}
        while heap:
            _, cost, node = heapq.heappop(heap)
            if cost > costs[node]:
                continue
            if node == last:
                nodes = [node]
                while node != first:
                    node = previous[node]
                    nodes.append(node)
                positions = start_escape + [coordinate(n) for n in reversed(nodes)] + list(reversed(end_escape))
                simplified = [positions[0]]
                index = 0
                while index < len(positions) - 1:
                    candidate = len(positions) - 1
                    while candidate > index + 1 and LineString([positions[index], positions[candidate]]).intersects(obstacles):
                        candidate -= 1
                    if LineString([positions[index], positions[candidate]]).intersects(obstacles):
                        return None
                    simplified.append(positions[candidate])
                    index = candidate
                return simplified
            for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)):
                neighbor = node[0] + dy, node[1] + dx
                if not 0 <= neighbor[0] < blocked.shape[0] or not 0 <= neighbor[1] < blocked.shape[1] or blocked[neighbor]:
                    continue
                if dy and dx and (blocked[node[0] + dy, node[1]] or blocked[node[0], node[1] + dx]):
                    continue
                if not self.grid_edge_clear(node, neighbor, obstacles, blocked):
                    continue
                new_cost = cost + math.hypot(dx, dy)
                if new_cost < costs.get(neighbor, math.inf):
                    costs[neighbor] = new_cost
                    previous[neighbor] = node
                    heapq.heappush(heap, (new_cost + math.dist(neighbor, last), new_cost, neighbor))
        return None

    def grid_anchor(self, endpoints, grid_obstacles):
        blocked, obstacles = grid_obstacles
        results = []
        for position in endpoints:
            result = None
            escapes = []
            for distance in (0.9, 1.1, 1.3, 1.5, 0.7, 0.5, 0.3):
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    escape = position[0] + distance * dx, position[1] + distance * dy
                    if not LineString([position, escape]).intersects(obstacles):
                        escapes.append([position, escape])
            escapes.append([position])
            for escape_path in escapes:
                escape = escape_path[-1]
                approximate = round((escape[1] + 32) / self.grid_step), round((escape[0] + 24.5) / self.grid_step)
                candidates = [(approximate[0] + dy, approximate[1] + dx) for dy in range(-3, 4) for dx in range(-3, 4)]
                candidates = [n for n in candidates if 0 <= n[0] < blocked.shape[0] and 0 <= n[1] < blocked.shape[1]]
                candidates.sort(key=lambda n: math.dist((self.x_coordinates[n[1]], self.y_coordinates[n[0]]), escape))
                for node in candidates:
                    coordinate = float(self.x_coordinates[node[1]]), float(self.y_coordinates[node[0]])
                    if not blocked[node] and not LineString([escape, coordinate]).intersects(obstacles):
                        result = node, escape_path + [coordinate]
                        break
                if result:
                    break
            results.append(result)
        return results

    def plan_net(self, net):
        net_root = self.root(net["source_net_id"])
        ports = [p for p in self.ports.values() if self.root(p["source_port_id"]) == net_root
                 and self.source_ports[p["source_port_id"]].get("source_component_id") in self.source_components
                 and not self.port_name(p).startswith((".J3 >", ".J7 >"))]
        if len(ports) < 2:
            return [], "Fewer than two physical endpoints"
        width = net.get("trace_width", 0.2)
        paths, failures = [], []
        first_root = self.physical_root(ports[0]["pcb_port_id"])
        joined = [port for port in ports if self.physical_root(port["pcb_port_id"]) == first_root]
        ports = [port for port in ports if port not in joined]
        while ports:
            _, start, end = min(((math.dist(point(a), point(b)), a, b) for a in joined for b in ports), key=lambda edge: edge[0])
            obstacles = self.obstacles(net_root, "top", width)
            route = None if net["name"] in self.off_top_nets else self.grid_route((point(start), point(end), obstacles))
            layers = ["top"] * len(route) if route else []
            via_points = []
            if route is None:
                result = self.multilayer_route((point(start), point(end)), (net_root, width))
                if result is None:
                    failures.append(f"No ordinary through-via top/bottom path: {self.port_name(start)} to {self.port_name(end)}")
                    ports.remove(end)
                    continue
                route, layers, via_points = result
            component = self.components[start["pcb_component_id"]]
            rotation = math.radians(-component["rotation"])
            local = []
            for index, (x, y) in enumerate(route[1:-1], 1):
                dx, dy = x - component["display_offset_x"], y - component["display_offset_y"]
                waypoint = {"x": round(dx * math.cos(rotation) - dy * math.sin(rotation), 6),
                            "y": round(dx * math.sin(rotation) + dy * math.cos(rotation), 6)}
                local.append(waypoint)
                if layers[index] != layers[index + 1]:
                    local.append({**waypoint, "via": True, "fromLayer": layers[index], "toLayer": layers[index + 1]})
                    local.append(dict(waypoint))
            paths.append({"net": net["name"], "from": self.port_name(start), "to": self.port_name(end), "width": width,
                          "pcbPath": local, "global_path_mm": route, "segment_layers": layers,
                          "classification": "manual native trace"})
            for index, (first, second) in enumerate(zip(route, route[1:])):
                self.copper.append((net_root, layers[index + 1], LineString([first, second]).buffer(width / 2)))
            for via_position in via_points:
                hole = Point(via_position).buffer(0.15)
                self.holes.append(hole)
                self.plated_hole_roots[hole.wkb] = net_root
                for layer in ("top", "inner1", "inner2", "bottom"):
                    self.copper.append((net_root, layer, Point(via_position).buffer(0.35)))
            end_root = self.physical_root(end["pcb_port_id"])
            connected = [port for port in ports if self.physical_root(port["pcb_port_id"]) == end_root]
            joined.extend(connected)
            ports = [port for port in ports if port not in connected]
        return paths, "; ".join(failures) if failures else None

    def multilayer_route(self, endpoints, net_width):
        start, end = endpoints
        net_root, width = net_width
        top_obstacles = self.obstacles(net_root, "top", width)
        via_obstacles = []
        for record, shape in self.pads:
            port = self.ports.get(record.get("pcb_port_id"))
            same_net = port and self.root(port["source_port_id"]) == net_root
            via_obstacles.append(shape.buffer(self.copper_clearance + (0.15 if same_net else 0.35)))
        via_obstacles.extend(shape.buffer(0.41) for shape in self.holes)
        via_obstacles.extend(shape.buffer(0.56) for _, shape in self.keepouts)
        via_obstacles.extend(shape.buffer(0.35 + self.copper_clearance) for root, _, shape in self.copper if root != net_root)
        via_obstacles.append(box(-26, -34, 26, 34).difference(self.board.buffer(-0.61)))
        via_obstacles = unary_union(via_obstacles)

        def candidates(position):
            valid = []
            bent_candidates = []
            for distance in np.arange(0.6, 3.41, 0.2):
                for degrees in range(0, 360, 30):
                    angle = math.radians(degrees)
                    candidate = (round(position[0] + float(distance) * math.cos(angle), 6),
                                 round(position[1] + float(distance) * math.sin(angle), 6))
                    if Point(candidate).intersects(via_obstacles):
                        continue
                    if LineString([position, candidate]).intersects(top_obstacles):
                        bent_candidates.append(candidate)
                        continue
                    valid.append((candidate, [position, candidate]))
                    if len(valid) == 8:
                        return valid
            if valid:
                return valid
            for candidate in bent_candidates[:16]:
                escape = self.grid_route((position, candidate, top_obstacles))
                if escape:
                    valid.append((candidate, escape))
                    if len(valid) == 4:
                        break
            if not valid:
                valid = self.grid_escape(position, (top_obstacles, via_obstacles))
            return valid

        pairs = [(math.dist(start, a) + math.dist(a, b) + math.dist(b, end), a, b, first_escape, last_escape)
                 for a, first_escape in candidates(start) for b, last_escape in candidates(end) if math.dist(a, b) > 0.96]
        pairs.sort(key=lambda pair: pair[0])
        # Native trace pcbPath transitions to internal layers create partial-span
        # vias. Ordinary vias on this board must span top to bottom. Internal
        # routing is authored separately as native regions plus through vias.
        for layer in ("bottom",):
            obstacles = self.obstacles(net_root, layer, width)
            for _, first_via, last_via, first_escape, last_escape in pairs:
                route = self.grid_route((first_via, last_via, obstacles))
                if route:
                    # Layer at each point describes the segment arriving there.
                    # The native via after first_via changes the outgoing layer.
                    positions = first_escape + route[1:-1] + list(reversed(last_escape))
                    layers = ["top"] * len(first_escape) + [layer] * (len(route) - 1) + ["top"] * (len(last_escape) - 1)
                    return positions, layers, [first_via, last_via]
        return None

    def grid_escape(self, position, obstacles):
        top_obstacles, via_obstacles = obstacles[:2]
        blocked = contains_xy(top_obstacles, self.grid_x, self.grid_y)
        via_blocked = contains_xy(via_obstacles, self.grid_x, self.grid_y)
        if len(obstacles) == 3:
            allowed_exits = obstacles[2]
            if allowed_exits.dtype != np.bool_ or allowed_exits.shape != via_blocked.shape:
                raise ValueError('Exit reachability mask must match the native planning grid')
            via_blocked |= ~allowed_exits

        def coordinate(node):
            return float(self.x_coordinates[node[1]]), float(self.y_coordinates[node[0]])

        anchor = self.grid_anchor((position,), (blocked, top_obstacles))[0]
        if anchor is None:
            return []
        first, escape = anchor
        heap, costs, previous, exits = [(0, first)], {first: 0}, {}, []
        while heap:
            cost, node = heapq.heappop(heap)
            if cost > costs[node]:
                continue
            candidate = coordinate(node)
            if math.dist(position, candidate) > 6:
                continue
            if not via_blocked[node] and math.dist(position, candidate) >= 0.6 and all(math.dist(candidate, existing[0]) >= 0.4 for existing in exits):
                reverse = [node]
                current = node
                while current != first:
                    current = previous[current]
                    reverse.append(current)
                positions = escape + [coordinate(n) for n in reversed(reverse)]
                simplified = [position]
                index = 0
                while index < len(positions) - 1:
                    last = len(positions) - 1
                    while last > index + 1 and LineString([positions[index], positions[last]]).intersects(top_obstacles):
                        last -= 1
                    if LineString([positions[index], positions[last]]).intersects(top_obstacles):
                        break
                    simplified.append(positions[last])
                    index = last
                if index == len(positions) - 1:
                    exits.append((candidate, simplified))
                    if len(exits) == 4:
                        return exits
            for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)):
                next_node = node[0] + dy, node[1] + dx
                if not 0 <= next_node[0] < blocked.shape[0] or not 0 <= next_node[1] < blocked.shape[1] or blocked[next_node]:
                    continue
                if dy and dx and (blocked[node[0] + dy, node[1]] or blocked[node[0], node[1] + dx]):
                    continue
                if not self.grid_edge_clear(node, next_node, top_obstacles, blocked):
                    continue
                next_cost = cost + math.hypot(dx, dy)
                if next_cost < costs.get(next_node, math.inf):
                    costs[next_node] = next_cost
                    previous[next_node] = node
                    heapq.heappush(heap, (next_cost, next_node))
        return exits


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("circuit_json")
    parser.add_argument("output_json")
    parser.add_argument("nets", nargs="+")
    parser.add_argument("--off-top", default="", help="Comma-separated nets requiring a layer change before their long run")
    parser.add_argument('--reserve-proposals', action='append', default=[])
    parser.add_argument('--grid-mm', type=float, choices=(0.05, 0.1), default=0.1)
    parser.add_argument('--copper-reserve-mm', type=float, choices=(0.0001, 0.01, 0.07), default=0.01)
    args = parser.parse_args()
    circuit = json.loads(Path(args.circuit_json).read_text())
    planner = ManualSignalPlanner(circuit)
    planner.set_grid(args.grid_mm)
    planner.set_copper_reserve(args.copper_reserve_mm)
    for path in args.reserve_proposals:
        planner.reserve_proposals(json.loads(Path(path).read_text()))
    planner.off_top_nets = set(filter(None, args.off_top.split(",")))
    paths, unresolved = [], []
    Path(args.output_json).parent.mkdir(parents=True, exist_ok=True)
    for name in args.nets:
        net = next(r for r in circuit if r["type"] == "source_net" and r["name"] == name)
        planned, reason = planner.plan_net(net)
        paths.extend(planned)
        if reason:
            unresolved.append({"net": name, "reason": reason})
        print(json.dumps({"net": name, "manual_paths": len(planned), "unresolved": reason}), flush=True)
        Path(args.output_json).write_text(json.dumps({"classification": "manual proposals, not solver caches",
            "source_circuit_json": args.circuit_json, "grid_mm": planner.grid_step, "copper_clearance_mm": planner.copper_clearance,
            "paths": paths, "unresolved": unresolved}, indent=2) + "\n")


if __name__ == "__main__":
    main()
