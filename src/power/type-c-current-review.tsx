import { TUSB320LAIRWBR } from "../../imports/TUSB320LAIRWBR/TUSB320LAIRWBR"
import { TPS7A2033PDBVR } from "../../imports/TPS7A2033PDBVR/TPS7A2033PDBVR"
import { TPS3839K33DBZR } from "../../imports/TPS3839K33DBZR/TPS3839K33DBZR"
import { SN74LVC1G14DBVR } from "../../imports/SN74LVC1G14DBVR/SN74LVC1G14DBVR"
import { SN74LVC1G08DBVR } from "../../imports/SN74LVC1G08DBVR/SN74LVC1G08DBVR"
import { RC0603FR_07470KL } from "../../imports/RC0603FR_07470KL/RC0603FR_07470KL"
import { RC0603FR_07430KL } from "../../imports/RC0603FR_07430KL/RC0603FR_07430KL"
import { RC0603FR_0710KL } from "../../imports/RC0603FR_0710KL/RC0603FR_0710KL"
import { RC0603FR_071KL } from "../../imports/RC0603FR_071KL/RC0603FR_071KL"
import { GRM188R61A106ME69D } from "../../imports/GRM188R61A106ME69D/GRM188R61A106ME69D"
import { GRM188R61A226ME15D } from "../../imports/GRM188R61A226ME15D/GRM188R61A226ME15D"
import { GRM188R71C104KA01D } from "../../imports/GRM188R71C104KA01D/GRM188R71C104KA01D"

// Independent UFP hardware current detector. Charger/pack/system-enable still pending.
// CC1/CC2 use the controller's internal Rd; do not add parallel external Rd.
// Dedicated controller supply comes from charger VSYS, not raw USB VBUS.
export function TypeCCurrentReviewSheet() {
  return (
    <schematicsheet
      name="type-c-current-review"
      displayName="AI Remote A0 — Type-C current review (unrouted)"
      sheetIndex={1}
      sheetSize="A4"
    >
      <group name="type-c-current-review-group" schLayout={{ layoutMode: "relative" }}>
        <net name="GND" isGroundNet />
        <net name="VSYS" isPowerNet />
        <net name="USB_CTRL_V3V3" isPowerNet />
        <net name="VBUS" />
        <net name="USB_CC1" />
        <net name="USB_CC2" />
        <net name="VBUS_DETECT_MID" />
        <net name="VBUS_DETECT" />
        <net name="USB_HIGH_CURRENT_N" />
        <net name="USB_HIGH_CURRENT_DETECTED" />
        <net name="USB_CURRENT_OUT2" />
        <net name="USB_CTRL_READY" />
        <net name="USB_CHARGER_EN2" />
        <TPS7A2033PDBVR name="U15" layer="top" pcbX={-18} pcbY={6} schX={-10} schY={8} />
        <TUSB320LAIRWBR name="U18" layer="top" pcbX={-6} pcbY={0} schX={-6} schY={0} />
        <TPS3839K33DBZR name="U19" layer="top" pcbX={6} pcbY={6} schX={3} schY={6} />
        <SN74LVC1G14DBVR name="U20" layer="top" pcbX={6} pcbY={0} schX={3} schY={0} />
        <SN74LVC1G08DBVR name="U21" layer="top" pcbX={16} pcbY={0} schX={10} schY={0} />
        <GRM188R61A106ME69D
          name="C60"
          layer="top"
          pcbX={-23}
          pcbY={6}
          schX={-13}
          schY={8}
          schRotation={-90}
        />
        <GRM188R61A226ME15D
          name="C61"
          layer="top"
          pcbX={-13}
          pcbY={6}
          schX={-4}
          schY={8}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C62"
          layer="top"
          pcbX={-6}
          pcbY={5}
          schX={-1}
          schY={8}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C63"
          layer="top"
          pcbX={11}
          pcbY={6}
          schX={6}
          schY={6}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C64"
          layer="top"
          pcbX={6}
          pcbY={-5}
          schX={3}
          schY={-6}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C65"
          layer="top"
          pcbX={16}
          pcbY={-5}
          schX={11}
          schY={-6}
          schRotation={-90}
        />
        <RC0603FR_071KL
          name="R73"
          layer="top"
          pcbX={-18}
          pcbY={-5}
          schX={-10}
          schY={4}
          schRotation={-90}
        />
        <RC0603FR_07470KL name="R71" layer="top" pcbX={-23} pcbY={0} schX={-13} schY={-8} />
        <RC0603FR_07430KL name="R72" layer="top" pcbX={-18} pcbY={0} schX={-8} schY={-8} />
        <RC0603FR_0710KL
          name="R74"
          layer="top"
          pcbX={0}
          pcbY={5}
          pcbRotation={180}
          schX={-1}
          schY={3}
          schRotation={-90}
        />
        <RC0603FR_0710KL
          name="R75"
          layer="top"
          pcbX={0}
          pcbY={-5}
          pcbRotation={180}
          schX={-1}
          schY={-3}
          schRotation={-90}
        />
        <RC0603FR_071KL
          name="R76"
          layer="top"
          pcbX={21}
          pcbY={6}
          schX={13}
          schY={0}
          schRotation={-90}
        />
        <trace from="U15.pin1" to="net.VSYS" />
        <trace from="U15.pin2" to="net.GND" />
        <trace from="U15.pin3" to="net.VSYS" />
        <trace from="U15.pin5" to="net.USB_CTRL_V3V3" />
        <trace from="U18.pin1" to="net.USB_CC1" />
        <trace from="U18.pin2" to="net.USB_CC2" />
        <trace from="U18.pin3" to="net.GND" />
        <trace from="U18.pin4" to="net.VBUS_DETECT" />
        <trace from="U18.pin7" to="net.USB_HIGH_CURRENT_N" />
        <trace from="U18.pin8" to="net.USB_CURRENT_OUT2" />
        <trace from="U18.pin10" to="net.GND" />
        <trace from="U18.pin11" to="net.GND" />
        <trace from="U18.pin12" to="net.USB_CTRL_V3V3" />
        <trace from="U19.pin1" to="net.GND" />
        <trace from="U19.pin2" to="net.USB_CTRL_READY" />
        <trace from="U19.pin3" to="net.USB_CTRL_V3V3" />
        <trace from="U20.pin2" to="net.USB_HIGH_CURRENT_N" />
        <trace from="U20.pin3" to="net.GND" />
        <trace from="U20.pin4" to="net.USB_HIGH_CURRENT_DETECTED" />
        <trace from="U20.pin5" to="net.USB_CTRL_V3V3" />
        <trace from="U21.pin1" to="net.USB_CTRL_READY" />
        <trace from="U21.pin2" to="net.USB_HIGH_CURRENT_DETECTED" />
        <trace from="U21.pin3" to="net.GND" />
        <trace from="U21.pin4" to="net.USB_CHARGER_EN2" />
        <trace from="U21.pin5" to="net.USB_CTRL_V3V3" />
        <trace from="R71.pin1" to="net.VBUS" />
        <trace from="R71.pin2" to="net.VBUS_DETECT_MID" />
        <trace from="R72.pin1" to="net.VBUS_DETECT_MID" />
        <trace from="R72.pin2" to="net.VBUS_DETECT" />
        <trace from="R73.pin1" to="net.USB_CTRL_V3V3" />
        <trace from="R73.pin2" to="net.GND" />
        <trace from="R74.pin1" to="net.USB_CTRL_V3V3" />
        <trace from="R74.pin2" to="net.USB_HIGH_CURRENT_N" />
        <trace from="R75.pin1" to="net.USB_CTRL_V3V3" />
        <trace from="R75.pin2" to="net.USB_CURRENT_OUT2" />
        <trace from="R76.pin1" to="net.USB_CHARGER_EN2" />
        <trace from="R76.pin2" to="net.GND" />
        <trace from="C60.pin1" to="net.VSYS" />
        <trace from="C60.pin2" to="net.GND" />
        <trace from="C61.pin1" to="net.USB_CTRL_V3V3" />
        <trace from="C61.pin2" to="net.GND" />
        <trace from="C62.pin1" to="net.USB_CTRL_V3V3" />
        <trace from="C62.pin2" to="net.GND" />
        <trace from="C63.pin1" to="net.USB_CTRL_V3V3" />
        <trace from="C63.pin2" to="net.GND" />
        <trace from="C64.pin1" to="net.USB_CTRL_V3V3" />
        <trace from="C64.pin2" to="net.GND" />
        <trace from="C65.pin1" to="net.USB_CTRL_V3V3" />
        <trace from="C65.pin2" to="net.GND" />
      </group>
    </schematicsheet>
  )
}
