import { MAX98357AETE_T } from "../../imports/MAX98357AETE_T/MAX98357AETE_T"
import { AO3400A } from "../../imports/AO3400A/AO3400A"
import { AO3401A } from "../../imports/AO3401A/AO3401A"
import { S2B_PH_SM4_TB_LF__SN_ } from "../../imports/S2B_PH_SM4_TB_LF__SN_/S2B_PH_SM4_TB_LF__SN_"
import { RC0603FR_071KL } from "../../imports/RC0603FR_071KL/RC0603FR_071KL"
import { RC0603FR_0710KL } from "../../imports/RC0603FR_0710KL/RC0603FR_0710KL"
import { RC0603FR_07100RL } from "../../imports/RC0603FR_07100RL/RC0603FR_07100RL"
import { RC0603FR_0722RL } from "../../imports/RC0603FR_0722RL/RC0603FR_0722RL"
import { GRM188R61A106ME69D } from "../../imports/GRM188R61A106ME69D/GRM188R61A106ME69D"
import { GRM188R71C104KA01D } from "../../imports/GRM188R71C104KA01D/GRM188R71C104KA01D"

// Unrouted amplifier application. External speaker qualification remains B-012.
// SD_MODE is driven from VSYS, through a default-off two-MOSFET interface.
// Use 16 kHz/64Fs I2S and valid paired clocks; shut down before stopping clocks.
export function SpeakerAmplifierReviewSheet() {
  return (
    <schematicsheet
      name="speaker-amplifier-review"
      displayName="AI Remote A0 — speaker amplifier review (unrouted)"
      sheetIndex={1}
      sheetSize="A4"
    >
      <group name="speaker-amplifier-review-group" schLayout={{ layoutMode: "relative" }}>
        <net name="GND" isGroundNet />
        <net name="VSYS" isPowerNet />
        <net name="MCU_AUDIO_ENABLE" />
        <net name="AUDIO_NMOS_GATE" />
        <net name="AUDIO_PMOS_GATE" />
        <net name="AUDIO_ENABLE_SUPPLY" />
        <net name="AMP_SD_MODE" />
        <net name="SPEAKER_P" />
        <net name="SPEAKER_N" />
        <MAX98357AETE_T name="U3" layer="top" pcbX={0} pcbY={0} schX={2} schY={0} />
        <AO3400A name="Q1" layer="top" pcbX={-14} pcbY={0} schX={-10} schY={-8} />
        <AO3401A name="Q2" layer="top" pcbX={-8} pcbY={0} schX={-5} schY={-8} />
        <S2B_PH_SM4_TB_LF__SN_
          name="J4"
          layer="top"
          pcbX={13}
          pcbY={0}
          pcbRotation={-90}
          schX={9}
          schY={0}
        />
        <GRM188R61A106ME69D
          name="C50"
          layer="top"
          pcbX={5}
          pcbY={5}
          schX={1}
          schY={7}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C51"
          layer="top"
          pcbX={0}
          pcbY={8}
          pcbRotation={180}
          schX={4}
          schY={7}
          schRotation={-90}
        />
        <RC0603FR_07100RL name="R60" layer="top" pcbX={-19} pcbY={-5} schX={-15} schY={-8} />
        <RC0603FR_0710KL
          name="R61"
          layer="top"
          pcbX={-14}
          pcbY={-5}
          schX={-10}
          schY={-11}
          schRotation={-90}
        />
        <RC0603FR_071KL
          name="R62"
          layer="top"
          pcbX={-8}
          pcbY={5}
          schX={-5}
          schY={-4}
          schRotation={-90}
        />
        <RC0603FR_07100RL name="R63" layer="top" pcbX={-4} pcbY={-5} schX={0} schY={-8} />
        <RC0603FR_071KL
          name="R64"
          layer="top"
          pcbX={1}
          pcbY={-5}
          schX={4}
          schY={-8}
          schRotation={-90}
        />
        <trace from="U3.pin2" to="net.VSYS" />
        <trace from="U3.pin7" to="net.VSYS" />
        <trace from="U3.pin8" to="net.VSYS" />
        <trace from="U3.pin3" to="net.GND" />
        <trace from="U3.pin11" to="net.GND" />
        <trace from="U3.pin15" to="net.GND" />
        <trace from="U3.pin17" to="net.GND" />
        <trace from="U3.pin4" to="net.AMP_SD_MODE" />
        <trace from="U3.pin9" to="net.SPEAKER_P" />
        <trace from="U3.pin10" to="net.SPEAKER_N" />
        <trace from="J4.pin1" to="net.SPEAKER_P" />
        <trace from="J4.pin2" to="net.SPEAKER_N" />
        <trace from="J4.pin3" to="net.GND" />
        <trace from="J4.pin4" to="net.GND" />
        <trace from="Q1.pin1" to="net.AUDIO_NMOS_GATE" />
        <trace from="Q1.pin2" to="net.GND" />
        <trace from="Q1.pin3" to="net.AUDIO_PMOS_GATE" />
        <trace from="Q2.pin1" to="net.AUDIO_PMOS_GATE" />
        <trace from="Q2.pin2" to="net.VSYS" />
        <trace from="Q2.pin3" to="net.AUDIO_ENABLE_SUPPLY" />
        <trace from="R60.pin1" to="net.MCU_AUDIO_ENABLE" />
        <trace from="R60.pin2" to="net.AUDIO_NMOS_GATE" />
        <trace from="R61.pin1" to="net.AUDIO_NMOS_GATE" />
        <trace from="R61.pin2" to="net.GND" />
        <trace from="R62.pin1" to="net.VSYS" />
        <trace from="R62.pin2" to="net.AUDIO_PMOS_GATE" />
        <trace from="R63.pin1" to="net.AUDIO_ENABLE_SUPPLY" />
        <trace from="R63.pin2" to="net.AMP_SD_MODE" />
        <trace from="R64.pin1" to="net.AMP_SD_MODE" />
        <trace from="R64.pin2" to="net.GND" />
        <trace from="C50.pin1" to="net.VSYS" />
        <trace from="C50.pin2" to="net.GND" />
        <trace from="C51.pin1" to="net.VSYS" />
        <trace from="C51.pin2" to="net.GND" />
        <net name="MCU_AUDIO_DIN" />
        <net name="AMP_DIN" />
        <RC0603FR_0722RL name="R65" layer="top" pcbX={-4} pcbY={9} schX={-9} schY={4} />
        <RC0603FR_0710KL
          name="R68"
          layer="top"
          pcbX={-19}
          pcbY={9}
          schX={-4}
          schY={4}
          schRotation={-90}
        />
        <trace from="R65.pin1" to="net.MCU_AUDIO_DIN" />
        <trace from="R65.pin2" to="net.AMP_DIN" />
        <trace from="R68.pin1" to="net.AMP_DIN" />
        <trace from="R68.pin2" to="net.GND" />
        <trace from="U3.pin1" to="net.AMP_DIN" />
        <net name="MCU_AUDIO_BCLK" />
        <net name="AMP_BCLK" />
        <RC0603FR_0722RL name="R66" layer="top" pcbX={-4} pcbY={5} schX={-9} schY={1} />
        <RC0603FR_0710KL
          name="R69"
          layer="top"
          pcbX={-19}
          pcbY={5}
          schX={-4}
          schY={1}
          schRotation={-90}
        />
        <trace from="R66.pin1" to="net.MCU_AUDIO_BCLK" />
        <trace from="R66.pin2" to="net.AMP_BCLK" />
        <trace from="R69.pin1" to="net.AMP_BCLK" />
        <trace from="R69.pin2" to="net.GND" />
        <trace from="U3.pin16" to="net.AMP_BCLK" />
        <net name="MCU_AUDIO_LRCLK" />
        <net name="AMP_LRCLK" />
        <RC0603FR_0722RL name="R67" layer="top" pcbX={-4} pcbY={1} schX={-9} schY={-2} />
        <RC0603FR_0710KL
          name="R70"
          layer="top"
          pcbX={-19}
          pcbY={1}
          schX={-4}
          schY={-2}
          schRotation={-90}
        />
        <trace from="R67.pin1" to="net.MCU_AUDIO_LRCLK" />
        <trace from="R67.pin2" to="net.AMP_LRCLK" />
        <trace from="R70.pin1" to="net.AMP_LRCLK" />
        <trace from="R70.pin2" to="net.GND" />
        <trace from="U3.pin14" to="net.AMP_LRCLK" />
      </group>
    </schematicsheet>
  )
}
