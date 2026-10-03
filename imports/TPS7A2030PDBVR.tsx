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

export const TPS7A2030PDBVR = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C963429"
  ]
}}
      manufacturerPartNumber="TPS7A2030PDBVR"
      footprint="dfn6_missing(5)_p0.95mm_w3.69mm_pw0.7mm_pl1.1mm_pin1location(rightside,bottom)"
      cadModel={{
        objUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C963429.obj?uuid=c7fdf6dae3ca4abaabd1bafd2d31350d",
        stepUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C963429.step?uuid=c7fdf6dae3ca4abaabd1bafd2d31350d",
        pcbRotationOffset: 180,
        modelOriginPosition: { x: 0, y: 0.0001142999999501626, z: 0.050795 },
      }}
      {...props}
    />
  )
}