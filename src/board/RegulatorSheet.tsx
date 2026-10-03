import { place } from "./placement"
import { DFE201612E_R47M_P2 } from "../../imports/DFE201612E_R47M_P2/DFE201612E_R47M_P2"
import { GRM188R61A106ME69D } from "../../imports/GRM188R61A106ME69D/GRM188R61A106ME69D"
import { GRM188R61A226ME15D } from "../../imports/GRM188R61A226ME15D/GRM188R61A226ME15D"
import { RC0603FR_07100KL } from "../../imports/RC0603FR_07100KL/RC0603FR_07100KL"
import { RC0603FR_0751K1L } from "../../imports/RC0603FR_0751K1L/RC0603FR_0751K1L"
import { RC0603FR_079K1L } from "../../imports/RC0603FR_079K1L/RC0603FR_079K1L"
import { TPS63802DLAR } from "../../imports/TPS63802DLAR/TPS63802DLAR"

export function RegulatorSheet() {
  return (
    <schematicsheet
      name="regulated-3v3-review"
      displayName="AI Remote A1 - 3.3 V buck boost"
      sheetIndex={3}
      sheetSize="A4"
    >
      <group name="regulator-review" schX={0} schY={0} schLayout={{ layoutMode: "relative" }}>
        <TPS63802DLAR name="U2" {...place("U2")} schX={0} schY={0} />
        <DFE201612E_R47M_P2 name="L1" {...place("L1")} schX={0} schY={4} />
        <GRM188R61A106ME69D name="C4" {...place("C4")} schX={-6} schY={0} schRotation={-90} />
        <GRM188R61A226ME15D name="C5" {...place("C5")} schX={6} schY={0} schRotation={-90} />
        <RC0603FR_0751K1L name="R5" {...place("R5")} schX={6} schY={-4} schRotation={-90} />
        <RC0603FR_079K1L name="R6" {...place("R6")} schX={6} schY={-7} schRotation={-90} />
        <RC0603FR_07100KL name="R7" {...place("R7")} schX={-6} schY={4} schRotation={-90} />
        <trace from="U2.pin10" to="net.VSYS" />
        <trace from="U2.pin1" to="net.BUCK_ENABLE" />
        <trace from="U2.pin2" to="net.GND" />
        <trace from="U2.pin3" to="net.GND" />
        <trace from="U2.pin8" to="net.GND" />
        <trace name="REG_L1" from="U2.pin9" to="L1.pin1" />
        <trace name="REG_L2" from="U2.pin7" to="L1.pin2" />
        <trace from="U2.pin6" to="net.V3V3" />
        <trace from="C4.pin1" to="net.VSYS" />
        <trace from="C4.pin2" to="net.GND" />
        <trace from="C5.pin1" to="net.V3V3" />
        <trace from="C5.pin2" to="net.GND" />
        <trace from="R5.pin1" to="net.V3V3" />
        <trace from="R5.pin2" to="net.REG_FB" />
        <trace from="R6.pin1" to="net.REG_FB" />
        <trace from="R6.pin2" to="net.GND" />
        <trace from="U2.pin4" to="net.REG_FB" />
        <trace from="R7.pin1" to="net.V3V3" />
        <trace from="R7.pin2" to="net.REG_PG" />
        <trace from="U2.pin5" to="net.REG_PG" />
      </group>
    </schematicsheet>
  )
}
