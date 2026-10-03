import objPath from "./RC2010JK_07510KL.obj"
import stepPath from "./RC2010JK_07510KL.step"
import type { ResistorProps } from "@tscircuit/props"

export const RC2010JK_07510KL = (props: Omit<ResistorProps, "resistance">) => {
  const { name = "R1", ...restProps } = props

  return (
    <resistor
      name={name}
      resistance="510kohm"
      supplierPartNumbers={{
  "jlcpcb": [
    "C326810"
  ]
}}
      manufacturerPartNumber="RC2010JK-07510KL"
      footprint={<footprint>
        <smtpad portHints={["pin2"]} pcbX="2.391156mm" pcbY="0mm" width="1.2825222mm" height="2.6999946mm" shape="rect" />
<smtpad portHints={["pin1"]} pcbX="-2.391156mm" pcbY="0mm" width="1.2825222mm" height="2.6999946mm" shape="rect" />
<silkscreenpath route={[{"x":1.8262091999999939,"y":-1.578610000000026},{"x":3.261131399999954,"y":-1.578610000000026},{"x":3.261131399999954,"y":1.578610000000026},{"x":1.8262091999999939,"y":1.578610000000026}]} />
<silkscreenpath route={[{"x":-1.8262092000001076,"y":-1.578610000000026},{"x":-3.2611314000000675,"y":-1.578610000000026},{"x":-3.2611314000000675,"y":1.578610000000026},{"x":-1.8262092000001076,"y":1.578610000000026}]} />
<silkscreentext text="{NAME}" pcbX="0.0127mm" pcbY="2.5748mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-3.282417099999975,"y":1.599997300000041},{"x":3.2824170999998614,"y":1.599997300000041},{"x":3.2824170999998614,"y":-1.599997300000041},{"x":-3.282417099999975,"y":-1.599997300000041},{"x":-3.282417099999975,"y":1.599997300000041}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 0, y: 0.000012699999842880061, z: 0 },
      }}
      {...restProps}
    />
  )
}