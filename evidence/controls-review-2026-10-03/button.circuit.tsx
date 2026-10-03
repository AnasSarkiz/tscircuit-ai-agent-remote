import { EVQPUC02K } from "../../imports/EVQPUC02K/EVQPUC02K"

export default () => (
  <board width={20} height={20} routingDisabled>
    <schematicsheet name="hold-button-import-review" sheetSize="A4" sheetIndex={1}>
      <EVQPUC02K name="SW1" layer="top" pcbX={0} pcbY={0} schX={0} schY={0} />
    </schematicsheet>
  </board>
)
