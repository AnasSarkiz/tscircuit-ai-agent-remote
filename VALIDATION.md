# Validation — A0

Date: 2026-10-02 (Europe/Tirane). **Blocked before a complete schematic/PCB exists. Not fabrication ready.** A0 identifies engineering intake and import qualification, not a fabricated board revision. No physical hardware is available.

| Stage | Status | Evidence and remaining work |
|---|---|---|
| 1. Confirm requirements | in progress | Brief and approved maximum 50 × 65 mm; display/battery mechanics, current budget, mounting and stackup unresolved |
| 2. Schematic and BOM | blocked | C370970 holes and mounting slots exceed manufacturer ranges; complete schematic/BOM not authored |
| 3. Placement before routing | not started | Depends on stages 1–2; no placement/render exists |
| 4. Copper routing | not started | User authorized routing after prerequisite gates pass; no routes exist |
| 5. Automated and visual checks | not started | Preliminary import checks below do not complete board validation |
| 6. Prototype fabrication | not started | No Gerbers, drills, assembly BOM or placement files |
| 7. Physical prototype | not started | No hardware or physical test evidence |
| 8. Store release | not started | Publication not authorized; no release package |

## Source and dependencies

Project: `boards/tscircuit-ai-agent-remote--01a0fe57`. No earlier board was reused. The Git milestone containing this file identifies the source revision (`git rev-parse HEAD`). `evidence/source-manifest.sha256` records sources, unchanged imported definitions/assets, references, package manifest and lockfile before that commit; excludes itself, Git metadata, dependencies, build output and logs.

Pinned dependencies: tscircuit **0.0.2729**, @tscircuit/cli **0.1.2228**, TypeScript **5.9.3**, Biome **2.5.14**, @types/bun **1.4.2**. Runtime Bun **1.3.9**. `bun.lock` records transitive dependencies. Installation emitted peer-version warnings involving circuit-json 0.0.509, React/ReactDOM 19.3.0 and @tscircuit/alphabet 0.0.25; unresolved, not accepted board warnings.

Initializer succeeded; optional skill download failed under sandbox networking. Installed tscircuit skill and current official handbook were read. CLI help verified required netlist, pin_specification, source, schematic-placement, placement and shorts commands, PNG/SVG builds and snapshots. Native A4 API verified in installed @tscircuit/props: `<schematicsheet name displayName sheetIndex sheetSize="A4">`. No sheet has been rendered/reviewed.

## Requirements

Approved maximum **50 × 65 mm** supersedes initial approximately 50 × 45 mm. Four copper layers intended. Scope: 5 V USB-C sink/native USB, protected 500–1000 mAh single-cell LiPo, 3.3 V rail, ESP32-S3 antenna module, dual digital microphones, SPI color display, I2S amplifier/external 8 Ω speaker, haptic output, RGB indication, encoder/push, TALK/APPROVE/REJECT, power/privacy switches, BOOT/RESET and test access. Firmware is outside scope.

JLCPCB is the intended board/assembly manufacturer. Final stackup, copper weight/thickness, trace widths, clearances, drill/via limits, current limits and layer spans have **not** been selected or validated. Do not treat default geometry as a manufacturing specification. Exact battery protection/thermistor/polarity/rating, display procurement/interface/mechanics, mounting, enclosure and RF clearance must be resolved before stage 1 passes.

ESP32-S3-WROOM-1-N8R8 octal PSRAM reserves GPIO35/36/37. Manufacturer antenna guidelines were consulted; no RF keepout is laid out. Hardware microphone privacy requires supply isolation and prevention of clock/data phantom power; Ioff buffer candidates are not electrically qualified.

## BLOCKING B-001 — C370970

**ALPS EC11E15244G1, C370970.** Supported import: `tsci import --jlcpcb C370970 --use-exact-footprint --download`. Component source/models remain unmodified. Import log, original supplier record and `evidence/imports/C370970-audit.json` preserve provenance/measurements.

| Feature | Imported | Official ALPS range | Result |
|---|---|---|---|
| Five terminal holes | 1.3000228 mm diameter | 1.00–1.10 mm | fail |
| Two mounting slots | 3.200019 mm long | 2.60–2.70 mm | fail |

Exact-part mounting GIF and EC11E catalogue page 2 drawing 2 were inspected: `references/alps-ec11e15244g1-mounting.gif`, `references/alps-ec11e.pdf`, `evidence/datasheets/alps-ec11e-2.png`. The 14.5 mm row spacing is correct. Manufacturer 12.5 mm measures outside slot edges, not center spacing; neither is falsely flagged.

Affected stages: 2–6. Workspace instructions prohibit patching imports and require stopping dependent work. Resolve through a corrected supported import or a genuine alternative qualified against its own drawing. No generic footprint or altered hole geometry was used.

C209762 / EC11J1525402 was researched and imported as an alternative, but ALPS marks it **Not Recommended for New Designs**. It is not selected or fully qualified. A viable qualified encoder remains unresolved.

## Other preliminary evidence

C109322 / TPS63070RNMR was rejected for missing physical pin identities 8/13 (grouped same-net pads) and lost PS/SYNC alias. This is not a diagnosed short. Alternate C2845237 / TPS63802DLAR retains all ten pin identities/functions; two identity tests pass, but application design, passives, full footprint/model review and current limits remain pending. Official DLA0010A package/land pattern, pages 35–36, were rendered and inspected: `evidence/datasheets/tps63802-35.png` and `tps63802-36.png`.

Waveshare 1.54 inch display schematic page 1 was inspected (`evidence/datasheets/waveshare-1.54-1.png`). **J1 and PH connector J2 have opposite listed pin order:** J1 VCC/GND/DIN/SCK/CS/DC/RST/BL; J2 BL/RST/DC/CS/SCK/DIN/GND/VCC. Final module/connector procurement remains unresolved. Downloaded DXF is unreviewed; no display component was authored.

Free-text import `1.54 LCD` selected unrelated DSK110 / C908227; excluded from selected components. Initial formatting touched whitespace in four imports; restored through supported importer, original C109322 checksum matched. `imports/**` is excluded from formatting.

## Commands actually run

Commands run from this project directory. Logs under `evidence/tooling/`.

| Command | Actual result | Log |
|---|---|---|
| `bun run format:check` | exit 0 | format-check.log |
| `bun run typecheck` | exit 0 | typecheck.log |
| `bun test` | exit 1; 2 pass, 2 fail | import-qualification-current.log; both failures C370970 geometry |
| `bun run build` | exit 1; explicit blocker; no board generated | build-blocked.log |

Build guard in `main.tsx` prevents claiming an incomplete board built successfully. Tooling success does not establish electrical correctness. Earlier `import-qualification.log` records rejected TPS63070 checks, not current board results.

Required placement checks (`netlist`, `pin_specification`, `source`, `schematic-placement`, `placement`) have **not** run against a complete circuit: none exists and stage 2 is blocked. Routed build, `check shorts dist/index/circuit.json`, snapshot and copper-layer visual review have **not** occurred. No board DRC/shorts pass or snapshot acceptance is claimed.

## Routes and fabrication

Supported native route-cache type `{pcbTraces, cacheKey}` exists; cache-key generation/reuse still needs verification. `routes/README.md` records route preservation/repair intent. **No saved routes exist.** There is no copper to move or repair and no fabrication package.

Complete A4 sheets, bodies/courtyards, connector/test access, holes, each copper layer, critical power paths, mask/paste, outline, drills, assembler feedback and fabrication exports remain unreviewed. No accepted board warnings, physical measurements, hardware photos or test results are invented.
