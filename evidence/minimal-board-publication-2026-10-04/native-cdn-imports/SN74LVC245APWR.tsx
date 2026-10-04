import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["DIR"],
  pin2: ["A1"],
  pin3: ["A2"],
  pin4: ["A3"],
  pin5: ["A4"],
  pin6: ["A5"],
  pin7: ["A6"],
  pin8: ["A7"],
  pin9: ["A8"],
  pin10: ["GND"],
  pin11: ["B8"],
  pin12: ["B7"],
  pin13: ["B6"],
  pin14: ["B5"],
  pin15: ["B4"],
  pin16: ["B3"],
  pin17: ["B2"],
  pin18: ["B1"],
  pin19: ["N_OE"],
  pin20: ["VCC"]
} as const

const pinAttributes = {
  pin10: {requiresGround: true},
  pin20: {requiresPower: true}
} as const

export const SN74LVC245APWR = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C7848"
  ]
}}
      manufacturerPartNumber="SN74LVC245APWR"
      footprint="tssop20_p0.65mm_w3.9999mm_pw0.364mm_pl1.742mm_rounded0.182mm_pin1location(leftside,bottom)"
      cadModel={{
        objUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C7848.obj?uuid=f8ba5b4174b9490d8c445fbe2ed40b80",
        stepUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C7848.step?uuid=f8ba5b4174b9490d8c445fbe2ed40b80",
        pcbRotationOffset: 90,
        modelOriginPosition: { x: 0, y: 0.000012700000070253736, z: -0.019205 },
      }}
      {...props}
    />
  )
}