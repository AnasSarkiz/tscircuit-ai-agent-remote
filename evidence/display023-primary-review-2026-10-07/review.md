# ER-TFT023-1 primary review — 2026-10-07

The user uploaded the exact replacement datasheet and explicitly answered
**“Accept the 2.3-inch display (Recommended)”**. Select the no-touch ER-TFT023-1
for the next design revision. The earlier ≥80% display-body coverage requirement
is relaxed for this panel. Selection is accepted; a complete connector/flex
arrangement and a board implementation are not yet qualified.

## Primary evidence and dimensions

The uploaded `ER-TFT023-1_Datasheet.pdf` is archived byte-for-byte here:
934,319 bytes, 25 pages, SHA-256
`476f23033ca4ce0caa9ca6470fbc3d287b841240afaa54db986756fdfa588095`.
Source: user upload `file_0000000035c88246ac847e10a3175a43`.
Reviewed primary pages 4–6 and 9–12, revision 2.0 / 2018-08-08; no-touch drawing
dated 2015-11-17. The datasheet names **ILI9342**; the product URL/PDF keywords
spell ILI9432. Firmware must follow the actual ILI9342 specification.

- Native landscape body: 50.90 × 45.80 × 2.25 mm, ±0.20 / ±0.20 / ±0.15 mm.
- Rotate the front view 90° counterclockwise to obtain a 45.80 × 50.90 mm
  portrait body with a **right-side flex exit**. The native drawing itself has
  a bottom exit; changing the panel name alone does not solve the layout.
- Native active area 46.75 × 35.06 mm; portrait 35.06 × 46.75 mm, native 320×240.
- 50 contacts, 0.50 mm pitch, 24.50 ±0.05 mm contact span, 25.50 mm tail width,
  26.90 mm extension beyond the body.
- Terminal FPC **including its PI stiffener**: 0.30 ±0.03 mm thick. This is not a
  documented flexible-span thickness or minimum bend radius.
- Conductors: 0.35 ±0.05 mm wide. Exposed contacts: 3.50 ±0.20 mm long;
  rear stiffener: 4.50 ±0.30 mm deep.

The primary front/conductor view puts panel pin 1 on the right and pin 50 on
the left. Pin 1 becomes north after the portrait rotation. The contact face
points toward the user when the tail is flat. The manufacturer recommends a
50-pin 0.5 mm **top-contact ER-CON50HT-1** for its unfolded arrangement.
`no-touch-outline.png` and `no-touch-flex-detail.png` are document renderings,
not modified component drawings.

## Electrical audit

`audit-panel.py` checks all 50 contacts against the accepted native netlist.
Under the old provisional panel n → J7 (51−n) mapping, 49 assignments match the
new primary requirements. **Panel pin 6 / IM0 is grounded but must connect to
VLCD**: four-wire, eight-bit serial Interface I requires IM3…IM0 = **1111**,
where the old panel used 1110. This is a required role change, not approval of
the old physical contact mapping. New pin 33 is NC and remains open.
`primary-pin-audit.csv` records every assignment, including unused contacts.

The fixed TPS7A2028 regulator produces 2.8 V. Its ±1.5% accuracy interval,
2.758–2.842 V, fits the new VCI and VDDI ranges. VDDI has an absolute maximum of
3.0 V, so direct 3.3 V panel logic is unsuitable; retain the 2.8 V level shifter.
The four TPS60230 backlight sinks supply approximately 62.4 mA total, below the
panel's 80 mA maximum and its 70 mA typical operating point. This does not verify
actual brightness or power-up. The primary outline gives Vf = 3.0 V at 80 mA,
while its table gives 3.2 V typical / 3.3 V maximum at 70 mA; preserve that
manufacturer discrepancy rather than silently changing the specification.

## Connector arrangements and placement proposal

The existing genuine JLC import **AFC07-S50ECA-00 / C262650** is the top-contact
type recommended for a flat tail. Keeping it behind the panel requires a
qualified two-fold flex path to restore the upward conductor face. A candidate
rotation of 270° puts connector pin 1 north. Conditional correspondence is
panel n → J7 n, with final insertion toward +X. The old 51−n mapping cannot be
retained with this proposed pose.

A single fold flips the contacts toward the PCB and instead needs a
lower-contact socket, such as the genuine **AFC07-S50FCC-00 / C11063** at 90°.
That also conditionally maps n → n. Its specific primary drawing remains
unretrieved; the signed JLC datasheet CDN was denied by the proxy. The older
family drawing distinguishes upper/lower contact types, but neither this
alternative nor its final folded geometry is accepted as a drop-in replacement.
The two genuine imports have opposite local pin-1 sides.

Dated official stock observations from the preceding review: C262650 18,986
total / 18,798 available-to-buy; C11063 6,076 / 6,045, at 11:30 UTC. Reference
initial prices were $0.286 and $0.2569. These are observations, not an assembly
allocation, reservation or current quote. Neither arrangement adds an adapter.

The current J7 centre is approximately 11.8 mm below the new panel's flex
centreline. The following **unaccepted nominal proposal** avoids a socket-only
move overlapping U14:

| Item | Centre X, Y (mm) | Rotation |
| --- | --- | --- |
| Portrait display body | −3.5, −3.3 | Native front view 90° CCW |
| J7 / existing C262650 | 9.5, −3.3 | 270° |
| U14 | 2.25, 13.0 | 0° |
| C42 | 6.25, 15.7 | 270° |
| C43 | −1.15, 17.4 | 180° |

The body fits nominal case XY bounds and covers about **69.54%** of PCB area at
this pose; its maximum area ratio is 71.73%. The enclosure centre is (0, 3.5),
not the PCB origin. Nominal panel-to-antenna gap is 9.525 mm. The panel is thinner
than the rejected part, but that alone does not qualify the complete Z stack.

The nominal component rectangles have no pairwise overlap at a 0.20 mm review
margin after these moves. Genuine CLI measurement coupons, not hand-authored
footprints, establish the rotated capacitor and alternate-connector profiles.
The coupons are unrouted measurements and do not establish a complete-board
placement or connectivity pass. Three rejected rectangle proposals remain
archived. See `nominal-placement-proposal.png` / `.pdf`.

Actual socket housings extend beyond `pcb_component` rectangles: the genuine
ECA model spans 30.6 × 5.75 × 2.0 mm. Bend zones, flex-span thickness/minimum
bend radius, slot height, insertion engagement and full 3D clearance still need
qualification. The family connector drawing recommends conductor widths of
0.30 ±0.03 mm, versus the panel's 0.35 ±0.05 mm; full contact-tolerance review is
pending. No guessed numerical bend radius is treated as a manufacturer limit.

## Implementation status and genuine blockers

No canonical board source, copper, import, original solver cache, package file
or native artifact changed. Applying this proposal would require retiring and
reauthoring the affected manual copper, preserving all 9,842 previously connected
terminal pairs, and rerunning actual placement, shorts, clearance, widths,
through-via and connectivity checks. Native JSON must come from the canonical
CLI; measurement-coupon success cannot stand in for full-board validation.

U14 / C7848 has the existing strict supplier rotation discrepancy
`incompatible_pin1_locations`. Root `AGENTS.md` requires reporting imported
component issues and stopping dependent work; genuine imported definitions must
not be patched. This blocks accepting its proposed move. Final physical J7
mating is independently unresolved. Neither blocker is the missing new LCD PDF:
the upload now provides that primary document.

The accepted native remains SHA-256
`35c5fb2bfc870daf11b5f5e30847f1e5a86fd886ebb8ef11fc3cf6e88e77e63d`,
384 traces, 325 through vias, 270 pours, **50 native opens (46 J7 + 4 U27)**.
Zero previously measured shorts/clearance violations is not zero full DRC.
J3 outer polarity, strict schema/paste/export gates, width necks, availability
and the 14 actual UI schematic issues remain open. **Not ready to order.**

The review and selection record are published to GitHub under the existing
authorization. Public tscircuit **0.0.8-wip-speaker-routing** remains the previous
accepted implementation; no replacement implementation or new release is claimed.
Reusable startup instructions are updated to distinguish the approved panel
selection from this unaccepted physical proposal. A draft save does not apply
network settings or publish the environment.
