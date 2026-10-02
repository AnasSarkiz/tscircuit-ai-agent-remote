# Issues — A0

## RESOLVED LOCALLY B-001: C370970 terminal holes and mounting-slot lengths

Part: **C370970, ALPS EC11E15244G1**. Imported using pinned CLI 0.1.2228 with `--jlcpcb --use-exact-footprint --download`.

- Five terminal holes: 1.3000228 mm imported; manufacturer 1.00-1.10 mm.
- Two mounting slots: 3.200019 mm long imported; manufacturer 2.60-2.70 mm.
- Hole pattern row spacing 14.5 mm is correct (7 + 7.5 mm); no false row-spacing discrepancy is reported.
- Manufacturer 12.5 mm dimension is measured across outside slot edges, not between slot centers.

Affected gates: schematic/BOM import qualification (stage 2), placement/mechanics (stage 3), then routing, checks and fabrication (stages 4-6).

Evidence: `evidence/imports/C370970-audit.json`, original supplier JSON, `references/alps-ec11e15244g1-mounting.gif`, `references/alps-ec11e.pdf` and `evidence/datasheets/alps-ec11e-2.png`. Independent manufacturer-range tests reproduce both failures.

Original resolution rule prohibited local component edits. The user's subsequent explicit instructions authorized updating both C370970's symbol and footprint. The local import now has five **1.05 mm** terminal holes and two **2.65 mm** mounting-slot lengths, within the original unchanged manufacturer-range tests. Other geometry, centers, pin mappings, identity and models are preserved. This exception applies to C370970 only; no supplier library update is claimed.

Current evidence: `evidence/imports/C370970-footprint-change.json`, `evidence/encoder-footprint-circuit.json`, `evidence/encoder-footprint-pcb.svg` and PNG. Generated geometry was measured, the PCB preview inspected, and the isolated component placement check passed with zero errors/warnings. All four existing qualification tests pass without changing their limits. Final finished-hole tolerances, complete board integration, mechanical assembly and physical fit remain pending; this does not approve fabrication.

Historical alternative investigation: **C209762 / EC11J1525402** imported successfully through the supported workflow. ALPS marks this exact part Not Recommended for New Designs, so it was not selected or fully qualified. The user-authorized C370970 correction resolves the reported dimension issue instead.

Historical symbol-only change (revision 1f63764, 2026-10-02): removed C370970's custom `symbol` JSX prop. Native `chip` renders a box and preserves seven source pins (6–12). At that revision the footprint was unchanged and B-001 remained open. Audit: `evidence/imports/C370970-symbol-change.json`; preview: `evidence/encoder-chip-box-schematic.svg`. The subsequent authorized footprint correction is recorded above.

## Candidate rejection R-001: TPS63070RNMR C109322

The original import omits physical pin identities 8 and 13 and loses pin 1's PS/SYNC functional alias. TI assigns 7/8 to VOUT and 12/13 to VIN; grouped pads are electrically equivalent but do not satisfy exact pin identity qualification. This is not evidence of a short.

The supported import of genuine TI **TPS63802DLAR C2845237** retains all ten manufacturer pin numbers/functions and is an alternative candidate. No TPS63070 dependent circuit was authored. Old TPS63070 source and failed qualification evidence are retained; it is excluded from the proposed active BOM. TPS63802 placement, passives, complete power design and model qualification remain pending. This change resolves selection dependency on TPS63070, not the board validation stage.

## Other pending items

### RESOLVED LOCALLY B-002 — C5656610 / ICS-43434 acoustic opening

Unmodified import has a 0.3999992 mm acoustic hole. TDK DS-000069 v1.2 page 17 recommends a minimum 0.50 mm PCB opening. Original six pin identities/functions match page 10. This is a manufacturer-recommendation discrepancy, not a diagnosed short or absolute electrical-rating violation. The independent opening test fails; stage 2 and dependent stages 3–6 remain blocked.

Audit: `evidence/imports/C5656610-audit.json`. Prepared but **not applied**: `evidence/proposals/C5656610-acoustic-hole.diff`, diameter-only correction to 0.60 mm. Existing C370970 authorization does not cover this microphone, so approval for other documented import corrections was requested. Original microphone source/pads/models remain unchanged. The user requested waiting for an upstream correction. Fresh import with tscircuit 0.0.2736 / CLI 0.1.2232 on 2026-10-03 still measures 0.3999992 mm. Evidence: `evidence/update-check-2026-10-03/microphone-check.json`; the published fix is not verified. The user reaffirmed waiting for the upstream correction after this recheck; no local microphone edits or substitutions are authorized. No board routing is authorized before the remaining prerequisite gates pass.

TDK's manufacturer pages differ on lifecycle (Production/NRND versus EOL). Final selection/availability must be checked; this does not itself establish a bad import. Local datasheet download returned HTML, preserved as download evidence. Official PDF text was accessible through web tools; no local PDF render is claimed.

### Remaining design work

- Display: manufacturer documentation obtained for Waveshare 1.54inch LCD Module, ST7789, 240 x 240, 3.3 V operation, 50 x 35 mm module with PH2.0 eight-pin connection. Exact JLCPCB-sourced display/connector and permitted external assembly need final qualification; no display component or footprint has been authored.
- A free-text supported-import search for `1.54 LCD` selected the unrelated **DSK110 diode C908227**. That file is preserved as evidence of the search behavior and is not a display or active BOM selection. Future imports must use verified exact part numbers.
- Supplier catalogue stock/prices are inconsistent between catalogue/search endpoints. Exact JLCPCB assembly availability/classification and costs remain unverified.
- Accepted 2026-10-03: square, dominant screen, one top hold-to-talk button, top-side assembly only, speaker and rechargeable battery. See `REQUIREMENTS.md`. Prior encoder/extra-button/front-LED requirements are superseded; their imports remain historical evidence.
- Privacy: retain hardware microphone disable and prevent audio clock/data phantom power, using the single-control design. Exact architecture and Ioff buffer qualification remain pending; no software-only mute substitution.
- Battery: protected 1S nominal 3.7 V / 4.2 V-charge, 500–1000 mAh pack; exact MPN, sourcing/import, protection, thermistor, polarity and peak current rating remain pending. New SMT connector candidate C295747 is imported verbatim. Official JST drawing fetch returned 403; full footprint qualification is still pending. Charger/connector imports do not establish an integrated rechargeable system.
- Power budget, USB enumeration/current policy, passive component selection and regulator loop layout remain pending.
- A4 schematic, complete pin allocation, board outline/mounting, component placement, RF keepout and enclosure/ergonomics remain pending.
- Saved native routes and DRC/short repair remain pending because pre-routing gates have not passed.
- No physical prototype is available; no hardware results or physical photos are claimed.

## Tooling notes

- Initial optional skill download failed in the sandbox; the installed tscircuit skill and official handbook were read directly.
- A first formatter run changed import whitespace. All four affected imports were restored with the supported importer; regulator checksum matched the original. `imports/**` is now excluded from formatting.
- Initial diagnostic-script TypeScript errors were corrected by making the script a module; no component source was patched.
- LCSC encoder datasheet download returned an HTML challenge despite HTTP 200. Preserved as `evidence/downloads/C370970-datasheet-challenge.html`; actual official ALPS PDF and mounting diagram were obtained and inspected.
- Initial GitHub creation was rejected by automatic approval review. A narrower empty-private-repository creation succeeded after proving the attached brief explicitly requested it. Repository identity: AnasSarkiz/tscircuit-ai-agent-remote.

## User-authorized local C5656610 correction — 2026-10-03

The user's latest direct instruction authorizes manual correction after confirming
that the supplier footprint is undersized. This supersedes the prior wait for
upstream for this local correction. Only the acoustic diameter changed from
0.3999992 to **0.60 mm**. A byte comparison proves all other imported source is
unchanged. Source center, pads, pin mappings and models are preserved.

Audit: `evidence/microphone-local-correction-2026-10-03/change-audit.json`.
Generated diameter is 0.60 mm, minimum hole-to-copper gap is 0.2580203 mm,
and the isolated placement check passes with 0 errors / 0 warnings. All five
existing import tests pass. Supplier raw data and the converter remain unchanged.
Previous B-002 failure and wait entries above are historical evidence.

## BLOCKING B-003 — C5656610 native ground-pad port generation

The current native renderer reports `source_ambiguous_port_reference` for MIC1.GND.
Pin 3 consists of four separated polygon pad shapes, matching the imported
supplier layout. The renderer requires matched shapes to overlap before it
creates a PCB port for that logical pin. It produces six logical ports but only
five PCB ports, with all four ground shapes carrying `pcb_port_id: null`.

Using the documented `MIC1.pin3` selector correctly creates a source trace to
GND; the PCB-port generation still fails. Changing selector aliases therefore
does not resolve this error. The corrected component build exits 1. No DRC
suppression or geometry/pin-map workaround was applied. This is not a diagnosed
short or proof that the four-segment supplier pad geometry is itself incorrect.

Evidence: `evidence/microphone-local-correction-2026-10-03/build.log`, `circuit.json`
and `change-audit.json`. Affected stage: 2 and dependent stages 3–6. Full-board
schematic, component selection, battery/display mechanics and placement are
also unfinished. Stop dependent routing until native port handling and all
prerequisite checks are resolved.

## Publication status

Root AGENTS.md now authorizes and requires pushing each completed implementation
step and publishing the same prototype revision. GitHub source push is being
performed for this correction. Tscircuit publication is **blocked** by the failed
component build (B-003) and the main entry's explicit incomplete-design build
failure. No invalid package, placeholder success or bypassed build is published.
