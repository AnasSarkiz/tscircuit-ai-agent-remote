import { A_74LVC2G07GW_125 } from "../../imports/A_74LVC2G07GW_125"
import { TPS7A2028PDBVR } from "../../imports/TPS7A2028PDBVR/TPS7A2028PDBVR"
import { GRM188R61A106ME69D } from "../../imports/GRM188R61A106ME69D/GRM188R61A106ME69D"
import { GRM188R71C104KA01D } from "../../imports/GRM188R71C104KA01D/GRM188R71C104KA01D"
import { RC0603FR_07330RL } from "../../imports/RC0603FR_07330RL"
import { RC0603FR_07100RL } from "../../imports/RC0603FR_07100RL/RC0603FR_07100RL"
import { RC0603FR_0710KL } from "../../imports/RC0603FR_0710KL/RC0603FR_0710KL"
import { RC0603FR_07100KL } from "../../imports/RC0603FR_07100KL/RC0603FR_07100KL"
import { RC0603FR_071KL } from "../../imports/RC0603FR_071KL/RC0603FR_071KL"

// Independent application candidate, not integrated into index.circuit.tsx.
// The physical switch and microphones remain absent pending qualification.
// Both clock high levels come only from the hardware-switched VMIC rail.
// Clock capacitance, turn-off timing and partial-power AC injection are unqualified.
export function MicrophoneRegulatedClockReviewSheet() {
  return (
    <schematicsheet
      name="mic-regulated-clock-review"
      displayName="AI Remote A0 — regulated microphone clocks (unrouted candidate)"
      sheetIndex={1}
      sheetSize="A4"
    >
      <group name="mic-regulated-clock-review-group" schLayout={{ layoutMode: "relative" }}>
        <net name="V3V3" isPowerNet />
        <net name="VMIC" isPowerNet />
        <net name="GND" isGroundNet />
        <net name="HOLD_HARDWARE" />
        <net name="MCU_MIC_BCLK" />
        <net name="MCU_MIC_WS" />
        <net name="MIC_BCLK_INPUT" />
        <net name="MIC_WS_INPUT" />
        <net name="MIC_BCLK" />
        <net name="MIC_WS" />
        <TPS7A2028PDBVR name="U23" layer="top" pcbX={-16} pcbY={10} schX={-10} schY={9} />
        <A_74LVC2G07GW_125 name="U24" layer="top" pcbX={-8} pcbY={10} schX={5} schY={9} />
        <GRM188R61A106ME69D
          name="C73"
          layer="top"
          pcbX={0}
          pcbY={10}
          schX={-15}
          schY={4}
          schRotation={-90}
        />
        <GRM188R61A106ME69D
          name="C74"
          layer="top"
          pcbRotation={180}
          pcbX={8}
          pcbY={10}
          schX={-10}
          schY={4}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C75"
          layer="top"
          pcbX={16}
          pcbY={10}
          schX={10}
          schY={9}
          schRotation={-90}
        />
        <RC0603FR_071KL
          name="R86"
          layer="top"
          pcbX={-16}
          pcbY={0}
          schX={-5}
          schY={4}
          schRotation={-90}
        />
        <RC0603FR_07100KL
          name="R87"
          layer="top"
          pcbX={-8}
          pcbY={0}
          schX={-15}
          schY={9}
          schRotation={-90}
        />
        <RC0603FR_07100RL name="R88" layer="top" pcbX={0} pcbY={0} schX={0} schY={4} />
        <RC0603FR_07100RL name="R89" layer="top" pcbX={8} pcbY={0} schX={5} schY={4} />
        <RC0603FR_0710KL
          name="R90"
          layer="top"
          pcbX={16}
          pcbY={0}
          schX={10}
          schY={4}
          schRotation={-90}
        />
        <RC0603FR_0710KL
          name="R91"
          layer="top"
          pcbX={-16}
          pcbY={-10}
          schX={15}
          schY={4}
          schRotation={-90}
        />
        <RC0603FR_07330RL
          name="R92"
          layer="top"
          pcbX={-8}
          pcbY={-10}
          schX={0}
          schY={-2}
          schRotation={-90}
        />
        <RC0603FR_07330RL
          name="R93"
          layer="top"
          pcbX={0}
          pcbY={-10}
          schX={5}
          schY={-2}
          schRotation={-90}
        />
        <RC0603FR_0710KL
          name="R94"
          layer="top"
          pcbX={8}
          pcbY={-10}
          schX={10}
          schY={-2}
          schRotation={-90}
        />
        <RC0603FR_0710KL
          name="R95"
          layer="top"
          pcbX={16}
          pcbY={-10}
          schX={15}
          schY={-2}
          schRotation={-90}
        />
        <trace from="U23.pin1" to="net.V3V3" />
        <trace from="U23.pin2" to="net.GND" />
        <trace from="U23.pin3" to="net.HOLD_HARDWARE" />
        <trace from="U23.pin5" to="net.VMIC" />
        <trace from="U24.pin1" to="net.MIC_BCLK_INPUT" />
        <trace from="U24.pin2" to="net.GND" />
        <trace from="U24.pin3" to="net.MIC_WS_INPUT" />
        <trace from="U24.pin4" to="net.MIC_WS" />
        <trace from="U24.pin5" to="net.VMIC" />
        <trace from="U24.pin6" to="net.MIC_BCLK" />
        <trace from="C73.pin1" to="net.V3V3" />
        <trace from="C73.pin2" to="net.GND" />
        <trace from="C74.pin1" to="net.VMIC" />
        <trace from="C74.pin2" to="net.GND" />
        <trace from="C75.pin1" to="net.VMIC" />
        <trace from="C75.pin2" to="net.GND" />
        <trace from="R86.pin1" to="net.VMIC" />
        <trace from="R86.pin2" to="net.GND" />
        <trace from="R87.pin1" to="net.HOLD_HARDWARE" />
        <trace from="R87.pin2" to="net.GND" />
        <trace from="R88.pin1" to="net.MCU_MIC_BCLK" />
        <trace from="R88.pin2" to="net.MIC_BCLK_INPUT" />
        <trace from="R89.pin1" to="net.MCU_MIC_WS" />
        <trace from="R89.pin2" to="net.MIC_WS_INPUT" />
        <trace from="R90.pin1" to="net.MIC_BCLK_INPUT" />
        <trace from="R90.pin2" to="net.GND" />
        <trace from="R91.pin1" to="net.MIC_WS_INPUT" />
        <trace from="R91.pin2" to="net.GND" />
        <trace from="R92.pin1" to="net.VMIC" />
        <trace from="R92.pin2" to="net.MIC_BCLK" />
        <trace from="R93.pin1" to="net.VMIC" />
        <trace from="R93.pin2" to="net.MIC_WS" />
        <trace from="R94.pin1" to="net.MIC_BCLK" />
        <trace from="R94.pin2" to="net.GND" />
        <trace from="R95.pin1" to="net.MIC_WS" />
        <trace from="R95.pin2" to="net.GND" />
      </group>
    </schematicsheet>
  )
}
