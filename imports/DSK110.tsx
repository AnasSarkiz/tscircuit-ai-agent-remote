import type { DiodeProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["anode","pos"],
  pin2: ["cathode","neg"]
} as const

export const DSK110 = (props: DiodeProps) => {
  const { name = "D1", ...restProps } = props

  return (
    <diode
      name={name}
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C908227"
  ]
}}
      manufacturerPartNumber="DSK110"
      footprint="smdpads2_p3.4mm_pw1.2mm_ph1.4mm"
      cadModel={{
        objUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C908227.obj?uuid=440d24646afe4714aa0c5451b02577ae",
        stepUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C908227.step?uuid=440d24646afe4714aa0c5451b02577ae",
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 0.000012699999999199463, y: 0, z: 0.09 },
      }}
      {...restProps}
    />
  )
}