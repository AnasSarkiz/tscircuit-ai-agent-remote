import objPath from "./TLV75728PDBVR.obj"
import stepPath from "./TLV75728PDBVR.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["IN"],
  pin2: ["GND"],
  pin3: ["EN"],
  pin4: ["NC"],
  pin5: ["OUT"]
} as const

const pinAttributes = {
  pin2: {requiresGround: true},
  pin4: {doNotConnect: true}
} as const

export const TLV75728PDBVR = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C2863639"
  ]
}}
      manufacturerPartNumber="TLV75728PDBVR"
      footprint="sot25_w2.2mm_pl1mm_pin1location(leftside,bottom)"
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 0, y: 0, z: -0.75 },
      }}
      {...props}
    />
  )
}