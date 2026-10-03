import { LD_SM_430 } from "./imports/LD_SM_430/LD_SM_430"

// Import/mechanical diagnostic only. The third mounting land's electrical role
// and complete motor application are not qualified; no motor net is authored.
export default () => (
  <board width={20} height={20} routingDisabled>
    <schematicsheet
      name="alternate-haptic-import-review"
      displayName="C41348533 alternate haptic motor — import review only"
      sheetIndex={1}
      sheetSize="A4"
    >
      <LD_SM_430 name="M2" layer="top" />
    </schematicsheet>
  </board>
)
