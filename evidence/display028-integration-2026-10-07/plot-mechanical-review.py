"""Show exact panel/body dimensions against unchanged native PCB geometry.

The straight FPC rectangle is a dimensional envelope, not a qualified neck,
fold or mating model. No minimum bend radius is inferred from terminal thickness.
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

OUTPUT = Path(__file__).resolve().parent


def rectangle(axis, specification):
    left, bottom, right, top = specification["bounds"]
    axis.add_patch(Rectangle((left, bottom), right-left, top-bottom, **specification["style"]))


def main():
    audit = json.loads((OUTPUT / "mechanical-and-interface-audit.json").read_text())
    projection = json.loads((OUTPUT / "finished-front-native-projection.json").read_text())
    figure, axes = plt.subplots(1, 2, figsize=(15, 7), layout="constrained")
    for axis in axes:
        rectangle(axis, {"bounds": [-37.5, -30, 37.5, 30], "style": {"fill": False, "edgecolor": "#333333", "linewidth": 1.7}})
        rectangle(axis, {"bounds": [-36.7, -29.2, 36.7, 29.2], "style": {"fill": False, "edgecolor": "#555555", "linestyle": ":", "linewidth": 1}})
        rectangle(axis, {"bounds": [-41, -30, 34, 30], "style": {"fill": False, "edgecolor": "#aa7733", "linestyle": "--", "linewidth": 1}})
        pcb_outline = [[point["x"], point["y"]] for point in projection["pcbOutline"]]
        axis.add_patch(Polygon(pcb_outline, facecolor="#e9f0e8", edgecolor="#37684d", linewidth=1.5))
        rectangle(axis, {"bounds": audit["antenna_keepout_landscape_bounds_mm"], "style": {"facecolor": "#f5c0c0", "edgecolor": "#a52323", "linewidth": 1.5}})
        axis.text(-36, -12, "Existing RF\nkeepout", ha="center", fontsize=8)
        axis.set_aspect("equal")
        axis.set(xlabel="Finished landscape front X (mm)", ylabel="Finished front Y (mm)")
        axis.grid(alpha=0.15)
    rectangle(axes[0], {"bounds": [-34.65, -25.1, 34.65, 25.1], "style": {"facecolor": "#d8dce2", "edgecolor": "#606874", "alpha": 0.85}})
    rectangle(axes[0], {"bounds": [-32.25, -21.9, 25.35, 21.3], "style": {"facecolor": "#7fb3cc", "edgecolor": "#24566b", "alpha": 0.85}})
    axes[0].text(-3.45, 0, "ER-TFT028A2-4 candidate\nILI9341 / landscape 320 x 240\nActive: 57.6 x 43.2 mm", ha="center", fontsize=10)
    rectangle(axes[0], {"bounds": [-34.65, -22, -31.675, -2], "style": {"fill": False, "edgecolor": "#ba1111", "hatch": "////", "linewidth": 1.5}})
    rectangle(axes[0], {"bounds": [34.65, -12.75, 61.35, 12.75], "style": {"fill": False, "edgecolor": "#bd7023", "linestyle": "--", "linewidth": 1.5}})
    axes[0].text(48, 0, "Unfolded tail\n26.7 +/- 0.5 mm\nDimensional envelope\nNeck offset unqualified", ha="center", fontsize=8)
    axes[0].annotate("Right-side flex exit; return path required\nNo qualified bend radius/path or final J7 pose", xy=(35, -9), xytext=(5, -35), fontsize=8, arrowprops={"arrowstyle": "->"})
    axes[0].set(xlim=(-45, 66), ylim=(-39, 34), title="Exact candidate outline over unchanged PCB\n77.31% enclosure body coverage / 100% PCB coverage")
    for courtyard in projection["outlines"]:
        points = [[point["x"], point["y"]] for point in courtyard["outline"]]
        connector = courtyard["reference"] == "J7"
        axes[1].add_patch(Polygon(points, facecolor="#f0c97f" if connector else "#bbbbbb", edgecolor="#945911" if connector else "#666666", linewidth=0.6))
        if courtyard["reference"] in ["J7", "U14", "U1", "C42", "C43", "U27", "J1"]:
            center = projection["frontPoses"][courtyard["reference"]]["center"]
            axes[1].text(center["x"], center["y"], courtyard["reference"], fontsize=7, ha="center", va="center")
    rectangle(axes[1], {"bounds": [-34.65, -25.1, 34.65, 25.1], "style": {"fill": False, "edgecolor": "#24566b", "linestyle": "--", "linewidth": 1.5}})
    axes[1].set(xlim=(-45, 41), ylim=(-39, 34), title="125 actual native component courtyards\nCurrent J7 shown; no new placement accepted")
    axes[1].text(0, -35, "Black: centered 75 x 60 mm target case\nBrown dash: existing offset case; LCD crosses its right wall", ha="center", fontsize=8)
    figure.suptitle("MECHANICAL BLOCKER REVIEW - NO IMPLEMENTED DISPLAY REPLACEMENT OR ROUTING PASS", fontsize=11)
    figure.savefig(OUTPUT / "mechanical-review.png", dpi=160)
    figure.savefig(OUTPUT / "mechanical-review.pdf")
    plt.close(figure)


if __name__ == "__main__":
    main()
