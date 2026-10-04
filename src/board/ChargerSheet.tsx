import { BQ24074RGTR } from "../../imports/BQ24074RGTR/BQ24074RGTR"
import { GRM188R61A106ME69D } from "../../imports/GRM188R61A106ME69D/GRM188R61A106ME69D"
import { RC0603FR_07100KL } from "../../imports/RC0603FR_07100KL/RC0603FR_07100KL"
import { RC0603FR_073KL } from "../../imports/RC0603FR_073KL/RC0603FR_073KL"
import { S3B_PH_SM4_TB_LF__SN_ } from "../../imports/S3B_PH_SM4_TB_LF__SN_/S3B_PH_SM4_TB_LF__SN_"
import { place } from "./placement"
export function ChargerSheet() {
  return (
    <schematicsheet
      name="ChargerSheet"
      displayName="AI Remote A1 - USB100 charging - PACK PROVISIONAL"
      sheetSize="A4"
      sheetIndex={2}
    >
      <group name="ChargerSheet-group" schLayout={{ layoutMode: "relative" }}>
        <BQ24074RGTR name="U16" {...place("U16")} schX={0} schY={0} />
        <S3B_PH_SM4_TB_LF__SN_ name="J3" {...place("J3")} schX={10} schY={3} />
        <GRM188R61A106ME69D name="C1" {...place("C1")} schX={-9} schY={5} />
        <GRM188R61A106ME69D name="C2" {...place("C2")} schX={5} schY={5} />
        <GRM188R61A106ME69D name="C3" {...place("C3")} schX={5} schY={-5} />
        <RC0603FR_073KL name="R1" {...place("R1")} schX={-6} schY={-6} />
        <RC0603FR_073KL name="R2" {...place("R2")} schX={-9} schY={-6} />
        <RC0603FR_07100KL name="R3" {...place("R3")} schX={-12} schY={0} />
        <RC0603FR_07100KL name="R4" {...place("R4")} schX={-12} schY={3} />
        <trace from="U16.pin1" to="net.PACK_NTC" />
        <trace from="U16.pin2" to="net.PACK_BAT" />
        <trace from="U16.pin3" to="net.PACK_BAT" />
        <trace from="U16.pin4" to="net.GND" />
        <trace from="U16.pin5" to="net.GND" />
        <trace from="U16.pin6" to="net.GND" />
        <trace from="U16.pin7" to="net.CHARGE_PGOOD_N" />
        <trace from="U16.pin8" to="net.GND" />
        <trace from="U16.pin9" to="net.CHARGE_STATUS_N" />
        <trace from="U16.pin10" to="net.VSYS" />
        <trace from="U16.pin11" to="net.VSYS" />
        <trace from="U16.pin12" to="net.CHARGER_ILIM" />
        <trace from="U16.pin13" to="net.VBUS" />
        <trace from="U16.pin16" to="net.CHARGER_ISET" />
        <trace from="U16.pin17" to="net.GND" />
        {/* AKY2945: outer BAT/GND contact numbers require supplier or physical confirmation. */}
        <trace from="J3.pin2" to="net.PACK_NTC" />
        <trace from="J3.pin4" to="net.GND" />
        <trace from="C1.pin1" to="net.VBUS" />
        <trace from="C1.pin2" to="net.GND" />
        <trace from="C2.pin1" to="net.PACK_BAT" />
        <trace from="C2.pin2" to="net.GND" />
        <trace from="C3.pin1" to="net.VSYS" />
        <trace from="C3.pin2" to="net.GND" />
        <trace from="R1.pin1" to="net.CHARGER_ISET" />
        <trace from="R1.pin2" to="net.GND" />
        <trace from="R2.pin1" to="net.CHARGER_ILIM" />
        <trace from="R2.pin2" to="net.GND" />
        <trace from="R3.pin1" to="net.V3V3" />
        <trace from="R3.pin2" to="net.CHARGE_PGOOD_N" />
        <trace from="R4.pin1" to="net.V3V3" />
        <trace from="R4.pin2" to="net.CHARGE_STATUS_N" />
      </group>
    </schematicsheet>
  )
}
