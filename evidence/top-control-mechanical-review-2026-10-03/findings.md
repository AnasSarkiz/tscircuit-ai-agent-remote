# Top-control nominal mechanical study — unqualified

Source base fa90b5420f8e567270697c68132f311444a42424. This is a read-only dimension study using manufacturer body envelopes and preserved native pad geometry. It creates no purchased component definitions, final native PCB placement, keepout/cutout or fabrication files. The diagram was visually inspected.

The earlier50x65mm trial put the ESP32-S3-WROOM-1-N8R8/C2913201 physical body center at(0,22)mm. A top-edge SKSWCFE010/C255576 candidate at(21,30.5)mm has only9.9495088mm nominal separation between its body/terminal envelope and the antenna rectangle. It intersects the conservative15mm recommendation region. This is a trial placement issue, not a supplier footprint defect.

Moving only the module physical center to(-8,22)mm gives17.9495088mm nominal control/antenna separation. The matching imported native application origin is(-8,18.224544)mm, accounting for the prior3.775456mm body-graphic offset. No imported geometry was moved or edited in source. The relative manufacturer graphic/3D alignment remains subject to final CAD qualification.

The actual49 rectangular native MCU lands remain within the50x65mm board envelope, minimum nominal edge margin4.7805042mm. Actual two native switch lands have minimum nominal edge margin1.238mm. These bounds include native pad extents, not just component centers. The LCD body remains33.7x42.94mm, lower edge at-31.5mm and upper edge11.44mm; its nominal antenna gap remains15.82mm. Active area28.03x35.04mm still needs review against the requested dominant front screen and final square enclosure. A PCB trial is not proof that the accepted conceptual exterior is dimensionally feasible.

The LCD body and module shield retain2.19mm plan-view overlap, requiring a raised LCD, vertical clearance and tail/connector validation. The module antenna extends2.25mm beyond the rectangular PCB top; substrate removal, board-outline and enclosure clearance are unqualified. The switch's top-push direction is normal to the PCB; a top-edge enclosure control still requires a real actuation mechanism and travel/tolerance review. The tiny switch is a candidate under a larger actuator, not a visually prominent user-facing button by itself.

RF keepout applies to all copper layers and conductive component/body/wiring/enclosure material. The study does not position or clear microphone hardware, screw heads, pack metal, speaker metal, FPC, other parts or enclosure surfaces. No RF range/throughput tests have been performed. Module/switch/LCD placement tolerances and actual keepout polygon must be reviewed before approving any placement. The switch's separate land/paste/application acceptance remains pending; this study does not resolve B-005, B-006 or B-010.

Inputs preserved and measured:

- references/esp32-s3-module.pdf — manufacturer v1.8 dimensions and land drawing, prior documented7.49mm antenna region and18x25.5mm body.
- references/HS17QS178RX.pdf — actual C5329581 display drawing.
- evidence/hold-control-alternate-review-2026-10-03/alps-sksw.pdf — current ALPS drawing and that folder's qualification record.
- evidence/mcu-usb-review-2026-10-03/circuit.json — native U1 center/pad geometry, unchanged full JSON and its separate schema status retained.
- evidence/hold-control-alternate-review-2026-10-03/circuit.json — native SW4 center/pad geometry, unchanged full JSON and its separate schema status retained.
- Espressif module layout guidance: https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html#general-principles-of-pcb-layout-for-modules-positioning-a-module-on-a-base-board

Transformations use transformation-matrix. The measurement parser only reads numeric rectangle geometry, asserts unrotated native instances and fails for missing/unsupported shapes. It is not a weaker replacement for the required native validation or full Circuit JSON schema gate. The current board remains unrouted and not ready for fabrication.
