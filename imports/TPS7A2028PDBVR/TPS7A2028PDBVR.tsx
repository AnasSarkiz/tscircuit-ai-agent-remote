import objPath from "./TPS7A2028PDBVR.obj"
import stepPath from "./TPS7A2028PDBVR.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["IN"],
  pin2: ["GND"],
  pin3: ["EN"],
  pin4: ["N","C"],
  pin5: ["OUT"]
} as const

const pinAttributes = {
  pin2: {requiresGround: true}
} as const

export const TPS7A2028PDBVR = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C2869847"
  ]
}}
      manufacturerPartNumber="TPS7A2028PDBVR"
      footprint="sot25_w2.2mm_pl1mm_pin1location(rightside,bottom)"
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 90,
        modelOriginPosition: { x: -0.000012699999956566899, y: 0.00006349999989652133, z: -0.7 },
      }}
      {...props}
    />
  )
}