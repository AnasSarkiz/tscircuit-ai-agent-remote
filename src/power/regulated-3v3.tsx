import { DFE201612E_R47M_P2 } from "../../imports/DFE201612E_R47M_P2/DFE201612E_R47M_P2"
import { GRM188R61A106ME69D } from "../../imports/GRM188R61A106ME69D/GRM188R61A106ME69D"
import { GRM188R61A226ME15D } from "../../imports/GRM188R61A226ME15D/GRM188R61A226ME15D"
import { RC0603FR_07100KL } from "../../imports/RC0603FR_07100KL/RC0603FR_07100KL"
import { RC0603FR_07560KL } from "../../imports/RC0603FR_07560KL/RC0603FR_07560KL"
import { TPS63802DLAR } from "../../imports/TPS63802DLAR/TPS63802DLAR"

// Draft application circuit: TI SLVSEU9D sections 7 and 10.2.
// Review coordinates belong to the isolated fixture, not the handheld placement.
export function Regulated3v3ReviewSheet() {
  return (
    <schematicsheet
      name="regulated-3v3-review"
      displayName="AI Remote A0 — 3.3 V buck-boost review (unrouted)"
      sheetIndex={1}
      sheetSize="A4"
    >
      <group name="regulator-review" schX={0} schY={0} schLayout={{ layoutMode: "relative" }}>
        <net name="GND" isGroundNet />
        <net name="VSYS" isPowerNet />
        <net name="V3V3" isPowerNet />
        <net name="REG_FB" />
        <net name="REG_PG" />
        <TPS63802DLAR name="U2" layer="top" pcbX={0} pcbY={0} schX={0} schY={0} />
        <DFE201612E_R47M_P2 name="L1" layer="top" pcbX={4} pcbY={0} schX={0} schY={4} />
        <GRM188R61A106ME69D
          name="C4"
          layer="top"
          pcbX={-4}
          pcbY={0}
          schX={-6}
          schY={0}
          schRotation={-90}
        />
        <GRM188R61A226ME15D
          name="C5"
          layer="top"
          pcbX={4}
          pcbY={-4}
          schX={6}
          schY={0}
          schRotation={-90}
        />
        <RC0603FR_07560KL
          name="R5"
          layer="top"
          pcbX={-4}
          pcbY={-4}
          schX={6}
          schY={-4}
          schRotation={-90}
        />
        <RC0603FR_07100KL
          name="R6"
          layer="top"
          pcbX={0}
          pcbY={-4}
          schX={6}
          schY={-7}
          schRotation={-90}
        />
        <RC0603FR_07100KL
          name="R7"
          layer="top"
          pcbX={-4}
          pcbY={4}
          schX={-6}
          schY={4}
          schRotation={-90}
        />
        <trace from="U2.pin10" to="net.VSYS" />
        <trace from="U2.pin1" to="net.VSYS" />
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
