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
import { RC0603FR_071KL } from "../../imports/RC0603FR_071KL/RC0603FR_071KL"
import { GRM188R61A106ME69D } from "../../imports/GRM188R61A106ME69D/GRM188R61A106ME69D"
import { GRM188R71C104KA01D } from "../../imports/GRM188R71C104KA01D/GRM188R71C104KA01D"

// Isolated application review only. No routing or full-board qualification.
// Espressif module datasheet v1.8 and ESP32-S3 hardware design guidelines:
// GPIO19 = USB D-, GPIO20 = USB D+; GPIO35/36/37 are reserved for octal PSRAM.
// USB power entitlement, VBUS detection, ESD qualification and the final rail
// tolerance remain integration requirements. U12 asserts reset near 3.08 V;
// its release margin must be checked against the completed power application.
// J6 is internal: VREF is a voltage-sense output, never a programmer supply.
export function Esp32S3UsbReviewSheet() {
  return (
    <schematicsheet
      name="mcu-usb-review"
      displayName="AI Remote A0 — MCU and USB review (unrouted)"
      sheetIndex={1}
      sheetSize="A4"
    >
      <group name="mcu-usb-review-group" schLayout={{ layoutMode: "relative" }}>
        <net name="V3V3" isPowerNet />
        <net name="GND" isGroundNet />
        <net name="USB_VBUS" isPowerNet />
        <net name="USB_DP" />
        <net name="USB_DN" />
        <net name="MCU_USB_DP" />
        <net name="MCU_USB_DN" />
        <net name="USB_CC1" />
        <net name="USB_CC2" />
        <net name="MCU_RESET_N" />
        <net name="MCU_EN" />
        <net name="MCU_BOOT_N" />
        <net name="SERVICE_UART_TX" />
        <net name="MCU_UART_TX" />
        <net name="MCU_UART_RX" />
        <ESP32_S3_WROOM_1_N8R8 name="U1" layer="top" pcbX={10} pcbY={5} schX={0} schY={0} />
        <TYPE_C_31_M_12 name="J1" layer="top" pcbX={-18} pcbY={-18} schX={-10} schY={0} />
        <TPD2EUSB30ADRTR name="D2" layer="top" pcbX={-10} pcbY={-15} schX={-6} schY={-6} />
        <TPS3839G33DBZR name="U12" layer="top" pcbX={-18} pcbY={12} schX={-10} schY={7} />
        <SM06B_SRSS_TB_LF__SN_
          name="J6"
          layer="top"
          pcbRotation={-90}
          pcbX={-18}
          pcbY={0}
          schX={10}
          schY={3}
        />
        <RC0603FR_0722RL name="R31" layer="top" pcbX={-4} pcbY={-6} schX={-6} schY={-2} />
        <RC0603FR_0722RL name="R32" layer="top" pcbX={-4} pcbY={-10} schX={-6} schY={0} />
        <RC0603FR_075K1L
          name="R33"
          layer="top"
          pcbX={-25}
          pcbY={-12}
          schX={-13}
          schY={-6}
          schRotation={-90}
        />
        <RC0603FR_075K1L
          name="R34"
          layer="top"
          pcbX={-25}
          pcbY={-18}
          schX={-10}
          schY={-6}
          schRotation={-90}
        />
        <RC0603FR_074K7L name="R35" layer="top" pcbX={-12} pcbY={12} schX={-5} schY={7} />
        <RC0603FR_0710KL
          name="R36"
          layer="top"
          pcbX={22}
          pcbY={-9}
          schX={6}
          schY={-6}
          schRotation={-90}
        />
        <RC0603FR_07100KL
          name="R37"
          layer="top"
          pcbX={-4}
          pcbY={6}
          schX={-5}
          schY={4}
          schRotation={-90}
        />
        <RC0603FR_071KL name="R38" layer="top" pcbX={22} pcbY={-13} schX={6} schY={0} />
        <GRM188R61A106ME69D
          name="C30"
          layer="top"
          pcbX={-4}
          pcbY={14}
          schX={6}
          schY={7}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C31"
          layer="top"
          pcbX={-4}
          pcbY={10}
          schX={7.2}
          schY={7}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C32"
          layer="top"
          pcbX={-18}
          pcbY={17}
          schX={8.4}
          schY={7}
          schRotation={-90}
        />
        <trace from="U1.pin2" to="net.V3V3" />
        <trace from="U1.pin1" to="net.GND" />
        <trace from="U1.pin40" to="net.GND" />
        <trace from="U1.pin41" to="net.GND" />
        <trace from="U1.pin3" to="net.MCU_EN" />
        <trace from="U1.pin27" to="net.MCU_BOOT_N" />
        <trace from="U1.pin13" to="net.MCU_USB_DN" />
        <trace from="U1.pin14" to="net.MCU_USB_DP" />
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
        <trace from="J1.pin15" to="net.USB_VBUS" />
        <trace from="J1.pin16" to="net.USB_VBUS" />
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
        <trace from="R31.pin2" to="net.MCU_USB_DP" />
        <trace from="R32.pin1" to="net.USB_DN" />
        <trace from="R32.pin2" to="net.MCU_USB_DN" />
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
      </group>
    </schematicsheet>
  )
}
