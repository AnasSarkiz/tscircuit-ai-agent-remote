import objPath from "./RC0603FR_074K7L.obj"
import stepPath from "./RC0603FR_074K7L.step"
import type { ResistorProps } from "@tscircuit/props"

export const RC0603FR_074K7L = (props: Omit<ResistorProps, "resistance">) => {
  const { name = "R1", ...restProps } = props

  return (
    <resistor
      name={name}
      resistance="4.7kohm"
      supplierPartNumbers={{
  "jlcpcb": [
    "C99782"
  ]
}}
      manufacturerPartNumber="RC0603FR-074K7L"
      footprint="smdpads2_p1.5067mm_pw0.8065mm_ph0.864mm_cyw2.8132mm_cyh1.364mm"
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 90,
        modelOriginPosition: { x: -0.004999999999999977, y: 0, z: -0.01 },
      }}
      {...restProps}
    />
  )
}