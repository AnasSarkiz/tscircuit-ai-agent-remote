import { GRM188R61A106ME69D } from "../../imports/GRM188R61A106ME69D/GRM188R61A106ME69D"
import { TPS22919DCKR } from "../../imports/TPS22919DCKR/TPS22919DCKR"
import { TPS3839K33DBZR } from "../../imports/TPS3839K33DBZR/TPS3839K33DBZR"
import { SN74LVC1G14DBVR } from "../../imports/SN74LVC1G14DBVR/SN74LVC1G14DBVR"
import { SN74LVC1G17DBVR } from "../../imports/SN74LVC1G17DBVR/SN74LVC1G17DBVR"
import { SN74LVC2G125DCUR } from "../../imports/SN74LVC2G125DCUR/SN74LVC2G125DCUR"
import { TLV3201AIDBVR } from "../../imports/TLV3201AIDBVR/TLV3201AIDBVR"
import { GRM188R71C104KA01D } from "../../imports/GRM188R71C104KA01D/GRM188R71C104KA01D"
import { RC0603FR_0710KL } from "../../imports/RC0603FR_0710KL/RC0603FR_0710KL"
import { RC0603FR_07100KL } from "../../imports/RC0603FR_07100KL/RC0603FR_07100KL"
import { RC0603FR_071KL } from "../../imports/RC0603FR_071KL/RC0603FR_071KL"

// Independent IC application review. The hardware button and microphones are
// intentionally absent until their imported-component qualification is resolved.
// HOLD_HARDWARE has no MCU output connection. This is not a complete board.
// SD uses a comparator with a VMIC/2 reference because the microphone guarantees
// 0.35/0.65 VDD levels, incompatible with the previous logic-buffer thresholds.
// Voice acquisition target: 16 kHz, 64 SCK/frame. Timing and power-off leakage
// still require integration review and physical measurements.
export function MicrophoneIsolationReviewSheet() {
  return (
    <schematicsheet
      name="mic-isolation-review"
      displayName="AI Remote A0 — microphone isolation IC review (unrouted)"
      sheetIndex={1}
      sheetSize="A4"
    >
      <group
        name="mic-isolation-review-group"
        schX={0.0}
        schY={0.0}
        schLayout={{ layoutMode: "relative" }}
      >
        <net name="V3V3" isPowerNet />
        <net name="GND" isGroundNet />
        <net name="HOLD_HARDWARE" />
        <net name="VMIC" isPowerNet />
        <net name="MIC_READY_N" />
        <net name="MIC_OE_N" />
        <net name="HOLD_SENSE_RAW" />
        <net name="MCU_MIC_BCLK" />
        <net name="MIC_WS" />
        <net name="MCU_MIC_WS" />
        <net name="MIC_BCLK" />
        <net name="MIC_SD" />
        <net name="MIC_SD_REF" />
        <net name="MIC_SD_BUFFERED" />
        <net name="MCU_MIC_SD" />
        <net name="MCU_HOLD_SENSE" />
        <TPS22919DCKR
          name="U8"
          layer="top"
          pcbX={-14}
          pcbY={10}
          schX={-7.700000000000001}
          schY={6.0}
        />
        <TPS3839K33DBZR
          name="U9"
          layer="top"
          pcbX={-7}
          pcbY={10}
          schX={-3.8500000000000005}
          schY={6.0}
        />
        <SN74LVC1G14DBVR name="U10" layer="top" pcbX={0} pcbY={10} schX={0.0} schY={6.0} />
        <SN74LVC1G17DBVR
          name="U11"
          layer="top"
          pcbX={7}
          pcbY={10}
          schX={3.8500000000000005}
          schY={6.0}
        />
        <SN74LVC2G125DCUR
          name="U6"
          layer="top"
          pcbX={-7}
          pcbY={0}
          schX={-3.8500000000000005}
          schY={0.0}
        />
        <TLV3201AIDBVR
          name="U7"
          layer="top"
          pcbX={7}
          pcbY={0}
          schX={3.8500000000000005}
          schY={0.0}
        />
        <GRM188R61A106ME69D
          name="C20"
          layer="top"
          pcbX={-14}
          pcbY={-10}
          schX={-1.8}
          schY={-5}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C21"
          layer="top"
          pcbX={-7}
          pcbY={-10}
          schX={-0.6}
          schY={-8}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C22"
          layer="top"
          pcbX={0}
          pcbY={-10}
          schX={-0.6}
          schY={-5}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C23"
          layer="top"
          pcbX={7}
          pcbY={-10}
          schX={0.6}
          schY={-5}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C24"
          layer="top"
          pcbX={14}
          pcbY={-10}
          schX={0.6}
          schY={-8}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C25"
          layer="top"
          pcbX={21}
          pcbY={-10}
          schX={1.8}
          schY={-5}
          schRotation={-90}
        />
        <RC0603FR_0710KL
          name="R20"
          layer="top"
          pcbX={-21}
          pcbY={10}
          schX={-11.55}
          schY={6.0}
          schRotation={-90}
        />
        <RC0603FR_07100KL
          name="R21"
          layer="top"
          pcbX={-21}
          pcbY={0}
          schX={-11.55}
          schY={0.0}
          schRotation={-90}
        />
        <RC0603FR_0710KL
          name="R22"
          layer="top"
          pcbX={-21}
          pcbY={-10}
          schX={-11.55}
          schY={-6.0}
          schRotation={-90}
        />
        <RC0603FR_071KL
          name="R23"
          layer="top"
          pcbRotation={180}
          pcbX={-14}
          pcbY={0}
          schX={-7.700000000000001}
          schY={0.0}
          schRotation={-90}
        />
        <RC0603FR_0710KL
          name="R24"
          layer="top"
          pcbX={0}
          pcbY={0}
          schX={0.0}
          schY={0.0}
          schRotation={-90}
        />
        <RC0603FR_0710KL
          name="R25"
          layer="top"
          pcbX={14}
          pcbY={0}
          schX={7.700000000000001}
          schY={0.0}
          schRotation={-90}
        />
        <RC0603FR_07100KL
          name="R26"
          layer="top"
          pcbX={21}
          pcbY={0}
          schX={11.55}
          schY={0.0}
          schRotation={-90}
        />
        <RC0603FR_071KL
          name="R27"
          layer="top"
          pcbX={14}
          pcbY={10}
          schX={7.700000000000001}
          schY={6.0}
          schRotation={-90}
        />
        <RC0603FR_071KL
          name="R28"
          layer="top"
          pcbX={21}
          pcbY={10}
          schX={11.55}
          schY={6.0}
          schRotation={-90}
        />
        <RC0603FR_0710KL
          name="R29"
          layer="top"
          pcbX={-14}
          pcbY={-16}
          schX={8}
          schY={-3}
          schRotation={-90}
        />
        <RC0603FR_0710KL
          name="R30"
          layer="top"
          pcbX={-7}
          pcbY={-16}
          schX={11}
          schY={-3}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C26"
          layer="top"
          pcbX={0}
          pcbY={-16}
          schX={9.5}
          schY={-6}
          schRotation={-90}
        />
        <trace from="U8.pin1" to="net.V3V3" />
        <trace from="U8.pin2" to="net.GND" />
        <trace from="U8.pin3" to="net.HOLD_HARDWARE" />
        <trace from="U8.pin5" to="net.VMIC" />
        <trace from="U8.pin6" to="net.VMIC" />
        <trace from="U9.pin1" to="net.GND" />
        <trace from="U9.pin2" to="net.MIC_READY_N" />
        <trace from="U9.pin3" to="net.VMIC" />
        <trace from="U10.pin2" to="net.MIC_READY_N" />
        <trace from="U10.pin3" to="net.GND" />
        <trace from="U10.pin4" to="net.MIC_OE_N" />
        <trace from="U10.pin5" to="net.V3V3" />
        <trace from="U11.pin2" to="net.HOLD_HARDWARE" />
        <trace from="U11.pin3" to="net.GND" />
        <trace from="U11.pin4" to="net.HOLD_SENSE_RAW" />
        <trace from="U11.pin5" to="net.V3V3" />
        <trace from="U6.pin1" to="net.MIC_OE_N" />
        <trace from="U6.pin2" to="net.MCU_MIC_BCLK" />
        <trace from="U6.pin3" to="net.MIC_WS" />
        <trace from="U6.pin4" to="net.GND" />
        <trace from="U6.pin5" to="net.MCU_MIC_WS" />
        <trace from="U6.pin6" to="net.MIC_BCLK" />
        <trace from="U6.pin7" to="net.MIC_OE_N" />
        <trace from="U6.pin8" to="net.VMIC" />
        <trace from="U7.pin1" to="net.MIC_SD_BUFFERED" />
        <trace from="U7.pin2" to="net.GND" />
        <trace from="U7.pin3" to="net.MIC_SD" />
        <trace from="U7.pin4" to="net.MIC_SD_REF" />
        <trace from="U7.pin5" to="net.V3V3" />
        <trace from="C20.pin1" to="net.V3V3" />
        <trace from="C20.pin2" to="net.GND" />
        <trace from="C21.pin1" to="net.VMIC" />
        <trace from="C21.pin2" to="net.GND" />
        <trace from="C22.pin1" to="net.V3V3" />
        <trace from="C22.pin2" to="net.GND" />
        <trace from="C23.pin1" to="net.V3V3" />
        <trace from="C23.pin2" to="net.GND" />
        <trace from="C24.pin1" to="net.VMIC" />
        <trace from="C24.pin2" to="net.GND" />
        <trace from="C25.pin1" to="net.V3V3" />
        <trace from="C25.pin2" to="net.GND" />
        <trace from="R20.pin1" to="net.HOLD_HARDWARE" />
        <trace from="R20.pin2" to="net.GND" />
        <trace from="R21.pin1" to="net.MIC_READY_N" />
        <trace from="R21.pin2" to="net.GND" />
        <trace from="R23.pin1" to="net.VMIC" />
        <trace from="R23.pin2" to="net.GND" />
        <trace from="R24.pin1" to="net.MIC_BCLK" />
        <trace from="R24.pin2" to="net.GND" />
        <trace from="R25.pin1" to="net.MIC_WS" />
        <trace from="R25.pin2" to="net.GND" />
        <trace from="R26.pin1" to="net.MIC_SD" />
        <trace from="R26.pin2" to="net.GND" />
        <trace from="R22.pin1" to="net.V3V3" />
        <trace from="R22.pin2" to="net.MIC_OE_N" />
        <trace from="R27.pin1" to="net.MIC_SD_BUFFERED" />
        <trace from="R27.pin2" to="net.MCU_MIC_SD" />
        <trace from="R28.pin1" to="net.HOLD_SENSE_RAW" />
        <trace from="R28.pin2" to="net.MCU_HOLD_SENSE" />
        <trace from="R29.pin1" to="net.VMIC" />
        <trace from="R29.pin2" to="net.MIC_SD_REF" />
        <trace from="R30.pin1" to="net.MIC_SD_REF" />
        <trace from="R30.pin2" to="net.GND" />
        <trace from="C26.pin1" to="net.MIC_SD_REF" />
        <trace from="C26.pin2" to="net.GND" />
      </group>
    </schematicsheet>
  )
}
