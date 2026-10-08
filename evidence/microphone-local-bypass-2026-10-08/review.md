# Local microphone bypass — public WIP .10

The genuine 100 nF C81/C45000 capacitor now sits beside U5. Its actual 0.30 mm top-layer supply trace is **1.442790 mm**, and its top-layer ground entry into the real pour is **0.599976 mm**. Neither bypass branch uses a via. R93/C105881 moves clear of C81 and reconnects VMIC and MIC_WS through explicitly authored native copper. The same manufacturer parts, pin maps, bodies, pads, paste, models and courtyards are retained.

**This repair is qualified as WIP. The full board has not reached zero DRC and zero missing connections, and is not ready to order.** The requested centered approximately 2.8-inch landscape LCD remains unimplemented. Legacy LCD geometry visible in native previews is provisional and superseded by that request.

Exact accepted native: `dist/index/circuit.json`, SHA-256 **8be25ca28e6271890aab0d450ffdc62088ced91967ae1b6185ab8267ff9f1177**, 6,564,850 bytes. The actual completed frozen-runtime build takes 266.04 seconds. Its exit 1 retains the same 50 connection errors as the parent; no generated JSON is repaired or substituted. `native-generation.json`, `generation-source-manifest.json`, `native-circuit.json.gz` and `completed-source-and-events.tar.gz` bind the actual source and events.

## What changed and how it was checked

| Check | Actual result |
| --- | --- |
| C81 rigid pose | (17.05, −28.10) mm, 180°, top |
| R93 rigid pose | (16.50, −31.42) mm, 0°, top |
| Local real contacts | C81.1–U5.5, C81.2–U5.3, R93.1–U5.5 and R93.2–U5.1 connected |
| Full geometric audit | **0 measured shorts / 0 clearance and geometric violations**, but **12 assigned nets physically open**, so the full gate fails |
| Existing terminal contacts | All **9,813** parent pairs preserved; zero losses or missing ports |
| Purchased geometry | 123 stationary components exact; only the two declared rigid moves; all 125 identities retained |
| Original assets and solver caches | All 244 compared files unchanged |
| Authored native copper widths | All 250 active regions checked; zero failures |
| Native inventory | 381 traces / 320 through vias / 273 pours |
| Vias | Every measured via: 0.30 mm hole, 0.45 mm land, all four layers; no blind/buried vias |
| High-current layers | 67 native traces and 89 authored trunks checked; top/bottom only; thermal/current capacity remains unqualified |
| Five required source checks | Netlist, pin specification, source, schematic placement and placement all pass |
| TypeScript / formatting | Both pass |
| Routing regression tests | 94 pass |
| Board tests | 49 pass / 2 fail: complete connections and strict native schema |
| Actual schematic UI style analysis | **15 issues**, failed; normal TLS verification, approved existing NSS CA, no failed module requests |
| Source snapshots | Complete in 58.76 s; PCB and schematic differ from unchanged references; failed, no snapshot update |
| Strict native schema | 169 original failures; full lossless failure tree retained |
| Native paste | 32 records still missing on genuine U16/U27 pill pads |
| Official short checker | Fails `Unsupported shape polygon`; independent geometry results do not turn that check into a pass |
| Native trace widths | 381 traces / 628 segments measured; 2 below explicit source minima and 65 below named-net nominal widths remain |
| Assembly rotation | U14 exact supplier pin-one discrepancy remains |

`local-bypass-qualification.json`, `purchased-geometry.json`, `connection-preservation.json`, `final-copper-audit.json`, `final-native-compliance.json`, the three region-width receipts and `trace-widths.json` retain scoped results separately. A successful scoped acceptance script does not imply the full connected/DRC gate passed.

The manufacturer's ICS-43434 instructions require a close 0.1 µF X7R supply bypass and short single-layer connections. Untouched U5/C81 courtyards impose a 1.380059 mm minimum pad-centre separation, so the tool's automatic 1 mm capacitor limit cannot fit these real footprints. The explicit supply limit is finite at 2 mm. A separate finite 2.5 mm ground preflight allowance accommodates its 2.15 mm nearest-pad estimate before the pour exists; the measured ground entry is only 0.599976 mm. This does not change clearance, width or connectivity thresholds.

The changed microphone circuit page and component-guide page, all copper layers and focused U5/C81/R93 zoom were directly inspected. The other 24 schematic pages are byte-identical to the previously inspected .9 PNGs; `visual-review.json` records every page hash. The fresh UI result and screenshot remain independent of the passing CLI schematic-placement check.

The exported browser HTML contains a preview initialization credential. Public HTML explicitly redacts that content; original hashes and the private outside-repository preservation path are in `ui-analysis/html-redaction-receipt.json`. Screenshots, analysis receipts and native geometry remain untouched. HTML is not claimed to be a byte-identical raw capture.

## Genuine supplier metadata and rejected trials

Live supplier-analysis failures initially dropped genuine pin-one maps on 97 components. That physically clear output was rejected. The final normal renderer uses the **43 exact previously generated official v4 orientation analyses**, recovered from the checkpoint-bound completed .9 source archive. `restored-supplier-cache.json` records original paths, byte hashes and provenance. These are original pin-one/polarity results for unchanged parts, never invented data, dated stock assertions or patched solver caches. The final native retains the full stationary supplier maps.

The actual build has 127 regular source/runtime/model inputs and 43 hidden orientation-cache inputs. The supported public package contains 128 regular files including native JSON; hidden caches are preserved with exact public GitHub evidence and reproducible restoration instructions. Run `publish:prepare` first, then restore those actual analyses for a local source rebuild. Clean staging before registry publication; do not upload stale phase debug or snapshots as package source.

All rejected courtyard, mount, default-length, ground-preflight, timeout and missing-supplier-metadata trials retain their actual native/source/events/logs. The 447,080,710-byte ground-preflight debug log is losslessly compressed, with round-trip hashes. `schema-audit.json.gz` likewise preserves the complete original schema tree. No failed record is deleted to achieve the repair's acceptance.

Routing remains the selected `beta_pipeline9` with existing genuine phase replays and explicitly labelled manual copper. No newly successful whole-board Pipeline9 or Freerouting result is claimed.

## Remaining blockers to the user's full target

The remaining 50 native errors are **46 J7 / 4 U27**. Twelve assigned nets remain physically open: GND, VLCD, LCD_SDA, LCD_SCLK, LCD_DC, LCD_RESET_N, LCD_CS_N, four backlight returns and backlight output. **J3's two unassigned battery outer contacts are additional unresolved connections**, excluded from the assigned-net count.

The exact preferred ER-TFT028A3-4 primary PDF remains HTTP 403. The exact-manufacturer ER-TFT028A2-4 candidate has common-cathode backlighting, whereas the old circuit uses a common-anode arrangement. Its centered body overlaps the present RF keepout by 59.5 mm²; folded-FPC minimum bend radius, mating contact face, pin-one direction and final socket access are not qualified. These are real wiring/mechanical dependencies, not paths that a different autorouter can decide. J3's numbered mating-view polarity also remains unverified. Root `AGENTS.md` requires dependent work to stop when genuine contact/pin mappings are unresolved; manual routing cannot supply that missing evidence.

Fresh exact official JLC pages yielded **14 HTTP 200 identities: 12 covering one board and 2 insufficient public-buyability records; 29 HTTP 503 results are unknown**, not assumed available. D2/C94934 reports zero stock/buyability. U1/C2913201 reports overseas stock but zero public buyability; neither establishes assembly allocation. Exact USB-ESD replacement searches returned HTTP 403, and no unqualified replacement is introduced. `official-stock/receipt.json` and `dated-stock-application.json` bind all 125 placements / 43 identities to this native. Previous unchanged-identity component subtotal **$26.3055** is a dated reference, excluding PCB, assembly, shipping, display and battery; it is not a current order quote.

Latest official package versions and canonical sources were checked. Core 0.0.2110 still lacks the tested pill-paste repair and retains the same capacitor-length preflight behavior. Frozen active dependencies are retained; simply advancing version numbers would not resolve these observed defects. Schema/paste/Gerber, U14 rotation, current/thermal/width, schematic style, stackup, supplier and mechanical gates remain unresolved. No fabrication package or hardware-test approval is issued.

An actual isolated, unchanged official **circuit-json@0.0.521** comparison also reports **the same 169 failures and type breakdown** on this exact native. The separate Bun resolver reached its recorded 180-second budget; a direct official npm artifact with exact published SHA-1 and SHA-512 integrity was then downloaded and used for read-only validation, with the existing frozen Zod runtime. `latest-schema-receipt.json`, the exact official artifact and losslessly archived full failure tree retain this result. Active dependency pins and native JSON are unchanged.

The previous .9 post-upload cloud source job has now **actually completed without a user-code job error**; its exact public logs are in `previous-cloud-completed-build.json`. This supersedes the old unfinished observation, and does not prove zero DRC or fabrication readiness. .10 publication and exact anonymous source/native/preview receipts are recorded separately when verified.

## Exact .10 publication and cloud setup

Implementation commit **3d88ca2fe4d617de73e757aec6522ba3d79c4a3a** is public on GitHub main. Registry release **d17c1129-2a2a-4834-a186-e562b77aa268** is public, listed and ready to build. All **128 files** are anonymously byte-verified, and the [public preview](https://tscircuit.com/AnasSarkiz/tscircuit-ai-agent-remote/releases/d17c1129-2a2a-4834-a186-e562b77aa268/preview) contains the exact accepted native object. `github-publication-receipt.json`, `final-registry-receipt.json` and `final-public-preview-receipt.json` retain the checks. The official CLI initially rejected two large files with HTTP413. Existing 126 files were verified before two genuine missing files were resumed through bounded official archive uploads; readiness follows the supported server lifecycle, without a manual readiness override.

The later automatic cloud job **4cf44817-6713-4d77-8bba-d5d6b4c33bf7** failed with `user_code_job_infrastructure_error` after sandbox busy/initialization/retry exhaustion, before executing board source. Actual anonymous logs and the other automatic job are retained separately. Uploaded native preview verification is independent of cloud source execution; no successful .10 cloud CI result is inferred.

Both automatic jobs are confirmed completed with that infrastructure error. After verifying no active release job remained and all128 public files still matched, one supported session-authenticated `/package_builds/create` rebuild was requested, with no props injection or readiness change: **a8de600a-7593-411f-936b-beddba0201a5**. Actual logs show execution starting. `cloud-rebuild-request.json` and `cloud-rebuild-observation.json` retain the request and observation; completion remains unverified until actual terminal logs are read. No repeated watcher is enabled.

Cloud draft **revision30** is saved and read back exactly. Only continuation instructions change; installation, repositories, network policy, credential/runtime requirements and the 20 custom host entries are preserved. No domains were added. This does not apply or publish the environment; the user must review/save in environment settings and publish to activate it. Fresh-task restoration remains unverified. `cloud-configuration-save-receipt.json` and `cloud-startup-instructions.md` record the saved state.
