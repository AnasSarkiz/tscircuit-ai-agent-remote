import type { ResistorProps } from "@tscircuit/props"

export const RC0603FR_0751K1L = (props: Omit<ResistorProps, "resistance">) => {
  const { name = "R1", ...restProps } = props

  return (
    <resistor
      name={name}
      resistance="51.1kohm"
      supplierPartNumbers={{
  "jlcpcb": [
    "C364359"
  ]
}}
      manufacturerPartNumber="RC0603FR-0751K1L"
      footprint="smdpads2_p1.5067mm_pw0.8065mm_ph0.864mm_cyw2.8132mm_cyh1.364mm"
      cadModel={{
        objUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C364359.obj?uuid=6bd5cd867e9542ebae21caaf5d2d4c4d",
        stepUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C364359.step?uuid=6bd5cd867e9542ebae21caaf5d2d4c4d",
        pcbRotationOffset: 90,
        modelOriginPosition: { x: -0.004999999999999977, y: 0, z: -0.01 },
      }}
      {...restProps}
    />
  )
}