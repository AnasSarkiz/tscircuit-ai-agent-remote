"""Draw the nominal review proposal; this does not model the flex or certify DRC."""
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).resolve().parent


def add_rectangle(axis, specification):
    bounds = specification["bounds"]
    axis.add_patch(Rectangle((bounds[0], bounds[1]), bounds[2] - bounds[0],
                             bounds[3] - bounds[1], **specification["style"]))


def main():
    audit = json.loads((OUTPUT / "primary-panel-audit.json").read_text())
    native = json.loads((ROOT / "dist/index/circuit.json").read_text())
    names = {record["source_component_id"]: record["name"] for record in native
             if record["type"] == "source_component"}
    components = {names[record["source_component_id"]]: record for record in native
                  if record["type"] == "pcb_component"
                  and record["source_component_id"] in names}
    coupon = json.loads((OUTPUT / "bypass-measurements/circuit.json").read_text())
    coupon_names = {record["source_component_id"]: record["name"] for record in coupon
                    if record["type"] == "source_component"}
    profiles = {coupon_names[record["source_component_id"]]: record for record in coupon
                if record["type"] == "pcb_component"}
    figure, axes = plt.subplots(1, 2, figsize=(11, 7), layout="constrained")
    for axis in axes:
        add_rectangle(axis, {"bounds": [-30, -34, 30, 41],
                             "style": {"fill": False, "edgecolor": "black", "linewidth": 1.5}})
        add_rectangle(axis, {"bounds": [-25, -32.5, 25, 32.5],
                             "style": {"fill": False, "edgecolor": "#315475", "linewidth": 1.5}})
        add_rectangle(axis, {"bounds": [-22, 31.675, -2, 39.675],
                             "style": {"facecolor": "#ffdddd", "edgecolor": "#9e2020"}})
        axis.text(-12, 35.5, "Antenna keepout", fontsize=8, ha="center")
        axis.set(xlim=(-33, 33), ylim=(-37, 44), xlabel="PCB X (mm)", ylabel="PCB Y (mm)")
        axis.set_aspect("equal")
        axis.grid(alpha=0.15)
    add_rectangle(axes[0], {"bounds": audit["proposed_panel_bounds_mm"],
                           "style": {"facecolor": "#e8dfb6", "edgecolor": "#736028"}})
    add_rectangle(axes[0], {"bounds": [-23.95, -26.675, 11.11, 20.075],
                           "style": {"facecolor": "#8dafc5", "edgecolor": "#315475"}})
    axes[0].text(-6.42, -3.3, "ER-TFT023-1\nportrait active area\n35.06 × 46.75 mm", ha="center")
    axes[0].annotate("Right-side flex exit\npath and folds unqualified", xy=(19.4, -3.3),
                     xytext=(19.4, -22), fontsize=8, rotation=90,
                     arrowprops={"arrowstyle": "->"})
    axes[0].set_title("Panel proposal: 45.8 × 50.9 mm body\n69.54% nominal PCB overlap")
    for name, component in components.items():
        moved = name in audit["proposed_board_pose_changes_mm"]
        centre = audit["proposed_board_pose_changes_mm"].get(name, [component["center"]["x"],
                                                                  component["center"]["y"]])
        profile = profiles[name] if name in ["C42", "C43"] else component
        bounds = [centre[0] - profile["width"] / 2, centre[1] - profile["height"] / 2,
                  centre[0] + profile["width"] / 2, centre[1] + profile["height"] / 2]
        add_rectangle(axes[1], {"bounds": bounds,
                               "style": {"facecolor": "#e8b165" if moved else "#cdd1d5",
                                         "edgecolor": "#915810" if moved else "#73777b",
                                         "linewidth": 0.7}})
        if moved or name == "U1":
            axes[1].text(*centre, name, fontsize=7, ha="center", va="center")
    current = components["J7"]
    add_rectangle(axes[1], {"bounds": [current["center"]["x"] - current["width"] / 2,
                                       current["center"]["y"] - current["height"] / 2,
                                       current["center"]["x"] + current["width"] / 2,
                                       current["center"]["y"] + current["height"] / 2],
                           "style": {"fill": False, "edgecolor": "#b32323", "linestyle": "--"}})
    axes[1].set_title("Nominal PCB footprint proposal\nOrange: J7 / U14 / C42 / C43 moves")
    figure.suptitle("REVIEW ONLY — no accepted PCB change, physical mating or full DRC pass", fontsize=12)
    figure.savefig(OUTPUT / "nominal-placement-proposal.png", dpi=180)
    figure.savefig(OUTPUT / "nominal-placement-proposal.pdf")
    plt.close(figure)


if __name__ == "__main__":
    main()
