"""Read-only primary-panel, existing-native and genuine-connector comparison.

The pin table below is external assembly review evidence, not a component
definition. This script does not write board source, imports or circuit JSON.
"""

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = Path(__file__).resolve().parent


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare_panel_pin(panel_pin, context):
    connector_pin = 51 - panel_pin
    source_port_id = context["ports"][connector_pin]["source_port_id"]
    existing_nets = sorted({
        context["nets"][net_id]
        for trace in context["traces"]
        if source_port_id in trace["connected_source_port_ids"]
        for net_id in trace["connected_source_net_ids"]
    })
    expected_net = context["expected"][panel_pin]
    return {
        "panel_pin": panel_pin,
        "panel_function": context["functions"][panel_pin],
        "existing_provisional_J7_pin": connector_pin,
        "existing_native_nets": existing_nets,
        "ER_TFT023_1_required_net": expected_net,
        "matches_new_primary_under_old_mapping": existing_nets == (
            [expected_net] if expected_net else []
        ),
        "conditional_rotated_ECA_two_fold_J7_pin": panel_pin,
    }


def component_bounds(component, centre):
    half_width = component["width"] / 2
    half_height = component["height"] / 2
    return [centre[0] - half_width, centre[1] - half_height,
            centre[0] + half_width, centre[1] + half_height]


def overlap_with_margin(bounds, context):
    other = context["other"]
    margin = context["margin_mm"]
    return (bounds[0] < other[2] + margin and bounds[2] > other[0] - margin
            and bounds[1] < other[3] + margin and bounds[3] > other[1] - margin)


def main():
    native = json.loads((ROOT / "dist/index/circuit.json").read_text())
    source_components = {r["source_component_id"]: r for r in native
                         if r["type"] == "source_component"}
    connector = next(r for r in source_components.values() if r["name"] == "J7")
    ports = {r["pin_number"]: r for r in native
             if r["type"] == "source_port"
             and r["source_component_id"] == connector["source_component_id"]}
    expected = {pin: None for pin in range(1, 51)}
    functions = {1: "LEDA", 2: "LEDK1", 3: "LEDK2", 4: "LEDK3", 5: "LEDK4",
                 10: "RESET", 11: "VSYNC", 12: "HSYNC", 13: "DOTCLK", 14: "DE",
                 33: "NC", 34: "SDA", 35: "RD", 36: "WRX(D/CX)",
                 37: "D/CX(SCL)", 38: "CSX", 39: "TE", 40: "VDDI",
                 41: "VDDI", 42: "VCI", 43: "GND", 44: "XR(X+)/SCL",
                 45: "YD(Y+)/SDA", 46: "XL(X-)/INT", 47: "YU(Y-)/RESET",
                 48: "GND", 49: "GND", 50: "GND"}
    expected[1] = "LCD_BACKLIGHT_OUTPUT"
    for pin in range(2, 6):
        expected[pin] = f"LCD_BACKLIGHT_RETURN_{pin - 1}"
    for pin in range(6, 10):
        functions[pin] = f"IM{pin - 6}"
        expected[pin] = "VLCD"
    for pin in [*range(11, 33), 43, 48, 49, 50]:
        expected[pin] = "GND"
    for pin in range(15, 33):
        functions[pin] = f"DB{32 - pin}"
    for pin in [35, 40, 41, 42]:
        expected[pin] = "VLCD"
    expected.update({10: "LCD_RESET_N", 34: "LCD_SDA", 36: "LCD_DC",
                     37: "LCD_SCLK", 38: "LCD_CS_N"})
    context = {"ports": ports, "functions": functions, "expected": expected,
               "nets": {r["source_net_id"]: r["name"] for r in native
                        if r["type"] == "source_net"},
               "traces": [r for r in native if r["type"] == "source_trace"]}
    pins = [compare_panel_pin(pin, context) for pin in range(1, 51)]
    mismatches = [r for r in pins if not r["matches_new_primary_under_old_mapping"]]
    coupon = json.loads((OUTPUT / "connector-coupon/circuit.json").read_text())
    coupon_component = next(r for r in coupon if r["type"] == "pcb_component")
    components = {source_components[r["source_component_id"]]["name"]: r
                  for r in native if r["type"] == "pcb_component"
                  and r["source_component_id"] in source_components}
    bypass_native = json.loads((OUTPUT / "bypass-measurements/circuit.json").read_text())
    bypass_names = {r["source_component_id"]: r["name"] for r in bypass_native
                    if r["type"] == "source_component"}
    bypass_profiles = {bypass_names[r["source_component_id"]]: r for r in bypass_native
                       if r["type"] == "pcb_component"}
    proposed_centres = {"J7": [9.5, -3.3], "U14": [2.25, 13.0],
                        "C42": [6.25, 15.7], "C43": [-1.15, 17.4]}
    proposed_rotations = {"J7": 270, "U14": 0, "C42": 270, "C43": 180}
    existing_pose_collisions = []
    proposed_pose_collisions = []
    proposed_bounds = component_bounds(components["J7"], proposed_centres["J7"])
    for name, component in components.items():
        if name == "J7":
            continue
        bounds = component_bounds(component, [component["center"]["x"],
                                               component["center"]["y"]])
        if overlap_with_margin(proposed_bounds, {"other": bounds, "margin_mm": 0.2}):
            existing_pose_collisions.append(name)
    bounds_by_name = {
        name: component_bounds(bypass_profiles[name] if name in ["C42", "C43"] else component,
                               proposed_centres.get(name, [component["center"]["x"],
                                                           component["center"]["y"]]))
        for name, component in components.items()
    }
    for name in proposed_centres:
        for other, bounds in bounds_by_name.items():
            if name == other:
                continue
            if overlap_with_margin(bounds_by_name[name], {"other": bounds, "margin_mm": 0.2}):
                proposed_pose_collisions.append([name, other])
    panel_centre = [-3.5, -3.3]
    panel_bounds = [-26.4, -28.75, 19.4, 22.15]
    overlap_area = 44.4 * 50.9
    result = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "primary_pdf_sha256": sha256(OUTPUT / "ER-TFT023-1_Datasheet.pdf"),
        "primary_revision": "2.0 / 2018-08-08",
        "no_touch_outline_date": "2015-11-17",
        "primary_pages_reviewed": [4, 5, 6, 9, 10, 11, 12],
        "native_sha256": sha256(ROOT / "dist/index/circuit.json"),
        "model": "ER-TFT023-1", "controller": "ILI9342", "touch": False,
        "resolution_native_pixels": [320, 240],
        "native_body_mm": [50.9, 45.8, 2.25],
        "body_tolerances_mm": [0.2, 0.2, 0.15],
        "portrait_body_mm": [45.8, 50.9, 2.25],
        "native_active_area_mm": [46.75, 35.06],
        "portrait_active_area_mm": [35.06, 46.75],
        "portrait_active_centre_offset_mm": [-2.92, 0.0],
        "manufacturer_recommends_unfolded_top_contact": True,
        "connector_contacts": 50, "connector_pitch_mm": 0.5,
        "FPC_terminal_with_PI_stiffener_thickness_mm": 0.3,
        "FPC_terminal_with_PI_stiffener_thickness_tolerance_mm": 0.03,
        "flexible_span_thickness_and_minimum_bend_radius_specified": False,
        "FPC_contact_span_mm": 24.5, "FPC_contact_span_tolerance_mm": 0.05,
        "FPC_contact_width_mm": 0.35, "FPC_contact_width_tolerance_mm": 0.05,
        "FPC_terminal_width_mm": 25.5, "FPC_extension_mm": 26.9,
        "FPC_exposed_contact_length_mm": 3.5,
        "FPC_exposed_contact_length_tolerance_mm": 0.2,
        "FPC_rear_stiffener_depth_mm": 4.5,
        "FPC_rear_stiffener_depth_tolerance_mm": 0.3,
        "native_flex_exit": "bottom in landscape front view",
        "right_flex_orientation": "panel rotated 90 degrees CCW, front facing user",
        "pin1_front_conductor_view": "right; becomes north in this portrait pose",
        "fold_back_contact_face": "faces PCB after a 180-degree fold about the vertical pin-row axis",
        "fold_back_lower_contact_candidate": "AFC07-S50FCC-00 / C11063",
        "fold_back_conditional_panel_to_FCC_pin_mapping": "n -> n, FCC at pcbRotation=90",
        "preferred_top_contact_candidate": "Retain AFC07-S50ECA-00 / C262650, rotate to pcbRotation=270",
        "preferred_top_contact_flex_path": "Two folds about axes parallel to the vertical contact row; conductor face restored upward; final insertion travels +X",
        "preferred_top_contact_conditional_panel_to_J7_pin_mapping": "n -> n; exact bend/insertion path remains unqualified",
        "two_fold_geometry_is_an_analytical_proposal_only": True,
        "full_physical_mating_qualified": False,
        "final_socket_arrangement_accepted": False,
        "specific_FCC_primary_drawing_retrieved": False,
        "connector_recommended_FPC_width_mm": 0.30,
        "connector_recommended_FPC_width_tolerance_mm": 0.03,
        "FPC_contact_width_tolerance_review_required": True,
        "interface": "4-wire 8-bit serial Interface I",
        "required_IM3_to_IM0": "1111", "existing_IM3_to_IM0": "1110",
        "VCI_normal_V": [2.7, 3.0, 3.3],
        "VDDI_normal_V": [1.65, "1.8/2.8", 3.0],
        "VDDI_absolute_max_V": 3.0,
        "VLCD_nominal_V": 2.8, "LDO_accuracy_fraction": 0.015,
        "VLCD_accuracy_interval_V": [2.758, 2.842],
        "regulated_VLCD_interval_within_panel_limits": True,
        "backlight_parallel_chips": 4,
        "backlight_typ_current_mA": 70, "backlight_max_current_mA": 80,
        "backlight_Vf_table_at_70mA_V": [3.2, 3.3],
        "backlight_Vf_outline_at_80mA_V": 3.0,
        "manufacturer_Vf_table_outline_discrepancy_retained": True,
        "existing_backlight_nominal_total_mA": 62.4,
        "nominal_current_exceeds_maximum": False,
        "brightness_or_hardware_qualified": False,
        "native_pin_rows_checked": len(pins),
        "matching_rows_under_old_provisional_mapping": len(pins) - len(mismatches),
        "new_primary_mismatches_under_old_provisional_mapping": mismatches,
        "pins": pins,
        "smaller_display_user_accepted": True,
        "prior_80_percent_body_coverage_requirement_relaxed_for_this_panel": True,
        "maximum_body_area_fraction_percent": 45.8 * 50.9 / 3250 * 100,
        "proposed_panel_centre_mm": panel_centre,
        "proposed_panel_bounds_mm": panel_bounds,
        "proposed_nominal_PCB_body_overlap_percent": overlap_area / 3250 * 100,
        "case_centre_mm": [0.0, 3.5],
        "case_outer_maximum_mm": [60, 75, 16], "case_wall_mm": 0.8,
        "case_inner_XY_bounds_mm": [-29.2, -33.2, 29.2, 40.2],
        "proposed_panel_body_within_nominal_case_XY": True,
        "antenna_lower_Y_mm": 31.675, "proposed_panel_antenna_gap_mm": 9.525,
        "proposed_board_pose_changes_mm": proposed_centres,
        "proposed_board_rotations_degrees": proposed_rotations,
        "ECA_at_proposed_pose_overlaps_existing_parts": existing_pose_collisions,
        "nominal_rectangles_after_proposed_moves_collisions": proposed_pose_collisions,
        "nominal_rectangle_margin_mm": 0.2,
        "placement_native_DRC_or_copper_clearance_pass_inferred": False,
        "footprint_rectangles_do_not_bound_full_3D_housings": True,
        "ECA_genuine_OBJ_extent_mm": [30.6, 5.75, 2.0],
        "FCC_genuine_OBJ_extent_mm": [30.6, 5.4, 2.0],
        "proposed_source_or_native_changes_applied": False,
        "remaining_gates": [
            "Specific FCC primary geometry only if choosing the single-fold lower-contact alternative; signed JLC datasheet CDN remains policy-denied",
            "FPC conductor-width tolerance comparison with the selected connector",
            "Bend radius/component-zone/slot-height and actual 3D flex path",
            "Full native placement and copper revalidation after moving J7/U14/C42/C43",
            "Canonical U14/C7848 supplier pin-1 rotation discrepancy",
            "Remaining unchanged board routing/fabrication gates",
        ],
        "fabrication_ready": False,
    }
    (OUTPUT / "primary-panel-audit.json").write_text(json.dumps(result, indent=2) + "\n")
    with (OUTPUT / "primary-pin-audit.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(pins[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(pins)
    print(json.dumps({k: result[k] for k in [
        "native_pin_rows_checked", "matching_rows_under_old_provisional_mapping",
        "new_primary_mismatches_under_old_provisional_mapping",
        "ECA_at_proposed_pose_overlaps_existing_parts",
        "nominal_rectangles_after_proposed_moves_collisions",
        "maximum_body_area_fraction_percent",
        "proposed_nominal_PCB_body_overlap_percent", "fabrication_ready"]}, indent=2))


if __name__ == "__main__":
    main()
