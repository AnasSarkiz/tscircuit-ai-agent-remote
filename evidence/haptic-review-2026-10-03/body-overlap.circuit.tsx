import { LCM0720A3176F } from "../../imports/LCM0720A3176F"
import { RC0603FR_0710KL } from "../../imports/RC0603FR_0710KL/RC0603FR_0710KL"
// Deliberate supplier-envelope reproduction: resistor occupies drawn motor body.
export default () => (
  <board width={40} height={24} routingDisabled>
    <schematicsheet name="haptic-body-overlap" sheetSize="A4" sheetIndex={1} displayName="Haptic supplier-envelope reproduction — not valid placement">
      <LCM0720A3176F name="M1" layer="top" pcbX={0} pcbY={0} schX={0} schY={0} />
      <RC0603FR_0710KL name="R91" layer="top" pcbX={-9.017} pcbY={0} schX={-8} schY={0} />
    </schematicsheet>
  </board>
)
