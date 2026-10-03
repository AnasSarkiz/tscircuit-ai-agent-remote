# Haptic circuit review — A0, 2026-10-03

The motor and its placement remain blocked. The independent regulator/flyback
application is `src/haptics/haptic-driver-review.tsx`; the native A4 fixture is
`evidence/haptic-review-2026-10-03/driver.circuit.tsx`. It is an unrouted review,
not an integrated handheld circuit or fabrication approval.

JLC C2942347 / LEADER LCM0720A3176F imported through the supported workflow,
without edits. Its manufacturer Rev0 drawing (2021-10-22) specifies rated3V,
operating2.7–3.3V, rated current <=85mA, starting current <=120mA at the minimum
starting voltage, and starting voltage <=2.5V. These do not establish a bound
on stall current at3.045V across temperature. Case diameter7±0.1mm, foam8mm;
case2.1±0.1mm plus0.3mm foam and0.15mm bottom tape give a provisional2.65mm
maximum stack. Required assembler support/fixture and mounting/reflow remain
unqualified. [Supplier](https://jlcpcb.com/partdetail/LEADER-0720_FPCB/C2942347),
[manufacturer drawing](https://jlcpcb.com/api/file/downloadByFileSystemAccessId/8590221675024584704).

**B-014:** the imported courtyard covers the FPC tail and excludes much of the
motor body at x=-9.017mm. A real imported resistor deliberately placed at that
top-side body center returns placement0 errors/0 warnings; inspected native3D
shows it hidden beneath the top-side motor. The fix chat confirmed a converter
body-bounds/courtyard defect: raw EasyEDA includes the body. The exact native
OBJ has3.85mm total height, a separate unresolved model qualification concern.
The alternate C2895081 / LCM0720A3134F has no importable EasyEDA library and
is not a verified replacement. Evidence, raw library, model bounds, drawings
and overlap reproduction are saved; no imported definition was patched.

The driver review uses genuine imported C963429 / TI TPS7A2030PDBVR,
C20917 / AOS AO3400A, and C2480 / MDD SS14. TI's DBV pin drawing is
1IN/2GND/3EN/4NC/5OUT; generated physical pads retain those numbers. Supply is
VSYS, output VMOTOR. Three-volt accuracy±1.5% requires VIN>=3.3V and load>=1mA;
then2.955–3.045V fits the motor's operating range. A1k bleed gives approximately
3mA only when enabled. Do not infer nominal-output accuracy from the DBV
145mV maximum dropout specification: that uses output=95% of nominal at300mA.
Battery/system cutoff, trace drops and transient margins remain unresolved.
[TI TPS7A20](https://www.ti.com/lit/ds/symlink/tps7a20.pdf).

MCU_HAPTIC_ENABLE drives regulator EN and the NMOS gate through100Ω; external
100k EN and10k gate pull-downs retain default-off paths. NMOS pins1/2/3 are
gate/source/drain. Its drain is HAPTIC_N, source grounded. SS14 pin1/cathode
connects VMOTOR; pin2/anode connects HAPTIC_N. A future motor would connect
between these nets, closing the flyback loop rather than forcing regulator
OUT negative. The motor is absent from this review because B-014 is unresolved.
Capacitors are10µF at IN,22µF at OUT and100nF across the prospective motor nets;
actual DC-biased capacitance, EMI and switch-off waveforms remain unqualified.
[AOS AO3400A](https://www.aosmd.com/pdfs/datasheet/AO3400A.pdf),
[MDD-authored SS14 Rev2025A5, supplier mirror](https://datasheet.lcsc.com/datasheet/pdf/9977bb85cd7e349115b7bcb7054cfa0d.pdf?productCode=C2480).

Native network-enabled build and all five required connectivity/placement checks
exit0 for the isolated fixture. The sandbox build's supplier-network warnings
disappear when rerun with network access. Final output:10 top-side components,
24 pads/24 paste shapes,zero PCB traces/vias/errors; PCB/A4 images inspected.
Two independent manufacturer physical-pin/polarity tests pass. Missing NMOS
reference text (B-008) and imported role metadata warnings (B-007) remain;
reference-prefix advisory comes from the importer using chip for a MOSFET.
No import warning was hidden.12 strict native schema failures remain B-010;
snapshot acceptance withheld while the schematic reference is missing.
Canonical suite19pass/1fail,177assertions; existing full-native-schema test fails.
TypeScript passes. No whole-board gate or physical test is completed here.
