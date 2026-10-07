# Canonical rounded-pad paste repair — tested source, unreleased runtime

The missing paste is a generator defect. `SmtPad.doInitialPcbPrimitiveRender`
emits rounded copper pads for `pill` and `rotated_pill`, but neither branch creates
solder paste. The native schema already supports both rounded paste shapes.

The source repair is implemented against
[tscircuit/core commit 90785db](https://github.com/tscircuit/core/commit/90785dbb91162d8ff7a25dbad6533929d8546f4c),
whose package version is **0.0.2106**. `source.patch` contains the complete six-file
change, including two visual regression tests. No imported component definition,
installed library bundle or generated native JSON was hand-patched.

The focused helper copies the emitted pad's actual position, rotation, layer and
component/group links. Its default aperture scales width, height and radius by
0.7. Explicit margins apply per side, corner radius cannot exceed the aperture's
half-dimensions, and covered or fully removed apertures produce no paste.

## Reproduction and checks

Before the repair, both new tests fail: zero paste records instead of 16 and 8.
Afterwards, **17 relevant tests pass with 308 assertions**, including existing
rectangle, circle, polygon, pill, imported-footprint and rotation regressions.
The full upstream TypeScript check, canonical formatting, package build and
distribution smoke tests pass. The entire upstream test suite was not run.
The upstream source diff passes whitespace and reverse-application checks
against its base. The archived patch retains one required blank context marker;
Git flags that marker as trailing whitespace when the patch itself is staged.
It is preserved byte for byte, rather than corrupting the applicable patch.

The older Bun 1.3.9 dependency installs stalled within their recorded budgets.
Using the repository's CI Bun **1.4.0**, current official source and supported
`--network-concurrency 4`, installation completed in 12.04 seconds. One install
postinstall was blocked by Bun's normal trust policy; the required build and
tests nevertheless ran successfully. Verbose install logs remain private because
they can contain transient redirect headers; resource outcomes are archived.

Cross-package checks use the handbook's build/yalc workflow in an isolated
coupon project. The unmodified canonical C7848 import produces **20 pads and 20
schema-valid native paste apertures**. Every physical pad field matches the
earlier coupon exactly. Its source SHA remains
`7713a61c8f3d2f1c8108d2fcb9ba89f494a129bf5481e5ed4b8e93682e6e386e`.
The existing genuine BQ24074RGTR/U16 and TPS60230RGTR/U27 imports produce
**34 pads and 34 valid apertures**, including both exposed center pads, with
rotation and bottom-layer reflection. All four PNGs were visually inspected.
These are component coupons, not a routed-board or stencil approval.

Yalc links were removed and official packages restored before this evidence was
committed. An initial link briefly targeted the board directory and was removed;
no board build ran with it. The board's package/lock are unchanged, and its
installed core package, JavaScript and types match a fresh official 0.0.2090 npm
tarball byte for byte. The coupon's restored official 0.0.2106 runtime reproduces
**0 versus 20** paste records. Therefore this tested fix is still unreleased.
The source emits a literal software stamp of 0.0.2107 despite package metadata
0.0.2106; the exact source commit identifies these local captures.

## Actual requested PCB outcome

The prior [exact display review](../display028-integration-2026-10-07/review.md)
and [mechanical overlay](../display028-integration-2026-10-07/mechanical-review.pdf)
remain applicable. This source repair does not resolve those mechanical gates.

| Requested result | Verified current result |
| --- | --- |
| Final display | Not selected; ER-TFT028A2-4 is an exact-datasheet candidate. Preferred A3 PDF remains challenged. |
| Manufacturer drawing | Archived exact EastRising ER-TFT028A2-4 no-touch drawing, 2019-12-10; SHA in the prior review. |
| Landscape body / active area | 69.3 × 50.2 mm / 57.6 × 43.2 mm. Body remains centered in the reviewed overlay. |
| FPC exit | Right side in the reviewed finished landscape orientation. |
| Final J7 pose | Unassigned. Current accepted native pose is (8.2, −12.625) mm, 90°; it is not a qualified replacement pose. |
| Components moved | None accepted in the active board. |
| Schematic / routing changes | None accepted. Candidate needs SPI mode 0110 and common-cathode backlight changes; final numbered connector mapping is unqualified. |
| Connectivity / DRC | Fresh unchanged-board audit: 0 measured shorts, 0 measured clearance violations, 12 physical open nets. Native has 50 open-port errors. Full pass is false. |
| Fabrication | Blocked; no fabrication package or order approval. |

Centered LCD body overlaps the current antenna keepout by **59.5 mm²**. The flat
26.7 mm tail extends beyond the enclosure; a compatible return path needs verified
contact face, numbered mating order, bend radius, latch access and Z clearance.
The manufacturer PDF gives no numerical minimum bend radius. Moving J7 or routing
its contacts before those checks would rely on assumptions the user forbids.

The accepted native SHA remains
`35c5fb2bfc870daf11b5f5e30847f1e5a86fd886ebb8ef11fc3cf6e88e77e63d`.
Existing schema, stock, trace-width, Gerber, battery-contact and programmer gates
remain open. The board's 32 missing U16/U27 paste records are not claimed fixed.
Next dependencies are a supported released generator repair and the exact
LCD/RF/flex qualification, followed by actual placement, schematic changes,
rerouting and full board requalification. No upstream release, merge, order or
physical-test claim is made.

The saved cloud draft is revision **28**, with 20 custom hosts and updated
continuation instructions. It adds `pkg.pr.new`; saving does not apply runtime
network settings or publish the environment. The initial public verification
confirms GitHub commit 0684f56 and tscircuit release
`0.0.8-wip-speaker-routing` are public and carry the exact accepted native bytes.
