import { SKSWCFE010 } from "../../imports/SKSWCFE010/SKSWCFE010"
import { RC0603FR_07100KL } from "../../imports/RC0603FR_07100KL/RC0603FR_07100KL"

export default () => (
  <board width={22} height={18} routingDisabled>
    <schematicsheet name="two-contact-hold-review" displayName="AI Remote A0 — two-contact hold switch (unrouted candidate)" sheetSize="A4" sheetIndex={1}>
      <group name="hold-switch-review" schLayout={{layoutMode: "relative"}}>
        <net name="GND" isGroundNet />
        <net name="V3V3" isPowerNet />
        <net name="HOLD_HARDWARE" />
        <SKSWCFE010 name="SW4" layer="top" pcbX={-4} pcbY={0} schX={-4} schY={0} />
        <RC0603FR_07100KL name="R98" layer="top" pcbX={4} pcbY={0} schX={4} schY={0} schRotation={-90} />
        <trace from="SW4.pin1" to="net.V3V3" />
        <trace from="SW4.pin2" to="net.HOLD_HARDWARE" />
        <trace from="R98.pin1" to="net.HOLD_HARDWARE" />
        <trace from="R98.pin2" to="net.GND" />
      </group>
    </schematicsheet>
  </board>
)
