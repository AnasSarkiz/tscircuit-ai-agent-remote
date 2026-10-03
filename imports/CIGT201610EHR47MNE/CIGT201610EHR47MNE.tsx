import objPath from "./CIGT201610EHR47MNE.obj"
import stepPath from "./CIGT201610EHR47MNE.step"
import type { InductorProps } from "@tscircuit/props"

export const CIGT201610EHR47MNE = (props: Omit<InductorProps, "inductance">) => {
  return (
    <inductor
      inductance="470nH"
      supplierPartNumbers={{
  "jlcpcb": [
    "C16195750"
  ]
}}
      manufacturerPartNumber="CIGT201610EHR47MNE"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="-0.750062mm" pcbY="0mm" width="0.7999984mm" height="1.7999964mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="0.750062mm" pcbY="0mm" width="0.7999984mm" height="1.7999964mm" shape="rect" />
<silkscreenpath route={[{"x":-0.999998000000005,"y":1.150010400000042},{"x":0.999998000000005,"y":1.150010400000042}]} />
<silkscreenpath route={[{"x":0.999998000000005,"y":-1.1500103999999283},{"x":-0.999998000000005,"y":-1.1500103999999283}]} />
<silkscreentext text="{NAME}" pcbX="0.0127mm" pcbY="2.143mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-1.400061199999982,"y":1.1499982000000273},{"x":1.400061199999982,"y":1.1499982000000273},{"x":1.400061199999982,"y":-1.1499982000000273},{"x":-1.400061199999982,"y":-1.1499982000000273},{"x":-1.400061199999982,"y":1.1499982000000273}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 0, y: 0, z: -0.01 },
      }}
      {...props}
    />
  )
}