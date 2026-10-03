# Nominal mechanical envelope study — incomplete

Parent source: a1e76d5f2879d74b68d882c3ea5576359b0ccc42. The new SVG/PNG
is a dimension study, not an imported-component definition, native PCB
placement, enclosure CAD or fabrication approval. It was visually inspected.

The genuine LCD C5329581 / HS17QS178RX **is already imported**. Its manufacturer
drawing gives a 33.7 × 42.94 × 2.2 mm module, active area 28.03 × 35.04 mm and
17.28 ± 0.3 mm tail dimension. This study uses the manufacturer's body envelope,
not the different imported body graphic. Mounting, tail bend and connector
position are unqualified. The accepted product picture is not dimensioned CAD.

ESP32-S3-WROOM-1-N8R8 C2913201 is nominally 18 × 25.5 × 3.1 mm, with
width/length ±0.2 mm and height ±0.15 mm. Recommended land drawing identifies
a 7.49 mm antenna area. Espressif recommends antenna beyond the base board,
feed point near its edge, or appropriate substrate removal if the antenna
cannot fully extend outside. End-product antenna clearance of at least 15 mm
in all directions is recommended; throughput/range still require physical tests.

## Trial results

For both trials, the nominal **physical module body center** is (0,22) mm.
This is not the imported component's native PCB origin. Native body graphic
extents are y=-8.9940511 to+16.5449631 mm relative to its origin, giving a
3.775456 mm offset. The corresponding application instance trial is
pcbY=18.224544 mm. Pin1's top copper land edge is y=9.4949518 mm relative
to that origin, giving required land top y=27.7194958 mm. Ignoring this
offset and treating pcbY as the body center would give incorrect pad support.
The graphic/model-to-physical drawing alignment still requires final CAD review.

LCD is centered in x, with its body bottom 1 mm inside the PCB's bottom edge.
PCB dimensions shown are the board's rectangular envelope, before antenna
substrate removal. **No keepout or cutout was generated or approved.**

| Trial | LCD top y | Antenna lower boundary y | Nominal gap | First-land support margin |
| --- | ---: | ---: | ---: | ---: |
| 50 × 50 mm | 18.94 mm | 27.26 mm | 8.32 mm | -2.72 mm |
| 50 × 65 mm | 11.44 mm | 27.26 mm | 15.82 mm | +4.78 mm |

The square **trial** fails both land support and the conservative 15 mm
LCD-to-antenna separation. This does not prove every square layout impossible.
The approved 50 × 65 mm trial has 0.82 mm nominal excess clearance, before
module, LCD, assembly and enclosure tolerances. A 2.19 mm plan-view overlap
between LCD body and module shield requires a raised LCD and actual vertical
clearance review; it does not represent permitted body contact. Module antenna
extends 2.25 mm beyond the PCB top. The case must accommodate it.

The antenna's expanded in-plane study region spans x=-24..24 mm and
y=12.26..49.75 mm. Therefore an arbitrary metal top-edge switch on a 50 mm
wide PCB is not qualified by the LCD clearance calculation. Its body, pads,
actuator, mounting, wiring and enclosure location must be checked. No switch
was added to this sketch or silently moved onto a second assembled PCB.
Exact battery, speaker and their metal/wiring envelopes must also be reviewed.

The user's compact rounded square exterior, dominant screen, one top control
and top-side assembly requirements remain active. These trial board envelopes
do not establish final exterior dimensions or prove the accepted visual design
is mechanically feasible. Stage 1 and complete placement remain unfinished.

## Sources

- Board `references/esp32-s3-module.pdf`, Espressif v1.8, physical dimensions
  p42 and recommended land drawing p44; the WROOM-1 height is 3.1±0.15 mm,
  distinct from WROOM-1U's 3.2±0.15 mm.
- Board `references/HS17QS178RX.pdf`, exact selected LCD manufacturer drawing.
- [Espressif module layout guidance](https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html#general-principles-of-pcb-layout-for-modules-positioning-a-module-on-a-base-board),
  checked 2026-10-03.
- Untouched native C2913201 import for actual origin and first-pad copper
  coordinates. The study renderer uses transformation-matrix for PCB-to-SVG
  coordinates; diagrams do not modify the imported definition.
