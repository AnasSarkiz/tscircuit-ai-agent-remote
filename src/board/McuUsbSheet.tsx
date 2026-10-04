import { place } from "./placement"
import { ESP32_S3_WROOM_1_N8R8 } from "../../imports/ESP32_S3_WROOM_1_N8R8/ESP32_S3_WROOM_1_N8R8"
import { TYPE_C_31_M_12 } from "../../imports/TYPE_C_31_M_12/TYPE_C_31_M_12"
import { TPD2EUSB30ADRTR } from "../../imports/TPD2EUSB30ADRTR/TPD2EUSB30ADRTR"
import { TPS3839G33DBZR } from "../../imports/TPS3839G33DBZR/TPS3839G33DBZR"
import { SM06B_SRSS_TB_LF__SN_ } from "../../imports/SM06B_SRSS_TB_LF__SN_/SM06B_SRSS_TB_LF__SN_"
import { RC0603FR_0722RL } from "../../imports/RC0603FR_0722RL/RC0603FR_0722RL"
import { RC0603FR_074K7L } from "../../imports/RC0603FR_074K7L/RC0603FR_074K7L"
import { RC0603FR_075K1L } from "../../imports/RC0603FR_075K1L/RC0603FR_075K1L"
import { RC0603FR_0710KL } from "../../imports/RC0603FR_0710KL/RC0603FR_0710KL"
import { RC0603FR_07100KL } from "../../imports/RC0603FR_07100KL/RC0603FR_07100KL"
import { A_0603WAF1001T5E } from "../../imports/A_0603WAF1001T5E/A_0603WAF1001T5E"
import { GRM188R61A106ME69D } from "../../imports/GRM188R61A106ME69D/GRM188R61A106ME69D"
import { GRM188R71C104KA01D } from "../../imports/GRM188R71C104KA01D/GRM188R71C104KA01D"

export function McuUsbSheet({ placementOnly = false }: { placementOnly?: boolean } = {}) {
  return (
    <schematicsheet
      name="mcu-usb-review"
      displayName="AI Remote A1 - MCU, USB and programming"
      sheetIndex={1}
      sheetSize="A4"
    >
      <group name="mcu-usb-review-group" schLayout={{ layoutMode: "relative" }}>
        <ESP32_S3_WROOM_1_N8R8 name="U1" {...place("U1")} schX={0} schY={0} />
        <TYPE_C_31_M_12 name="J1" {...place("J1")} schX={-10} schY={0} />
        <TPD2EUSB30ADRTR name="D2" {...place("D2")} schX={-6} schY={-6} />
        <TPS3839G33DBZR name="U12" {...place("U12")} schX={-10} schY={7} />
        <SM06B_SRSS_TB_LF__SN_ name="J6" {...place("J6")} schX={10} schY={3} />
        <RC0603FR_0722RL name="R31" {...place("R31")} schX={-6} schY={-2} />
        <RC0603FR_0722RL name="R32" {...place("R32")} schX={-6} schY={0} />
        <RC0603FR_075K1L name="R33" {...place("R33")} schX={-13} schY={-6} schRotation={-90} />
        <RC0603FR_075K1L name="R34" {...place("R34")} schX={-10} schY={-6} schRotation={-90} />
        <RC0603FR_074K7L name="R35" {...place("R35")} schX={-5} schY={7} />
        <RC0603FR_0710KL name="R36" {...place("R36")} schX={6} schY={-6} schRotation={-90} />
        <RC0603FR_07100KL name="R37" {...place("R37")} schX={-5} schY={4} schRotation={-90} />
        <A_0603WAF1001T5E name="R38" {...place("R38")} schX={6} schY={0} />
        <GRM188R61A106ME69D name="C30" {...place("C30")} schX={6} schY={7} schRotation={-90} />
        <GRM188R71C104KA01D name="C31" {...place("C31")} schX={7.2} schY={7} schRotation={-90} />
        <GRM188R71C104KA01D name="C32" {...place("C32")} schX={8.4} schY={7} schRotation={-90} />
        <trace from="U1.pin2" to="net.V3V3" />
        <trace from="U1.pin1" to="net.GND" />
        <trace from="U1.pin40" to="net.GND" />
        <trace from="U1.pin41" to="net.GND" />
        <trace from="U1.pin3" to="net.MCU_EN" />
        <trace from="U1.pin27" to="net.MCU_BOOT_N" />
        <trace
          path={["U1.pin13", "R32.pin2", "net.MCU_USB_DN"]}
          width={0.2906}
          pcbPath={placementOnly ? undefined : ["R32.pin2"]}
        />
        <trace
          path={["U1.pin14", "R31.pin2", "net.MCU_USB_DP"]}
          width={0.2906}
          pcbPath={placementOnly ? undefined : ["R31.pin2"]}
        />
        <trace from="U1.pin37" to="net.MCU_UART_TX" />
        <trace from="U1.pin36" to="net.MCU_UART_RX" />
        <trace from="U12.pin1" to="net.GND" />
        <trace from="U12.pin3" to="net.V3V3" />
        <trace from="U12.pin2" to="net.MCU_RESET_N" />
        <trace from="R35.pin1" to="net.MCU_RESET_N" />
        <trace from="R35.pin2" to="net.MCU_EN" />
        <trace from="R37.pin1" to="net.MCU_EN" />
        <trace from="R37.pin2" to="net.GND" />
        <trace from="R36.pin1" to="net.V3V3" />
        <trace from="R36.pin2" to="net.MCU_BOOT_N" />
        <trace from="R38.pin1" to="net.MCU_UART_TX" />
        <trace from="R38.pin2" to="net.SERVICE_UART_TX" />
        <trace from="J6.pin1" to="net.GND" />
        <trace from="J6.pin2" to="net.V3V3" />
        <trace from="J6.pin3" to="net.MCU_EN" />
        <trace from="J6.pin4" to="net.MCU_BOOT_N" />
        <trace from="J6.pin5" to="net.SERVICE_UART_TX" />
        <trace from="J6.pin6" to="net.MCU_UART_RX" />
        <trace from="J6.pin7" to="net.GND" />
        <trace from="J6.pin8" to="net.GND" />
        <trace from="J1.pin1" to="net.GND" />
        <trace from="J1.pin2" to="net.GND" />
        <trace from="J1.pin3" to="net.GND" />
        <trace from="J1.pin4" to="net.GND" />
        <trace from="J1.pin13" to="net.GND" />
        <trace from="J1.pin14" to="net.GND" />
        <trace from="J1.pin15" to="net.VBUS" />
        <trace from="J1.pin16" to="net.VBUS" />
        <trace from="J1.pin6" to="net.USB_CC1" />
        <trace from="J1.pin12" to="net.USB_CC2" />
        <trace from="J1.pin8" to="net.USB_DP" />
        <trace from="J1.pin10" to="net.USB_DP" />
        <trace from="J1.pin7" to="net.USB_DN" />
        <trace from="J1.pin9" to="net.USB_DN" />
        <trace from="D2.pin1" to="net.USB_DP" />
        <trace from="D2.pin2" to="net.USB_DN" />
        <trace from="D2.pin3" to="net.GND" />
        <trace from="R31.pin1" to="net.USB_DP" />
        <trace from="R32.pin1" to="net.USB_DN" />
        <trace from="R33.pin1" to="net.USB_CC1" />
        <trace from="R33.pin2" to="net.GND" />
        <trace from="R34.pin1" to="net.USB_CC2" />
        <trace from="R34.pin2" to="net.GND" />
        <trace from="C30.pin1" to="net.V3V3" />
        <trace from="C30.pin2" to="net.GND" />
        <trace from="C31.pin1" to="net.V3V3" />
        <trace from="C31.pin2" to="net.GND" />
        <trace from="C32.pin1" to="net.V3V3" />
        <trace from="C32.pin2" to="net.GND" />
        <trace from="U1.pin23" to="net.MCU_HOLD_READ" />
        <trace from="U1.pin8" to="net.MCU_MIC_BCLK" />
        <trace from="U1.pin9" to="net.MCU_MIC_WS" />
        <trace from="U1.pin10" to="net.MCU_MIC_SD" />
        <trace from="U1.pin17" to="net.MCU_AUDIO_BCLK" />
        <trace from="U1.pin12" to="net.MCU_AUDIO_LRCLK" />
        <trace from="U1.pin7" to="net.MCU_AUDIO_DIN" />
        <trace from="U1.pin4" to="net.MCU_AUDIO_ENABLE" />
        <trace from="U1.pin5" to="net.MCU_HAPTIC_ENABLE" />
        <trace from="U1.pin6" to="net.LCD_ENABLE" />
        <trace from="U1.pin18" to="net.MCU_LCD_CS_N" />
        <trace from="U1.pin20" to="net.MCU_LCD_SCLK" />
        <trace from="U1.pin19" to="net.MCU_LCD_SDA" />
        <trace from="U1.pin21" to="net.MCU_LCD_DC" />
        <trace from="U1.pin22" to="net.MCU_LCD_RESET_N" />
        <trace from="U1.pin24" to="net.MCU_BACKLIGHT_PWM" />
      </group>
    </schematicsheet>
  )
}
