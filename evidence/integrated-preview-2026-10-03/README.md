# A1 complete native board — unrouted preview

Actual integrated `main.tsx`, based on parent `98a3f7e`. The board is 50 × 65 mm,
with four layers, 1.6 mm thickness and 3 mm corner radius. It has 122 genuine
imported electronic parts and 8 copper test pads, all on top, across 13 A4 sheets.
There are zero copper traces or vias and zero native PCB geometry errors.
This is an untested prototype, not approved for fabrication.

`board-overview.png` combines the final native PCB top, actual ratsnest and actual
GLB top/bottom renders. Individual PNGs, SVGs, `board.glb`, `circuit.json` and the
native 13-page `schematic.pdf` are retained. Render helpers use public converter
APIs and the native GLB without modifying emitted Circuit JSON. Blue rectangles
on the PCB show a provisional raised LCD body and active area. The 3D views show
the PCB assembly; enclosure, display and battery fit remain unqualified.

`command-results.json` records actual results: build, all five pre-route checks,
formatting, TypeScript and snapshots exited 0. Canonical tests have 30 passes and
one existing strict-schema failure. Full-board strict schema validation rejects
156 native elements: 130 PCB components, 13 PCB groups and 13 schematic groups.
Known B-010 union/anchor/display-offset failures are preserved in compact summaries;
raw outputs have not been rewritten.

Placement reports no errors or suboptimal orientations and two connector-facing
warnings for J6 (internal service) and J7 (internal display FPC). Imported role and
category warnings remain metadata gaps. Connector access, lands, paste, silk,
current, rails, transients, privacy, RF, thermal limits and mechanical fit need
qualification. TMR and ITERM intentionally use the manufacturer's open-pin defaults.

The battery connector assumes pin 1 BAT, pin 2 GND and pin 3 NTC. The protected
pack, 8 Ω speaker, 3 V motor, LCD/backlight and TALK actuator remain provisional.
Side-switch pin mapping, inrush and transitions need qualification. B-005 missing
polygon microphone ground paste remains a fabrication blocker.

Native snapshots and all 13 schematic pages were visually reviewed. Display and
microphone-clock sheet coordinates were moved inward after inspection. These
checks do not establish full electrical qualification. The bottom is unpopulated.

The overlapping initial 50 × 55 mm trial is retained under `initial-50x55/` and
in `initial-pcb.png`; it is historical evidence, not the final design.
`source-manifest.json` hashes final source, dependencies, imports and deliverables.
Earlier publication receipts and speaker observations accompany this actual
implementation milestone. Registry publication is tracked separately from build
success. The background watcher remains paused.
