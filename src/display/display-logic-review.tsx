import { TPS7A2028PDBVR } from "../../imports/TPS7A2028PDBVR/TPS7A2028PDBVR"
import { SN74LVC245APWR } from "../../imports/SN74LVC245APWR/SN74LVC245APWR"
import { AFC07_S10FCC_00 } from "../../imports/AFC07_S10FCC_00/AFC07_S10FCC_00"
import { RC0603FR_07100KL } from "../../imports/RC0603FR_07100KL/RC0603FR_07100KL"
import { RC0603FR_0710KL } from "../../imports/RC0603FR_0710KL/RC0603FR_0710KL"
import { RC0603FR_071KL } from "../../imports/RC0603FR_071KL/RC0603FR_071KL"
import { GRM188R61A106ME69D } from "../../imports/GRM188R61A106ME69D/GRM188R61A106ME69D"
import { GRM188R61A226ME15D } from "../../imports/GRM188R61A226ME15D/GRM188R61A226ME15D"
import { GRM188R71C104KA01D } from "../../imports/GRM188R71C104KA01D/GRM188R71C104KA01D"

// Partial display logic application. Backlight supply and external LCD mechanics
// are not implemented by this fixture. Exact HS17QS178RX VDD is 2.7–3.3 V;
// the lower-voltage buffer prevents MCU signals exceeding VDD + 0.3 V.
// Firmware must set CS/reset/data/clock states before raising LCD_ENABLE.
export function DisplayLogicReviewSheet() {
  return (
    <schematicsheet
      name="display-logic-review"
      displayName="AI Remote A0 — LCD logic review (unrouted)"
      sheetIndex={1}
      sheetSize="A4"
    >
      <group name="display-logic-review-group" schLayout={{ layoutMode: "relative" }}>
        <net name="GND" isGroundNet />
        <net name="V3V3" isPowerNet />
        <net name="VLCD" isPowerNet />
        <net name="LCD_ENABLE" />
        <net name="LCD_BACKLIGHT_OUTPUT" />
        <net name="LCD_BACKLIGHT_RETURN" />
        <TPS7A2028PDBVR name="U13" layer="top" pcbX={-14} pcbY={4} schX={-9} schY={8} />
        <SN74LVC245APWR name="U14" layer="top" pcbX={0} pcbY={0} schX={0} schY={0} />
        <AFC07_S10FCC_00
          name="J7"
          layer="top"
          pcbX={15}
          pcbY={0}
          pcbRotation={-90}
          schX={9}
          schY={0}
        />
        <GRM188R61A106ME69D
          name="C40"
          layer="top"
          pcbX={-19}
          pcbY={4}
          schX={-15}
          schY={8}
          schRotation={-90}
        />
        <GRM188R61A226ME15D
          name="C41"
          layer="top"
          pcbX={-14}
          pcbY={-3}
          schX={-4}
          schY={8}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C42"
          layer="top"
          pcbX={0}
          pcbY={6}
          schX={-1}
          schY={8}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C43"
          layer="top"
          pcbX={15}
          pcbY={-9}
          schX={-4}
          schY={11}
          schRotation={-90}
        />
        <RC0603FR_07100KL
          name="R40"
          layer="top"
          pcbX={-19}
          pcbY={-6}
          schX={-9}
          schY={4}
          schRotation={-90}
        />
        <RC0603FR_071KL
          name="R41"
          layer="top"
          pcbX={-14}
          pcbY={-9}
          schX={-4}
          schY={-9}
          schRotation={-90}
        />
        <trace from="U13.pin1" to="net.V3V3" />
        <trace from="U13.pin2" to="net.GND" />
        <trace from="U13.pin3" to="net.LCD_ENABLE" />
        <trace from="U13.pin5" to="net.VLCD" />
        <trace from="R40.pin1" to="net.LCD_ENABLE" />
        <trace from="R40.pin2" to="net.GND" />
        <trace from="R41.pin1" to="net.VLCD" />
        <trace from="R41.pin2" to="net.GND" />
        <trace from="C40.pin1" to="net.V3V3" />
        <trace from="C40.pin2" to="net.GND" />
        <trace from="C41.pin1" to="net.VLCD" />
        <trace from="C41.pin2" to="net.GND" />
        <trace from="C42.pin1" to="net.VLCD" />
        <trace from="C42.pin2" to="net.GND" />
        <trace from="C43.pin1" to="net.VLCD" />
        <trace from="C43.pin2" to="net.GND" />
        <trace from="U14.pin1" to="net.VLCD" />
        <trace from="U14.pin10" to="net.GND" />
        <trace from="U14.pin19" to="net.GND" />
        <trace from="U14.pin20" to="net.VLCD" />
        <trace from="U14.pin7" to="net.GND" />
        <trace from="U14.pin8" to="net.GND" />
        <trace from="U14.pin9" to="net.GND" />
        <trace from="J7.pin1" to="net.LCD_BACKLIGHT_RETURN" />
        <trace from="J7.pin2" to="net.LCD_BACKLIGHT_OUTPUT" />
        <trace from="J7.pin3" to="net.VLCD" />
        <trace from="J7.pin10" to="net.GND" />
        <trace from="J7.pin11" to="net.GND" />
        <trace from="J7.pin12" to="net.GND" />
        <net name="MCU_LCD_CS_N" />
        <net name="LCD_CS_N" />
        <RC0603FR_07100KL
          name="R47"
          layer="top"
          pcbX={-8}
          pcbY={8}
          schX={-8}
          schY={1}
          schRotation={-90}
        />
        <RC0603FR_0710KL
          name="R42"
          layer="top"
          pcbX={8}
          pcbY={8}
          schX={15}
          schY={1}
          schRotation={-90}
        />
        <trace from="U14.pin2" to="net.MCU_LCD_CS_N" />
        <trace from="R47.pin1" to="net.MCU_LCD_CS_N" />
        <trace from="R47.pin2" to="net.GND" />
        <trace from="U14.pin18" to="net.LCD_CS_N" />
        <trace from="J7.pin5" to="net.LCD_CS_N" />
        <trace from="R42.pin1" to="net.LCD_CS_N" />
        <trace from="R42.pin2" to="net.VLCD" />
        <net name="MCU_LCD_RESET_N" />
        <net name="LCD_RESET_N" />
        <RC0603FR_07100KL
          name="R48"
          layer="top"
          pcbX={-8}
          pcbY={4}
          schX={-8}
          schY={-2}
          schRotation={-90}
        />
        <RC0603FR_0710KL
          name="R43"
          layer="top"
          pcbX={8}
          pcbY={4}
          schX={15}
          schY={-2}
          schRotation={-90}
        />
        <trace from="U14.pin3" to="net.MCU_LCD_RESET_N" />
        <trace from="R48.pin1" to="net.MCU_LCD_RESET_N" />
        <trace from="R48.pin2" to="net.GND" />
        <trace from="U14.pin17" to="net.LCD_RESET_N" />
        <trace from="J7.pin6" to="net.LCD_RESET_N" />
        <trace from="R43.pin1" to="net.LCD_RESET_N" />
        <trace from="R43.pin2" to="net.GND" />
        <net name="MCU_LCD_DC" />
        <net name="LCD_DC" />
        <RC0603FR_07100KL
          name="R49"
          layer="top"
          pcbX={-8}
          pcbY={0}
          schX={-8}
          schY={-5}
          schRotation={-90}
        />
        <RC0603FR_0710KL
          name="R44"
          layer="top"
          pcbX={8}
          pcbY={0}
          schX={15}
          schY={-5}
          schRotation={-90}
        />
        <trace from="U14.pin4" to="net.MCU_LCD_DC" />
        <trace from="R49.pin1" to="net.MCU_LCD_DC" />
        <trace from="R49.pin2" to="net.GND" />
        <trace from="U14.pin16" to="net.LCD_DC" />
        <trace from="J7.pin7" to="net.LCD_DC" />
        <trace from="R44.pin1" to="net.LCD_DC" />
        <trace from="R44.pin2" to="net.GND" />
        <net name="MCU_LCD_SCLK" />
        <net name="LCD_SCLK" />
        <RC0603FR_07100KL
          name="R50"
          layer="top"
          pcbX={-8}
          pcbY={-4}
          schX={-8}
          schY={-8}
          schRotation={-90}
        />
        <RC0603FR_0710KL
          name="R45"
          layer="top"
          pcbX={8}
          pcbY={-4}
          schX={15}
          schY={-8}
          schRotation={-90}
        />
        <trace from="U14.pin5" to="net.MCU_LCD_SCLK" />
        <trace from="R50.pin1" to="net.MCU_LCD_SCLK" />
        <trace from="R50.pin2" to="net.GND" />
        <trace from="U14.pin15" to="net.LCD_SCLK" />
        <trace from="J7.pin8" to="net.LCD_SCLK" />
        <trace from="R45.pin1" to="net.LCD_SCLK" />
        <trace from="R45.pin2" to="net.GND" />
        <net name="MCU_LCD_SDA" />
        <net name="LCD_SDA" />
        <RC0603FR_07100KL
          name="R51"
          layer="top"
          pcbX={-8}
          pcbY={-8}
          schX={-8}
          schY={-11}
          schRotation={-90}
        />
        <RC0603FR_0710KL
          name="R46"
          layer="top"
          pcbX={8}
          pcbY={-8}
          schX={15}
          schY={-11}
          schRotation={-90}
        />
        <trace from="U14.pin6" to="net.MCU_LCD_SDA" />
        <trace from="R51.pin1" to="net.MCU_LCD_SDA" />
        <trace from="R51.pin2" to="net.GND" />
        <trace from="U14.pin14" to="net.LCD_SDA" />
        <trace from="J7.pin9" to="net.LCD_SDA" />
        <trace from="R46.pin1" to="net.LCD_SDA" />
        <trace from="R46.pin2" to="net.GND" />
      </group>
    </schematicsheet>
  )
}
