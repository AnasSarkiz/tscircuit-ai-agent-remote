import { TPS3808G33DBVR } from "../../imports/TPS3808G33DBVR/TPS3808G33DBVR"
import { RC0603FR_07470KL } from "../../imports/RC0603FR_07470KL/RC0603FR_07470KL"
import { GRM188R71C104KA01D } from "../../imports/GRM188R71C104KA01D/GRM188R71C104KA01D"

// Independent buck-enable application review, not a complete power path.
// PACK_BAT means the actual charger BAT terminal. It is not a fake battery.
// Battery-presence detection, NTC/charging policy and transient timing are open.
export function BatteryReadyReviewSheet() {
  return (
    <schematicsheet
      name="battery-ready-review"
      displayName="AI Remote A0 — battery readiness for buck enable (unrouted candidate)"
      sheetIndex={1}
      sheetSize="A4"
    >
      <group name="battery-ready-review-group" schLayout={{ layoutMode: "relative" }}>
        <net name="GND" isGroundNet />
        <net name="VSYS" isPowerNet />
        <net name="PACK_BAT" isPowerNet />
        <net name="BUCK_ENABLE" />
        <TPS3808G33DBVR name="U25" layer="top" pcbX={0} pcbY={0} schX={0} schY={4} />
        <RC0603FR_07470KL
          name="R96"
          layer="top"
          pcbX={7}
          pcbY={6}
          schX={5}
          schY={4}
          schRotation={-90}
        />
        <RC0603FR_07470KL
          name="R97"
          layer="top"
          pcbX={7}
          pcbY={-6}
          schX={5}
          schY={-2}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C76"
          layer="top"
          pcbX={-7}
          pcbY={6}
          schX={-5}
          schY={4}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C77"
          layer="top"
          pcbX={-7}
          pcbY={-6}
          schX={0}
          schY={-2}
          schRotation={-90}
        />
        <trace from="U25.pin1" to="net.BUCK_ENABLE" />
        <trace from="U25.pin2" to="net.GND" />
        <trace from="U25.pin3" to="net.VSYS" />
        <trace from="U25.pin5" to="net.PACK_BAT" />
        <trace from="U25.pin6" to="net.VSYS" />
        <trace from="R96.pin1" to="net.VSYS" />
        <trace from="R96.pin2" to="net.BUCK_ENABLE" />
        <trace from="R97.pin1" to="net.BUCK_ENABLE" />
        <trace from="R97.pin2" to="net.GND" />
        <trace from="C76.pin1" to="net.VSYS" />
        <trace from="C76.pin2" to="net.GND" />
        <trace from="C77.pin1" to="net.BUCK_ENABLE" />
        <trace from="C77.pin2" to="net.GND" />
      </group>
    </schematicsheet>
  )
}
