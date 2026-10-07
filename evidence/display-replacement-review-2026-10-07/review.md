# Proposed right-side display replacement — 2026-10-07

The user rejected the ER-TFT026-1 because its bottom flex does not fit the
existing right-side J7 placement. They requested review of this product and a
matching connector:

https://www.buydisplay.com/spi-2-3-inch-tft-lcd-touch-screen-display-320x240-ili9432-controller

The URL advertises a 2.3-inch, 320×240 SPI display with an ILI9432 controller.
The exact panel model, chosen touch option, glass outline, flex exit, flex
length, contact count, pitch, conductor face, stiffener thickness, numbered
pinout, logic supply, backlight requirements and price are **not verified**.
The older uploaded ER-TFT026-1 PDF does not describe this proposed replacement.

## Retrieval and qualification

The product request returned HTTP 403 with a Cloudflare JavaScript/cookie
challenge. A candidate manufacturer PDF path,
`/download/manual/ER-TFT023-1_Datasheet.pdf`, returned HTTP 403 / error 1010.
That filename is a hypothesis, not a verified part identity or datasheet.
A normal Chromium request, with the inherited proxy and TLS verification
preserved, failed with `ERR_CERT_AUTHORITY_INVALID`. No verification or
access policy was bypassed. Raw request receipts and the failed browser
outcome are retained. GitHub repository searches did not produce a drawing.
Generic JLC search results were unrelated or failed and were not accepted as
part or stock evidence.

The next required input is the proposed product's actual manufacturer PDF or
numbered mechanical/pinout drawing, including the selected touch/no-touch
variant. Review its flex in the intended assembled orientation against the
right-side socket, display clearance, antenna region and enclosure. Image
rotation in firmware alone does not establish mechanical fit. Replacing the
connector also requires a fresh native placement and pin-order review.

The advertised controller differs from the current ILI9341 selection, so its
initialization sequence and firmware driver must be reviewed. The existing
VLCD and backlight circuitry cannot be accepted for it from the product title.
The 2.3-inch diagonal is smaller than the existing 2.6-inch choice; the previous
≥80% physical display-overlap requirement must be reassessed using the actual
body drawing. No connector-specific routing is accepted before these facts
are known.

## Stocked connector candidate

**JUSHUO AFC07-S50FCC-00 / JLCPCB C11063** is a candidate for a **50-pin,
0.5 mm-pitch, bottom-contact** flex. Its genuine import and manufacturer models
already exist in `imports/AFC07_S50FCC_00/`; the original supported import
receipt is `evidence/a3-routing-2026-10-04/buydisplay/import-C11063.log`.
This is a candidate, not an accepted replacement for J7.

The official JLCPCB page at https://jlcpcb.com/partdetail/C11063 returned HTTP
200 on 2026-10-07 at 11:30 UTC, matching exact manufacturer part number
AFC07-S50FCC-00. It reports 6,076 total stock and 6,045 available to buy.
The reference initial part price is $0.2569; quantity pricing, assembly loading
fees, allocation and an order quote are not qualified. The part is in the
extended library. Current stock is not a reservation.

The current upper-contact **AFC07-S50ECA-00 / C262650** also has positive stock:
18,986 total / 18,798 available to buy. A different flex exit does not establish
which contact face is required. Choose between these or a different genuine
connector only from the replacement panel drawing and actual assembly.

The imported FCC and ECA parts have opposite local pin-1 sides: FCC pin 1 is
at x≈+12.25 mm, ECA pin 1 at x≈−12.25 mm. Swapping their component names while
retaining the provisional net mapping could reverse the physical contact
assignments. Their pitch and general family identity do not establish an
electrically interchangeable replacement.

JLCPCB's public C11063 datasheet download uses
`jlc-prod-smt.oss-eu-central-1.aliyuncs.com`; the configured proxy denied CONNECT
with HTTP 403. That exact hostname was added to the saved environment draft,
preserving the prior 13 domains and install script. The replacement-review
continuation instructions were also saved. Saving is confirmed, but applying
the draft requires the user to review/save settings and publish the environment.
It does not resolve the BuyDisplay-origin Cloudflare challenge by itself.

## Board and publication state

No connector, board net, placement, trace, imported definition or generated
native artifact changed. The public board remains 0.0.8-wip-speaker-routing,
source commit e8e4eb46da63fe4ddc398497d5212a415cfa8866, with native SHA-256
`35c5fb2bfc870daf11b5f5e30847f1e5a86fd886ebb8ef11fc3cf6e88e77e63d`.
Its 50 open-port errors remain; fabrication readiness is false. These review
receipts are metadata, not a new routed board implementation or package release.

The local `.agents/skills/tscircuit/SKILL.md` requires: “When the canonical
approach is blocked, diagnose it. If it cannot be completed within scope, stop
and report the blocker and the proper next action; never conceal it with a
hack or fallback.” The blocker here is missing authoritative replacement-panel
geometry and pin specifications. Supply the new product's PDF/drawing to
continue a qualified connector selection and board revision; no additional
permission to make the authorized replacement is needed.
