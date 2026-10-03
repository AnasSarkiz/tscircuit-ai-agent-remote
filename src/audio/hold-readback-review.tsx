import { SN74LVC1G17DBVR } from "../../imports/SN74LVC1G17DBVR/SN74LVC1G17DBVR"
import { RC0603FR_0710KL } from "../../imports/RC0603FR_0710KL/RC0603FR_0710KL"
import { A_0603WAF1001T5E } from "../../imports/A_0603WAF1001T5E/A_0603WAF1001T5E"
import { GRM188R71C104KA01D } from "../../imports/GRM188R71C104KA01D/GRM188R71C104KA01D"

// Independent MCU readback candidate; the switch and microphone supply are not integrated.
// A Schmitt input accommodates slow button transitions. Its output is a separate MCU net.
// Release leakage, rail ramps, contact bounce and microphone turn-off timing remain open.
export function HoldReadbackReviewSheet() {
  return (
    <schematicsheet
      name="hold-readback-review"
      displayName="AI Remote A0 — hardware hold readback (unrouted candidate)"
      sheetSize="A4"
      sheetIndex={1}
    >
      <group
        name="hold-readback-review-group"
        schLayout={{ layoutMode: "relative" }}
        pcbStyle={{ silkscreenFontSize: 1 }}
      >
        <net name="GND" isGroundNet />
        <net name="V3V3" isPowerNet />
        <net name="HOLD_HARDWARE" />
        <net name="HOLD_BUFFER_OUT" />
        <net name="MCU_HOLD_READ" />
        <SN74LVC1G17DBVR name="U26" layer="top" pcbX={0} pcbY={0} schX={0} schY={0} />
        <RC0603FR_0710KL
          name="R99"
          layer="top"
          pcbX={-6}
          pcbY={0}
          schX={-5}
          schY={-3}
          schRotation={-90}
        />
        <A_0603WAF1001T5E name="R100" layer="top" pcbX={6} pcbY={0} schX={5} schY={0} />
        <GRM188R71C104KA01D
          name="C78"
          layer="top"
          pcbX={0}
          pcbY={5}
          schX={-5}
          schY={3}
          schRotation={-90}
        />
        <trace from="U26.pin2" to="net.HOLD_HARDWARE" />
        <trace from="U26.pin3" to="net.GND" />
        <trace from="U26.pin4" to="net.HOLD_BUFFER_OUT" />
        <trace from="U26.pin5" to="net.V3V3" />
        <trace from="R99.pin1" to="net.HOLD_HARDWARE" />
        <trace from="R99.pin2" to="net.GND" />
        <trace from="R100.pin1" to="net.HOLD_BUFFER_OUT" />
        <trace from="R100.pin2" to="net.MCU_HOLD_READ" />
        <trace from="C78.pin1" to="net.V3V3" />
        <trace from="C78.pin2" to="net.GND" />
      </group>
    </schematicsheet>
  )
}
