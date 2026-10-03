import { TPS7A2030PDBVR } from "../../imports/TPS7A2030PDBVR"
import { GRM188R61A226ME15D } from "../../imports/GRM188R61A226ME15D/GRM188R61A226ME15D"
export default () => (
  <board width={24} height={20} routingDisabled>
    <schematicsheet name="haptic-ldo-pin-review" sheetSize="A4" sheetIndex={1} displayName="Haptic regulator pin qualification — unrouted">
      <net name="GND" isGroundNet /><net name="VSYS" isPowerNet /><net name="VMOTOR" isPowerNet />
      <TPS7A2030PDBVR name="U22" layer="top" pcbX={0} pcbY={0} schX={0} schY={0} />
      <GRM188R61A226ME15D name="C71" layer="top" pcbX={6} pcbY={0} schX={6} schY={0} schRotation={-90} />
      <trace from="U22.pin1" to="net.VSYS" /><trace from="U22.pin2" to="net.GND" />
      <trace from="U22.pin3" to="net.VSYS" /><trace from="U22.pin5" to="net.VMOTOR" />
      <trace from="C71.pin1" to="net.VMOTOR" /><trace from="C71.pin2" to="net.GND" />
    </schematicsheet>
  </board>
)
