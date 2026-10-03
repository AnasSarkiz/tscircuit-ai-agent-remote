import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["1A"],
  pin2: ["GND"],
  pin3: ["2A"],
  pin4: ["2Y"],
  pin5: ["VCC"],
  pin6: ["1Y"]
} as const

const pinAttributes = {
  pin2: {requiresGround: true},
  pin5: {requiresPower: true}
} as const

export const SN74LVC2G07DCKR = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C7849"
  ]
}}
      manufacturerPartNumber="SN74LVC2G07DCKR"
      footprint="dfn6_p0.65mm_w2.7321mm_pw0.315mm_pl0.841mm_pin1location(rightside,bottom)"
      cadModel={{
        objUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C7849.obj?uuid=7a0f6368eaad4f179b3263108385ad41",
        stepUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C7849.step?uuid=7a0f6368eaad4f179b3263108385ad41",
        pcbRotationOffset: 180,
        modelOriginPosition: { x: -0.000012700000070253736, y: 0, z: -0.1 },
      }}
      {...props}
    />
  )
}