import { MSK12C02 } from "../../imports/MSK12C02/MSK12C02"
import { S2B_PH_K_S_LF__SN_ } from "../../imports/S2B_PH_K_S_LF__SN_/S2B_PH_K_S_LF__SN_"
import { SKSWCFE010 } from "../../imports/SKSWCFE010/SKSWCFE010"
import { place } from "./placement"
export function ControlsSheet() {
  return (
    <schematicsheet
      name="ControlsSheet"
      displayName="AI Remote A1 - Physical controls and external motor port"
      sheetSize="A4"
      sheetIndex={11}
    >
      <group name="ControlsSheet-group" schLayout={{ layoutMode: "relative" }}>
        <SKSWCFE010 name="SW4" {...place("SW4")} schX={-8} schY={5} />
        <SKSWCFE010 name="SW1" {...place("SW1")} schX={-8} schY={0} />
        <SKSWCFE010 name="SW2" {...place("SW2")} schX={-8} schY={-5} />
        <MSK12C02 name="SW5" {...place("SW5")} schX={4} schY={5} />
        <S2B_PH_K_S_LF__SN_ name="J8" {...place("J8")} schX={6} schY={-5} />
        <trace from="SW4.pin1" to="net.V3V3" />
        <trace from="SW4.pin2" to="net.HOLD_HARDWARE" />
        <trace from="SW1.pin1" to="net.MCU_BOOT_N" />
        <trace from="SW1.pin2" to="net.GND" />
        <trace from="SW2.pin1" to="net.MCU_EN" />
        <trace from="SW2.pin2" to="net.GND" />
        <trace from="SW5.pin2" to="net.MIC_INPUT" />
        <trace from="SW5.pin1" to="net.V3V3" />
        <trace from="SW5.pin3" to="net.GND" />
        <trace from="SW5.pin4" to="net.GND" />
        <trace from="J8.pin1" to="net.VMOTOR" />
        <trace from="J8.pin2" to="net.HAPTIC_N" />
      </group>
    </schematicsheet>
  )
}
