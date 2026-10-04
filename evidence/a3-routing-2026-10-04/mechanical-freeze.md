# A3 prototype placement freeze

**DISPLAY / FPC PLACEMENT FROZEN FOR PROTOTYPE ROUTING. A3 PLACEMENT FROZEN FOR ROUTING.** This freezes a reviewed assembly study, not enclosure tooling or verified physical fit. Native board GLB plus actual supplier model dimensions were inspected in perspective and side views in `mechanical.html`; this is a 3D assembly envelope study, not an electronic component definition. Native models remain unchanged. Five required checks: netlist/pin specification/source/schematic placement exit0; final placement exit0 with zero errors and three reviewed insertion-direction warnings. First placement checker also detected a 0.057 mm U14/C40 clearance conflict; C40 was moved 0.3 mm and passive orientations corrected before the final pass. Exact placement/source/GLB hashes are saved in placement-freeze-manifest.json. Copper is still absent at this checkpoint.

## Enclosure and display

PCB50x65x1.6 unchanged. Maximum external study60x75x14.82 mm: X[-30,30],Y[-34,41],Z[-7.97,6.85]. Conditional walls0.8 mm,back0.6 mm and frontcover/bezel0.6 mm. These are design allowances, not a mechanically qualified case. Preference57–58x72–73x13–14 is not currently proven; maximum is needed for the present display fold.

HS20HS072RX landscape body51.8x36.2x2.05(+/-0.05) at(0,-7.3). RearZ4.15;frontnominal6.20/max6.25. Actual tallest under-glass native part J6 top3.71 leaves0.44 nominal gap. J7 top2.81;U25 top2.449. Taller J3/J4/J8 (top6.30) are all beyond glass topY10.8. LCD is supported by bezel rails; neither FPC nor parts carry the glass load. Active area40.8x30.6; exact manufacturer active-area offsets remain represented by its drawing, approximate note rectangle is not a machining datum.

C11051 bottom-contact connector rotation90 faces left, mouthX-15.15236. Contact plane~Z1.90 from supplier section. FPC glass departure~Z5.10,0.5 mm outward straight, then a cylindrical180degree1.6 mm radius fold aroundY, minimumX-28.0. InsidecaseleftwallX-29.2 allows1.2 mm nominal gap. Pre-cut L tail is retained: horizontal root atY-14.9,vertical legX-17.5 toY-7.73, terminal tongue6.5 mm wide endingX-11.22655. 20.7(+/-0.5) mm drawing projection minus1 mm straight reversal and pi*1.6 gives3.926 mm insertion versus4 mm supplier section. Last5 mm stiffener remains straight; no bent stiffener or in-plane bend invented. Root offset and undimensioned strip shape are scaled drawing study assumptions, NOT manufacturer toleranced dimensions. Radius is a design target, not a supplier-certified minimum. Physical flex, latch access and assembly trial must confirm this before fabrication approval.

Native CAD intersection check across folded strip/tongue: only C25 lies below free flex; top1.60 vsflexlower1.84 =>0.24 mm nominal clearance. U7 moved away from flex to(-17,-19). J7 contact overlap is intentional. Assemble LCD/FPC before closing the bezel; removal requires opening case and lifting display while releasing C11051 slider. Internal J6 service plug must be fitted before display installation or accessed after removing glass. No claim of external service access.

The folded contact face points toward PCB. LCD terminal1 is at the north edge, corresponding to native J7 pin12; LCDn mates J7(13-n). Board wiring is reversed accordingly, including NC at J7pin6 and power/LED polarity. Imported connector definition is unchanged. Original exact display and connector drawings are retained under references/routing-a2 and evidence/display-review.

## Battery, RF and acoustic paths

AKY2945/LP523450 rotated behindPCB:52.5x35 at(0,-8),XY[-26.25,26.25]x[-25.5,9.5],topZ-1.10;5.7 mm nominal,conditional10% swelling6.27 givesbottom-7.37. PCBbottom-.8 =>0.30 mm nominal separation; no compressive mounting. Real pack thickness, foam, wiring and swelling policy remain physical qualification. NTC centre confirmed; outer numbered contacts still unproven after final authoritative drawing review. J3pin1/pin3 remain deliberately OPEN.

U1 antenna region dimensioned6 mm antennaX[-21,-3],Y[32.675,38.675]. All-layer keepoutX[-22,-2],Y[31.675,39.675], excludes only actual U1. Antenna native modeltopY38.675;internalcaseceiling40.2 =>1.525 mm nominal plastic/air margin. Glass/FPC topY10.8 gives>=21.875 mm longitudinal separation; packtop9.5 gives>=23.175 mm. Keepout is clear through the entire enclosure height. Metal speaker/motor envelopes and right-side wiring remainX>=14, at least17 mm horizontally from antenna. No battery/screw/cable crosses antenna exclusion.

Microphones now(-16.4,-28.8) and(21,-29), below packbottom-25.5. Rear acoustic corridors lead to case bottom without traversing pack;0.6 mm native acoustic holes unchanged. Acoustic channel/gasket design and noise/isolation are untested. Slim external speaker15x11x3 study at(19.5,18) fits rear pocket; PUI AS01508AO-WP-R8ohm/.7W is a manufacturer-backed candidate, exact JLC search empty, procurement acceptance remains OPEN. LEADER LCM0720A3176F7x7x2.65 envelope at(19.5,31), wire mounted, remains clear of antenna and speaker. No external part was fabricated as a PCB component.

J4/J8 mouths face+X with actual bodyfront22.5. Conservative3.4 mm mated housing extension plus2.5 mm wire-turn radius reaches28.4 vsinsidewall29.2 (0.8 nominal gap). JST side-entry assembled drawing gives9.6 mm totalprojection;3.4 mm here is a conservative study reserve, not claimed exact outer overhang. Plug insertion/removal is performed with the unscrewed board outsidecase; leaving in-case axial withdrawal space is not assumed. J3mouth+Y,top25.525,wire path right of antenna. USBshell reachesY-33.775 withinexternalbottom-34 and requires a real shell opening throughwall. TALK plastic actuator volume is modeled fromtopedge to actualtop push switch at(19,30.4); real force/travel/lever/case tolerances remain physical qualification.

## Mounts

Nylon M2 head envelope4 mm diameter,1.5 mm height abovePCB; plasticboss6 mm diameter. No metallic fastening near antenna. All-layer native radius3 keepouts preserved; actual routedcopper still needs audit.

| Hole | X mm | Y mm | NPTH drill mm | Keepout diameter mm | Hole edge to straight PCB edge mm | RF status |
|---|---:|---:|---:|---:|---:|---|
| M1 | 2 | 13 | 2.2 | 6 | 18.4 | Outside antenna; bossleft-1 vs modulecourtyardright-2.25 gives1.25 nominal gap |
| M2 | -21.5 | -29.5 | 2.2 | 6 | 1.9 | Far below antenna; nearest roundedcorner arc gives1.94 mm; bottomstraight governs1.90 mm |

M1bossbottomY10 vspacktop9.5 gives0.5 mm nominal gap; nylonheadtop2.30 vsglassrear4.15 gap1.85. M2bossupperY-26.5 vspackbottom-25.5 gap1.0; glassbottom-25.4 gap1.1. Boss/screw hole registration, torque and tolerance stack need physical test; two-point case stiffness not claimed validated.

### Keepout amendment before first successful copper

Espressif figure11-1 (saved esp32-antenna.png) distinguishes6 mm antenna area from7.49 mm pad-centre offset. Earlier oversized RF estimate overlapped U1 ground lands. Native keepout corrected to actual6 mm antenna+1 mm longitudinal margin, without moving any component or reducing manufacturer antenna exclusion. Antenna underside beginsY32.675,0.175 mm beyond PCBedge32.5. Original failed routing artifacts and original freeze manifest preserved; amendment changes only keepout/note metadata and routing settings. No successful copper existed at amendment.
