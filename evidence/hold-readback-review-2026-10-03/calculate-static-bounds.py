"""Conditional engineering calculations; not dynamic privacy qualification."""
import json
from pathlib import Path

folder = Path(__file__).parent
resistance_allowance = 0.021
hold_pulldown_max_ohms = 10000 * (1 + resistance_allowance)
readback_series_min_ohms = 1000 * (1 - resistance_allowance)
readback_series_max_ohms = 1000 * (1 + resistance_allowance)
main_rail_min_volts = 3.18204
main_rail_max_volts = 3.43818
microphone_ldo_enable_low_max_volts = 0.3
report = {
    "status": "conditional calculations, not qualification",
    "assumptions": [
        "2.1% resistor allocation exceeds compounded 1% initial plus 100ppm/C over 100C (2.01%); final YAGEO and aging review pending",
        "Main rail bounds are the prior static buck review, not measured transient limits",
        "SN74LVC1G17 5uA input leakage is tested at VI=5.5V or GND, not every release voltage",
        "TPS7A20 250nA EN leakage is tested at VEN=VIN=6V, not a low-EN guarantee",
        "ESP32 50nA input current and threshold rows apply at 3.3V, 25C; internal pulls disabled",
        "No bound is asserted for slow power ramps, floating ground, bounce or off deadline",
    ],
    "released_hold": {
        "pulldown_max_ohms": hold_pulldown_max_ohms,
        "total_source_leakage_budget_microamps_for_en_low":
            microphone_ldo_enable_low_max_volts / hold_pulldown_max_ohms * 1e6,
        "illustrative_release_volts_at_5_25_microamps": hold_pulldown_max_ohms * 5.25e-6,
        "old_100k_candidate_budget_microamps_with_added_readback_load":
            microphone_ldo_enable_low_max_volts / (100000 * 1.02) * 1e6,
        "qualification": "Do not extend endpoint leakage tests to arbitrary EN voltage; review full input loading",
    },
    "pressed_hold": {
        "minimum_nominal_pulldown_current_microamps": main_rail_min_volts / hold_pulldown_max_ohms * 1e6,
        "maximum_nominal_pulldown_current_microamps": main_rail_max_volts / (10000 * (1 - resistance_allowance)) * 1e6,
        "qualification": "Switch contact/trace drops and exact ALPS application acceptance pending",
    },
    "readback_at_3_3_volts_25_c": {
        "minimum_high_volts": 3.3 - .1 - 50e-9 * readback_series_max_ohms,
        "maximum_low_volts": .1 + 50e-9 * readback_series_max_ohms,
        "mcu_high_threshold_volts": .75 * 3.3,
        "mcu_low_threshold_volts": .25 * 3.3,
        "qualification": "Full supply/temperature, GPIO selection, startup pulls and timing pending",
    },
    "opposing_gpio": {
        "conditional_static_current_max_milliamps": main_rail_max_volts / readback_series_min_ohms * 1000,
        "qualification": "No protection against independent overvoltage, transient clamps or powered-off injection is asserted",
    },
    "schmitt_thresholds": {
        "at_vcc_3_volts_positive_threshold_max_volts": 1.92,
        "at_vcc_3_volts_negative_threshold_min_volts": .89,
        "qualification": "Discrete datasheet rows are not interpolated into a guaranteed full main-rail range",
    },
}
(folder / "static-bounds.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report["released_hold"]))
