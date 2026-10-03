import objPath from "./A_0603WAF1002T5E.obj"
import stepPath from "./A_0603WAF1002T5E.step"
import type { ResistorProps } from "@tscircuit/props"

export const A_0603WAF1002T5E = (props: Omit<ResistorProps, "resistance">) => {
  const { name = "R1", ...restProps } = props

  return (
    <resistor
      name={name}
      resistance="10kohm"
      supplierPartNumbers={{
  "jlcpcb": [
    "C25804"
  ]
}}
      manufacturerPartNumber="0603WAF1002T5E"
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