import { place } from "./placement"
import { TPS7A2028PDBVR } from "../../imports/TPS7A2028PDBVR/TPS7A2028PDBVR"
import { SN74LVC245APWR } from "../../imports/SN74LVC245APWR/SN74LVC245APWR"
import { AFC07_S12FCC_00 } from "../../imports/AFC07_S12FCC_00/AFC07_S12FCC_00"
import { RC0603FR_07100KL } from "../../imports/RC0603FR_07100KL/RC0603FR_07100KL"
import { RC0603FR_0710KL } from "../../imports/RC0603FR_0710KL/RC0603FR_0710KL"
import { RC0603FR_071KL } from "../../imports/RC0603FR_071KL/RC0603FR_071KL"
import { GRM188R61A106ME69D } from "../../imports/GRM188R61A106ME69D/GRM188R61A106ME69D"
import { GRM188R61A226ME15D } from "../../imports/GRM188R61A226ME15D/GRM188R61A226ME15D"
import { GRM188R71C104KA01D } from "../../imports/GRM188R71C104KA01D/GRM188R71C104KA01D"

export function DisplaySheet() {
  return (
    <schematicsheet
      name="display-logic-review"
      displayName="AI Remote A2 - HS20HS072RX interface - MECHANICS PENDING"
      sheetIndex={4}
      sheetSize="A4"
    >
      <group name="display-logic-review-group" schLayout={{ layoutMode: "relative" }}>
        <TPS7A2028PDBVR name="U13" {...place("U13")} schX={-6.75} schY={6.0} />
        <SN74LVC245APWR name="U14" {...place("U14")} schX={0.0} schY={0.0} />
        <AFC07_S12FCC_00 name="J7" {...place("J7")} schX={6.75} schY={0.0} />
        <GRM188R61A106ME69D
          name="C40"
          {...place("C40")}
          schX={-11.25}
          schY={6.0}
          schRotation={-90}
        />
        <GRM188R61A226ME15D name="C41" {...place("C41")} schX={-3.0} schY={6.0} schRotation={-90} />
        <GRM188R71C104KA01D
          name="C42"
          {...place("C42")}
          schX={-0.75}
          schY={6.0}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C43"
          {...place("C43")}
          schX={-3.0}
          schY={8.25}
          schRotation={-90}
        />
        <RC0603FR_07100KL name="R40" {...place("R40")} schX={-6.75} schY={3.0} schRotation={-90} />
        <RC0603FR_071KL name="R41" {...place("R41")} schX={-3.0} schY={-6.75} schRotation={-90} />
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
        <trace from="J7.pin1" to="net.GND" />
        <trace from="J7.pin2" to="net.LCD_CS_N" />
        <trace from="J7.pin3" to="net.LCD_DC" />
        <trace from="J7.pin4" to="net.LCD_SCLK" />
        <trace from="J7.pin5" to="net.LCD_SDA" />
        <trace from="J7.pin6" to="net.LCD_RESET_N" />
        <trace from="J7.pin8" to="net.VLCD" />
        <trace from="J7.pin9" to="net.VLCD" />
        <trace from="J7.pin10" to="net.LCD_BACKLIGHT_OUTPUT" />
        <trace from="J7.pin11" to="net.LCD_BACKLIGHT_RETURN" />
        <trace from="J7.pin12" to="net.GND" />
        <trace from="J7.pin13" to="net.GND" />
        <trace from="J7.pin14" to="net.GND" />
        <RC0603FR_07100KL name="R47" {...place("R47")} schX={-6.0} schY={0.75} schRotation={-90} />
        <RC0603FR_0710KL name="R42" {...place("R42")} schX={11.25} schY={0.75} schRotation={-90} />
        <trace from="U14.pin2" to="net.MCU_LCD_CS_N" />
        <trace from="R47.pin1" to="net.MCU_LCD_CS_N" />
        <trace from="R47.pin2" to="net.GND" />
        <trace from="U14.pin18" to="net.LCD_CS_N" />
        <trace from="R42.pin1" to="net.LCD_CS_N" />
        <trace from="R42.pin2" to="net.VLCD" />
        <RC0603FR_07100KL name="R48" {...place("R48")} schX={-6.0} schY={-1.5} schRotation={-90} />
        <RC0603FR_0710KL name="R43" {...place("R43")} schX={11.25} schY={-1.5} schRotation={-90} />
        <trace from="U14.pin3" to="net.MCU_LCD_RESET_N" />
        <trace from="R48.pin1" to="net.MCU_LCD_RESET_N" />
        <trace from="R48.pin2" to="net.GND" />
        <trace from="U14.pin17" to="net.LCD_RESET_N" />
        <trace from="R43.pin1" to="net.LCD_RESET_N" />
        <trace from="R43.pin2" to="net.GND" />
        <RC0603FR_07100KL name="R49" {...place("R49")} schX={-6.0} schY={-3.75} schRotation={-90} />
        <RC0603FR_0710KL name="R44" {...place("R44")} schX={11.25} schY={-3.75} schRotation={-90} />
        <trace from="U14.pin4" to="net.MCU_LCD_DC" />
        <trace from="R49.pin1" to="net.MCU_LCD_DC" />
        <trace from="R49.pin2" to="net.GND" />
        <trace from="U14.pin16" to="net.LCD_DC" />
        <trace from="R44.pin1" to="net.LCD_DC" />
        <trace from="R44.pin2" to="net.GND" />
        <RC0603FR_07100KL name="R50" {...place("R50")} schX={-6.0} schY={-6.0} schRotation={-90} />
        <RC0603FR_0710KL name="R45" {...place("R45")} schX={11.25} schY={-6.0} schRotation={-90} />
        <trace from="U14.pin5" to="net.MCU_LCD_SCLK" />
        <trace from="R50.pin1" to="net.MCU_LCD_SCLK" />
        <trace from="R50.pin2" to="net.GND" />
        <trace from="U14.pin15" to="net.LCD_SCLK" />
        <trace from="R45.pin1" to="net.LCD_SCLK" />
        <trace from="R45.pin2" to="net.GND" />
        <RC0603FR_07100KL name="R51" {...place("R51")} schX={-6.0} schY={-8.25} schRotation={-90} />
        <RC0603FR_0710KL name="R46" {...place("R46")} schX={11.25} schY={-8.25} schRotation={-90} />
        <trace from="U14.pin6" to="net.MCU_LCD_SDA" />
        <trace from="R51.pin1" to="net.MCU_LCD_SDA" />
        <trace from="R51.pin2" to="net.GND" />
        <trace from="U14.pin14" to="net.LCD_SDA" />
        <trace from="R46.pin1" to="net.LCD_SDA" />
        <trace from="R46.pin2" to="net.GND" />
      </group>
    </schematicsheet>
  )
}
