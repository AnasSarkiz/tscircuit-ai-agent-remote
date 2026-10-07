# 2.8-inch landscape integration — blocked, not implemented

The latest pasted request supersedes the accepted 2.3-inch selection. The actual
PCB has **not** been replaced or rerouted for a new display. No final J7 pose,
physical mating, whole-board DRC pass or fabrication approval is claimed.

## Exact manufacturer source and candidate

Preferred ER-TFT028A3-4 manufacturer download still returns a Cloudflare challenge.
Normal TLS-verified Chromium identifies a blocked challenge request to
`brunhild.challenges.cloudflare.com`. The root challenge hostname responding does
not establish access to this subdomain. Direct supplier retries, normal browser
results and precise network failures are preserved; no CAPTCHA automation, proxy
bypass or disabled TLS was used.

The accessible exact alternative is **ER-TFT028A2-4, no touch**. Its EastRising
manufacturer PDF is mirrored at
https://raw.githubusercontent.com/sndsgd/kicad-er-tft028a2-4/main/ER-TFT028A2-4_Datasheet.pdf
and archived under `primary/`. Manufacturer identity, exact model, rev 1.0,
24 pages, Dec02-2019 release and Dec10-2019 no-touch drawing were inspected.
PDF SHA256: `637fdf1c1d3e1bb76c9a3f534855007989b22854a9e32f2ed9caa483b4eae10c`.
Manufacturer product link recovered from the mirror's project:
https://www.buydisplay.com/2-8-inch-240x320-ips-tft-lcd-display-panel-optional-touch-panel-wide-view

This is a reviewed candidate, **not a fabrication-qualified selection**. No A3
dimensions or pin functions are inferred from A2. Its supplier stock is unverified.

## Verified body and interface

| Item | Exact A2 manufacturer specification |
| --- | --- |
| Landscape body | 69.3 × 50.2 mm;2.8 mm no-touch thickness |
| Landscape active area | 57.6 × 43.2 mm;320×240 after controller rotation |
| Active centre relative to body | (−3.45,−0.30) mm in the shown90°CCW front view |
| Controller | ILI9341 |
| Connector | 50 contacts,0.5mm pitch;top-contact ZIF recommended for the unfolded tail |
| Terminal thickness | 0.30±0.03mm, including stiffener;not a bend-radius specification |
| Contacts | 0.35±0.03mm conductor width;3.5 mm exposed length;25.5±0.1mm tail width |
| FPC extension | 26.7±0.5mm beyond the body in the flat drawing |
| Final front exit | Right after90°CCW rotation of the native portrait assembly |
| Chosen candidate electrical mode | Four-wire 8-bit Serial Interface I;IM3..IM0=0110 |
| Power | VCI2.5–3.3V,VDDI1.65–3.3V;existing2.8V regulator meets these limits |
| Backlight | Common cathode pin 1;four separate anodes pins 2–5;70mA typical/80mA maximum total |
| LED voltage | At80mA,3.2V typical/3.4V maximum |

All50 panel pin functions were checked and are recorded in `panel-pin-review.csv`.
**No final J7 contact mapping is assigned.** It must follow the actual socket,
contact face, row order and physically qualified assembly, not the old 51-minus-n
or abandoned2.3-inch mapping. The A2 drawing prints the inconsistent expression
P0.5*(40−1)=24.50, while its50-contact table and24.50mm span agree with 50 contacts;
this drawing typo is retained, not silently rewritten.

The existing backlight wiring assumes one common anode and four separate sink
returns. Connecting the A2 to it as-is would reverse these roles. Revised wiring
and current regulation must be reviewed. Reusing the TPS60230 with an aggregated
sink return is an engineering option that still needs qualification; no claim
that merely retaining its 62.4mA nominal setting proves compatibility is made.

## Actual mechanical findings

Dimensions50×65mm/60×75mm can be viewed as65×50mm/75×60mm in the finished landscape
orientation without changing their sizes. The body is centred on the PCB as
requested. `mechanical-review.pdf` and `.png` show the 197-point native PCB outline,
all 125 actual native courtyards, current J7, body, active area and RF keepout.

- Body covers77.308% of a75×60mm front face;active pixels cover55.296%.
- Body covers100% of the PCB projection. Body/PCB area ratio is107.042%, a
  different metric from overlap coverage.
- PCB overhang:left/right2.15mm each;top/bottom0.10mm each in the landscape view.
- A recentered75×60mm case gives outer-body margins2.85mm left/right and 4.90mm
  top/bottom. With existing 0.8 mm walls, inner margins are2.05mm and 4.10mm.
- The actual existing enclosure is offset3.5 mm along the native long axis.
  The centred panel crosses its outer right wall by0.65mm and its inner wall by
  1.45mm. Recentring that case changes the fit of the existing antenna/module.
- Body overlaps the actual 20 × 8mm antenna keepout by**59.5mm²**. Moving only J7
  does not resolve this. RF placement must change, or a different mechanical
  envelope/qualified display must be selected.
- Leaving the existing RF strip along the LCD long edge requires at least
  69.3+8+1.6=78.9mm case length before any extra clearance. This is a dimensional
  bound, not an approved enclosure redesign or a full RF design rule.
- Flat tail ends at frontX61.35mm, overrunning the recentered case's inner right
  wall by24.65mm. A return path is necessary. Its final bend and socket position
  cannot be derived from the body rectangle alone.

The full PDF gives **no numerical minimum FPC bend radius**. It warns against
forcibly bending/pulling cables. Terminal0.30mm thickness is not the bendable-span
thickness. The dotted tail in the overlay is explicitly only a dimensional
envelope: neck offset/profile, fold, latch access and3D mating are unqualified.
No guessed neck or bend is presented as accurate mechanical geometry.

Final J7 coordinates/rotation: **unassigned**. Components moved: **none**.
Actual board schematic/routing changes: **none**. The1.0 mm four-layer 50×65mm PCB,
previously accepted physical connections and all authentic solver caches remain
unchanged. The user allows affected-part moves, but this does not supply missing
manufacturer flex limits or qualify a guessed mating arrangement.

## Genuine U14 import diagnosis

Supported `tsci import C7848 --jlcpcb --use-exact-footprint --download` now exits 0
and downloads the real assets. OBJ and STEP bytes equal the existing genuine
board assets. The resulting model origin equals the original, resolving the
incorrect 4.05 mm origin from the earlier no-download trial. All20 numbered pad
centres match the accepted board within 0.000134537mm. Native pin 1 metadata and
supplier map now both say`bottomside_left`.

The canonical unrouted coupon build exits 0, but its exact 20 pill pads produce
**zero native solder-paste records**. This is a real fabrication defect, not a
passed stencil check. Replacing the current import would introduce20 additional
missing paste records on top of the existing 32. The candidate is therefore not
applied to the active board. No imported definition or generated JSON is patched.
Exact import source, native coupon, SVG, resource outcomes and qualification
receipt are under`u14-canonical-import/`.

## Preserved work and validation

Unaccepted2.3-inch changes and their18-courtyard-error placement capture are
preserved under`../display023-routing-2026-10-07/`. Its later0-intersection v4
proposal was never a full placement/DRC pass. Staged source is archived before
restoring the exact publicHEAD board source. Cloud setup rerun receipts are also
preserved there before restoring tracked smoke artifacts.

Cloud setup has already completed its frozen installation and supervisor smoke
checks. New helper TypeScript/formatting and 5 geometry regressions pass. These
check courtyard transforms and rejection of unsupported/incomplete geometry;
they do not prove a routed PCB or mechanical mating. A fresh unchanged-board
physical audit exits 1:0 measured shorts,0 measured geometry violations and 12
physically open nets. It is not a full DRC/connectivity pass. Accepted native still has 50 native
open-port errors and 12 physically open nets; J3 unassigned outers are excluded.
Old schema, paste, width, stock, programmer and Gerber blockers remain.

The cloud draft preserves all 17 prior custom destinations and adds
`*.challenges.cloudflare.com` and`modelcdn.tscircuit.com`. Startup instructions
now prioritize this new 2.8-inch request. Saving is not runtime application or
environment publication. Model CDN currently responds; the challenge subdomain
remains blocked. Apply the saved network settings to unblock normal manufacturer
browsing. No secrets were requested or stored.

## Remaining gates and proper continuation

1. Obtain the exact preferred A3 manufacturer drawing through normal allowed
   browsing, or fully qualify the exact A2 variant instead. Verify tail constraints
   and material/minimum bend radius;do not assume these from a similar panel.
2. Resolve centred-body/enclosure/RF fit and a natural side-entry return path,
   contact face/pin 1 row order, latch access and Z clearances. Only then set final
   J7/U14/C42/C43 and interfering-part poses from that mechanical result.
3. Correct the canonical pill-paste generator before accepting the genuine U14
   replacement;retain the unmodified import and genuine CAD assets.
4. Implement the corresponding schematic/backlight changes, validate native
   unrouted placement, then replace affected real copper and preserve prior
   numbered-terminal connectivity. Run the full unchanged manufacturing checks.

This review does not fulfil the requested implementation. Dependent placement,
contact fanout, routing and fabrication remain blocked. No new board version,
new tscircuit native preview, order or physical working-hardware claim is made.
