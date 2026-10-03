import { TPS7A2030PDBVR } from "../../imports/TPS7A2030PDBVR"
import { AO3400A } from "../../imports/AO3400A/AO3400A"
import { SS14 } from "../../imports/SS14"
import { RC0603FR_071KL } from "../../imports/RC0603FR_071KL/RC0603FR_071KL"
import { RC0603FR_0710KL } from "../../imports/RC0603FR_0710KL/RC0603FR_0710KL"
import { RC0603FR_07100KL } from "../../imports/RC0603FR_07100KL/RC0603FR_07100KL"
import { RC0603FR_07100RL } from "../../imports/RC0603FR_07100RL/RC0603FR_07100RL"
import { GRM188R61A106ME69D } from "../../imports/GRM188R61A106ME69D/GRM188R61A106ME69D"
import { GRM188R61A226ME15D } from "../../imports/GRM188R61A226ME15D/GRM188R61A226ME15D"
import { GRM188R71C104KA01D } from "../../imports/GRM188R71C104KA01D/GRM188R71C104KA01D"

// Independent, unrouted regulator and flyback application review.
// The motor remains absent: C2942347 body/model qualification is blocked by B-014.
// Three-volt accuracy requires VSYS >= 3.3 V and an enabled load >= 1 mA.
// Battery cutoff, startup/stall current and switch-off transients remain unqualified.
export function HapticDriverReviewSheet() {
  return (
    <schematicsheet
      name="haptic-driver-review"
      displayName="AI Remote A0 — haptic driver review (unrouted)"
      sheetIndex={1}
      sheetSize="A4"
    >
      <group name="haptic-driver-review-group" schLayout={{ layoutMode: "relative" }}>
        <net name="GND" isGroundNet />
        <net name="VSYS" isPowerNet />
        <net name="VMOTOR" isPowerNet />
        <net name="MCU_HAPTIC_ENABLE" />
        <net name="HAPTIC_NMOS_GATE" />
        <net name="HAPTIC_N" />
        <TPS7A2030PDBVR name="U22" layer="top" pcbX={-8} pcbY={0} schX={-6} schY={2} />
        <AO3400A name="Q9" layer="top" pcbX={5} pcbY={0} schX={6} schY={-2} />
        <SS14 name="D3" layer="top" pcbX={12} pcbY={0} schX={11} schY={2} schRotation={90} />
        <GRM188R61A106ME69D
          name="C70"
          layer="top"
          pcbX={-14}
          pcbY={5}
          schX={-11}
          schY={2}
          schRotation={-90}
        />
        <GRM188R61A226ME15D
          name="C71"
          layer="top"
          pcbX={-1}
          pcbY={5}
          schX={0}
          schY={2}
          schRotation={-90}
        />
        <GRM188R71C104KA01D
          name="C72"
          layer="top"
          pcbX={12}
          pcbY={6}
          schX={15}
          schY={2}
          schRotation={-90}
        />
        <RC0603FR_071KL
          name="R82"
          layer="top"
          pcbX={-1}
          pcbY={-5}
          schX={3}
          schY={2}
          schRotation={-90}
        />
        <RC0603FR_07100RL name="R83" layer="top" pcbX={5} pcbY={-8} schX={1} schY={-6} />
        <RC0603FR_0710KL
          name="R84"
          layer="top"
          pcbX={10}
          pcbY={-5}
          schX={6}
          schY={-6}
          schRotation={-90}
        />
        <RC0603FR_07100KL
          name="R85"
          layer="top"
          pcbX={-8}
          pcbY={-5}
          schX={-6}
          schY={-6}
          schRotation={-90}
        />
        <trace from="U22.pin1" to="net.VSYS" />
        <trace from="U22.pin2" to="net.GND" />
        <trace from="U22.pin3" to="net.MCU_HAPTIC_ENABLE" />
        <trace from="U22.pin5" to="net.VMOTOR" />
        <trace from="Q9.pin1" to="net.HAPTIC_NMOS_GATE" />
        <trace from="Q9.pin2" to="net.GND" />
        <trace from="Q9.pin3" to="net.HAPTIC_N" />
        <trace from="D3.pin1" to="net.VMOTOR" />
        <trace from="D3.pin2" to="net.HAPTIC_N" />
        <trace from="C70.pin1" to="net.VSYS" />
        <trace from="C70.pin2" to="net.GND" />
        <trace from="C71.pin1" to="net.VMOTOR" />
        <trace from="C71.pin2" to="net.GND" />
        <trace from="C72.pin1" to="net.VMOTOR" />
        <trace from="C72.pin2" to="net.HAPTIC_N" />
        <trace from="R82.pin1" to="net.VMOTOR" />
        <trace from="R82.pin2" to="net.GND" />
        <trace from="R83.pin1" to="net.MCU_HAPTIC_ENABLE" />
        <trace from="R83.pin2" to="net.HAPTIC_NMOS_GATE" />
        <trace from="R84.pin1" to="net.HAPTIC_NMOS_GATE" />
        <trace from="R84.pin2" to="net.GND" />
        <trace from="R85.pin1" to="net.MCU_HAPTIC_ENABLE" />
        <trace from="R85.pin2" to="net.GND" />
      </group>
    </schematicsheet>
  )
}
