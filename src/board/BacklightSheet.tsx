import { AO3400A } from "../../imports/AO3400A/AO3400A"
import { RC0603FR_07100RL } from "../../imports/RC0603FR_07100RL/RC0603FR_07100RL"
import { RC0603FR_0710KL } from "../../imports/RC0603FR_0710KL/RC0603FR_0710KL"
import { place } from "./placement"
export function BacklightSheet() {
  return (
    <schematicsheet
      name="BacklightSheet"
      displayName="AI Remote A1 - Resistive backlight - PROVISIONAL"
      sheetSize="A4"
      sheetIndex={12}
    >
      <group name="BacklightSheet-group" schLayout={{ layoutMode: "relative" }}>
        <AO3400A name="Q10" {...place("Q10")} schX={3} schY={0} />
        <RC0603FR_07100RL name="R102" {...place("R102")} schX={-6} schY={4} />
        <RC0603FR_07100RL name="R103" {...place("R103")} schX={-3} schY={-4} />
        <RC0603FR_0710KL name="R104" {...place("R104")} schX={3} schY={-4} />
        <trace from="R102.pin1" to="net.VSYS" />
        <trace from="R102.pin2" to="net.LCD_BACKLIGHT_OUTPUT" />
        <trace from="Q10.pin3" to="net.LCD_BACKLIGHT_RETURN" />
        <trace from="Q10.pin2" to="net.GND" />
        <trace from="Q10.pin1" to="net.BACKLIGHT_GATE" />
        <trace from="R103.pin1" to="net.MCU_BACKLIGHT_PWM" />
        <trace from="R103.pin2" to="net.BACKLIGHT_GATE" />
        <trace from="R104.pin1" to="net.BACKLIGHT_GATE" />
        <trace from="R104.pin2" to="net.GND" />
      </group>
    </schematicsheet>
  )
}
