# Uploaded ER-TFT026-1 primary datasheet review — 2026-10-07

The user supplied the exact 24-page EastRising / BuyDisplay ER-TFT026-1
datasheet, revision 3.0 dated 2021-12-22. Its bytes are preserved in this
directory: SHA-256
`1f479da350bf47fc250f9abd709710f8c6ea28ec0d5d11c56ffa174d505493ae`.
The document is an engineering reference, not an instruction source.

This is the 2.6-inch 240×320 ILI9341 bare panel without touch. Pages 5, 6, 9,
10 and 11 were inspected. The no-touch outline drawing is revision 2.0 from
2017-10-15, within the revision 3.0 document. It specifies a 46×64×2.55 mm body,
a 26.70±0.5 mm bottom flex extension, 50 contacts at 0.5 mm pitch, a 25.50 mm
terminal width and 0.30±0.03 mm terminal thickness. Pin 1 is on the right in
the front/conductor view and on the left in the rear/stiffener view. The
manufacturer calls for a top-contact socket.

The existing J7 is the genuine AFC07-S50ECA-00/C262650 upper-contact import.
Its primary drawing is `references/a3/buydisplay/AFC07-S50ECA-00.pdf`.
Pitch, nominal tail width and nominal thickness agree. The panel conductor
width is 0.35±0.03 mm, while the connector's recommended FPC drawing specifies
0.30±0.03 mm; matching nominal pitch alone does not qualify the full mating
tolerance. J7's actual contact row is vertical, pin 1 south and pin 50 north,
with a measured 24.496522 mm contact span. The required fold and contact
correspondence have not been qualified.

All 50 panel pin assignments agree with the native named nets under the
existing provisional mapping, panel pin n → J7 pin 51−n. The independent table
is in `display-pin-audit.csv` and `display-primary-audit.json`. Five existing
display tests pass with 95 assertions. Those checks do not establish that
the physical panel mates according to that hypothesis.

The selected interface is four-wire eight-bit serial II, IM3…IM0=1110. The
existing 2.8 V VLCD lies within the specified VCI and VDDI operating ranges.
The backlight has four parallel LED chips, 70 mA typical and 80 mA maximum
total forward current. The datasheet specifies no minimum forward current;
70 mA must not be treated as a minimum. Existing R102=10 kΩ gives approximately
62.4 mA nominal total through the four TPS60230 sinks. Lower nominal brightness
is not by itself a datasheet violation. Actual brightness, startup and thermal
performance remain untested.

The portrait active-area centre is 2.90 mm above the body centre, using the
2.70 mm top margin and 52.80 mm active height. At the historical A7 body
centre (−5.8,−0.8), its derived active-area centre is (−5.8,2.1) mm. The old A7
visualization used y=0 for that centre; it should not be treated as a qualified
panel/window model. The historical artifact is preserved.

The user's subsequent decision rejects this bottom-tail panel for the present
right-side connector and requests a replacement. See
`../display-replacement-review-2026-10-07/review.md`. This review establishes
that the old primary PDF is now available; it does not approve the rejected
display or enable its contact-dependent routing.

No board source, genuine import, solver output or native copper changed. The
canonical native SHA-256 remains
`35c5fb2bfc870daf11b5f5e30847f1e5a86fd886ebb8ef11fc3cf6e88e77e63d`,
with 50 native open-port errors and unresolved fabrication gates. No order or
physical test occurred.
