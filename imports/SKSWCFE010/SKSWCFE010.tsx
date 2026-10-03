import objPath from "./SKSWCFE010.obj"
import stepPath from "./SKSWCFE010.step"
import type { PushButtonProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["pin1"],
  pin2: ["pin2"]
} as const

export const SKSWCFE010 = (props: PushButtonProps<typeof pinLabels>) => {
  const { name = "SW1", ...restProps } = props

  return (
    <pushbutton
      name={name}
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C255576"
  ]
}}
      manufacturerPartNumber="SKSWCFE010"
      footprint={<footprint>
        <smtpad portHints={["pin2"]} pcbX="1.650492mm" pcbY="0mm" width="0.7999984mm" height="1.524mm" shape="rect" />
<smtpad portHints={["pin1"]} pcbX="-1.650492mm" pcbY="0mm" width="0.7999984mm" height="1.524mm" shape="rect" />
<silkscreenpath route={[{"x":1.499488999999926,"y":1.0000234000000319},{"x":-1.500530400000116,"y":1.0000234000000319}]} />
<silkscreenpath route={[{"x":-1.5005050000000892,"y":-0.9999725999999782},{"x":1.499488999999926,"y":-0.9999725999999782}]} />
<silkscreencircle pcbX="-0.000508mm" pcbY="0mm" radius="0.635mm" />
<silkscreentext text="{NAME}" pcbX="-0.017018mm" pcbY="1.991616mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-2.3004912000000104,"y":1.249998000000005},{"x":2.3004912000000104,"y":1.249998000000005},{"x":2.3004912000000104,"y":-1.249998000000005},{"x":-2.3004912000000104,"y":-1.249998000000005},{"x":-2.3004912000000104,"y":1.249998000000005}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 0.000012700000070253736, y: 0.0004999999999999449, z: -0.285 },
      }}
      {...restProps}
    />
  )
}