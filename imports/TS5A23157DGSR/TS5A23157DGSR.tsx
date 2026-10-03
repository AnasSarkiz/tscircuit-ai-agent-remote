import objPath from "./TS5A23157DGSR.obj"
import stepPath from "./TS5A23157DGSR.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["IN_1"],
  pin2: ["NO_1"],
  pin3: ["GND"],
  pin4: ["NO_2"],
  pin5: ["IN_2"],
  pin6: ["COM2"],
  pin7: ["NC_2"],
  pin8: ["V_POS"],
  pin9: ["NC_1"],
  pin10: ["COM_1"]
} as const

const pinAttributes = {
  pin3: {requiresGround: true}
} as const

export const TS5A23157DGSR = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C11133"
  ]
}}
      manufacturerPartNumber="TS5A23157DGSR"
      footprint="dfn10_pillpads_p0.5mm_w5.84mm_pw0.28mm_pl1.62mm_pin1location(leftside,bottom)"
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 0, y: 0, z: 0 },
      }}
      {...props}
    />
  )
}