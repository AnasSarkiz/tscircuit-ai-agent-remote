# Accepted human decisions and continuation authority

Latest request, 2026-10-05: "push it to tsci" explicitly authorizes publishing the current engineering WIP to tscircuit, superseding the earlier registry-upload deferral. Preserve all imported models and fabrication blockers; do not represent partial or unauthenticated publication as success.

This is a curated decision record, not a full conversation export. Original supplied briefs are in user-requests/ and current artifacts/validation supply exact engineering evidence.

- Continue the existing handheld AI remote to prototype fabrication readiness; do not restart. No fabrication order or invented physical tests.
- Rounded enclosure, dominant front display, one top-edge hold-to-talk button. Top PCB assembly. ESP32-S3 Wi-Fi/BLE/USB, dual digital microphones, external speaker, haptic function. J8 haptic JST removed in favor of direct motor pads. J6 UART optional; USB programming is required.
- PCB fixed 50 × 65 mm. Current accepted A7 thickness 1.0 mm, four layers. Enclosure maximum 60 × 75 × 16 mm; use latest A7 mechanical evidence, not earlier 15 mm proposal. Keep battery/display/metal/wiring outside the antenna region. Major placement frozen conditionally; documented C4 passive move accepted.
- Display bought from BuyDisplay, not JLCPCB: provisional ER-TFT026-1 no-touch with integrated ILI9341 controller, not the 8051 development kit. Physical display coverage target ≥80% of PCB; projected overlap 82.712%, tolerance allocation 81.737%. This does not prove final FPC fit or usable pixel coverage.
- Protected rechargeable 1S battery AKY2945 / LP523450. Supplier drawing: red BAT+, yellow 10 kΩ NTC in centre, black GND, JST PHR-3 2 mm. J3 centre must be PACK_NTC. Outer contact numbering NOT confirmed: do not guess or route either outer contact until keyed numbered supplier confirmation or physical measurement.
- J7 display connector orientation/face/pin1/short-FPC fold still needs exact physical/vendor evidence. Continue independent and upstream routing; no speculative contact-dependent fanout.
- Genuine JLC imports for board electronics; no custom/edited imported symbols or footprints except expressly allowed C370970 and C5656610 0.60 mm acoustic hole. Alternatives must be genuine imports with pin/land/stock review. Current resistor substitution C22548 → C21190 and C105588 → C22775; verify BOM quantities/current stock before assembly.
- Both board GitHub repository and tscircuit package must be public, with generated circuit.json included. Official compressed registry upload was explicitly authorized; A7 brief currently defers registry upload retries and requests routing progress. Migration Git push is authorized and needed for Cloud.
- Saved routes must preserve real native events/full JSON/per-phase paths before moves and demonstrate replay. Manual native paths allowed, clearly separated from genuine solver outputs. Incomplete/time-killed solver runs are NOT accepted routes.
- Stop reporting issues to another chat. Background automation remains paused; do not resume it. No extra threads/agents requested.
- Latest instruction: stop Mac routing due to memory exhaustion; set up this repo for Codex Cloud with all relevant continuation context. Carry over current accepted checkpoint and unbuilt proposals separately. Linux setup/resource supervisor limits one heavy process at a time and records failures truthfully.

Engineering status remains partial routing, pending copper/DRC/fabrication review. See CLOUD_HANDOFF.md for current exact build/source/cache hashes, blockers, next actions and commands.
