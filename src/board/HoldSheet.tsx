import { place } from "./placement"
import { SN74LVC1G17DBVR } from "../../imports/SN74LVC1G17DBVR/SN74LVC1G17DBVR"
import { RC0603FR_0710KL } from "../../imports/RC0603FR_0710KL/RC0603FR_0710KL"
import { A_0603WAF1001T5E } from "../../imports/A_0603WAF1001T5E/A_0603WAF1001T5E"
import { GRM188R71C104KA01D } from "../../imports/GRM188R71C104KA01D/GRM188R71C104KA01D"

export function HoldSheet() {
  return (
    <schematicsheet
      name="hold-readback-review"
      displayName="AI Remote A1 - Top HOLD control"
      sheetSize="A4"
      sheetIndex={8}
    >
      <group
        name="hold-readback-review-group"
        schLayout={{ layoutMode: "relative" }}
        pcbStyle={{ silkscreenFontSize: 1 }}
      >
        <SN74LVC1G17DBVR name="U26" {...place("U26")} schX={0} schY={0} />
        <RC0603FR_0710KL name="R99" {...place("R99")} schX={-5} schY={-3} schRotation={-90} />
        <A_0603WAF1001T5E name="R100" {...place("R100")} schX={5} schY={0} />
        <GRM188R71C104KA01D name="C78" {...place("C78")} schX={-5} schY={3} schRotation={-90} />
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
