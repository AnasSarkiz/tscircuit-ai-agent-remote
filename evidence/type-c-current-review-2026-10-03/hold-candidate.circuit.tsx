import { EVQ_P4HB3B } from "../../imports/EVQ_P4HB3B/EVQ_P4HB3B"
import { RC0603FR_0710KL } from "../../imports/RC0603FR_0710KL/RC0603FR_0710KL"
// Diagnostic only: candidate footprint has an unresolved mechanical discrepancy.
export default () => (
  <board width={24} height={20} routingDisabled>
    <schematicsheet name="hold-candidate" sheetSize="A4" sheetIndex={1} displayName="AI Remote A0 — unqualified hold candidate">
      <group name="hold-candidate-group" schLayout={{layoutMode:"relative"}}>
        <net name="V3V3" isPowerNet />
        <net name="GND" isGroundNet />
        <net name="HOLD_RAW" />
        <EVQ_P4HB3B name="SW1" layer="top" pcbX={0} pcbY={-7} schX={0} schY={0} />
        <RC0603FR_0710KL name="R77" layer="top" pcbX={6} pcbY={2} schX={5} schY={0} schRotation={-90} />
        <trace from="SW1.pin1" to="net.V3V3" />
        <trace from="SW1.pin2" to="net.HOLD_RAW" />
        <trace from="SW1.pin3" to="net.GND" />
        <trace from="SW1.pin4" to="net.GND" />
        <trace from="R77.pin1" to="net.HOLD_RAW" />
        <trace from="R77.pin2" to="net.GND" />
      </group>
    </schematicsheet>
  </board>
)
