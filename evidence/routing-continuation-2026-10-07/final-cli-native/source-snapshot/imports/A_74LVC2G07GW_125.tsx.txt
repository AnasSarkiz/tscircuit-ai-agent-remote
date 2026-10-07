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

export const A_74LVC2G07GW_125 = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C24478"
  ]
}}
      manufacturerPartNumber="74LVC2G07GW,125"
      footprint="dfn6_p0.65mm_w2.6998mm_pw0.4mm_pl0.9mm_pin1location(rightside,bottom)"
      cadModel={{
        objUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C24478.obj?uuid=c48363a009b446bc89c236a3f3be363d",
        stepUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C24478.step?uuid=c48363a009b446bc89c236a3f3be363d",
        pcbRotationOffset: 90,
        modelOriginPosition: { x: 0.0001015999999935957, y: 0.00008889999999439624, z: 0 },
      }}
      {...props}
    />
  )
}