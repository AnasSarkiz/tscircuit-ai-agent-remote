import objPath from "./SN74LVC1G125DBVR.obj"
import stepPath from "./SN74LVC1G125DBVR.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["OE"],
  pin2: ["A"],
  pin3: ["GND"],
  pin4: ["Y"],
  pin5: ["VCC"]
} as const

const pinAttributes = {
  pin3: {requiresGround: true},
  pin5: {requiresPower: true}
} as const

export const SN74LVC1G125DBVR = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C23654"
  ]
}}
      manufacturerPartNumber="SN74LVC1G125DBVR"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="-0.94996mm" pcbY="-1.15817015mm" width="0.4899914mm" height="1.1569954mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="0mm" pcbY="-1.15817015mm" width="0.4899914mm" height="1.1569954mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="0.94996mm" pcbY="-1.15817015mm" width="0.4899914mm" height="1.1569954mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="0.94996mm" pcbY="1.14916585mm" width="0.4899914mm" height="1.175004mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="-0.94996mm" pcbY="1.14916585mm" width="0.4899914mm" height="1.175004mm" shape="rect" />
<silkscreenpath route={[{"x":-1.5262098000000606,"y":-0.8557069500000125},{"x":-1.5262098000000606,"y":0.8467026499999974}]} />
<silkscreenpath route={[{"x":1.5262097999998332,"y":-0.8557069500000125},{"x":1.5262097999998332,"y":0.8467026499999974}]} />
<silkscreenpath route={[{"x":0.4764023999998699,"y":0.8467026499999974},{"x":-0.4764023999999836,"y":0.8467026499999974}]} />
<silkscreencircle pcbX="-1.651mm" pcbY="-1.14750215mm" radius="0.150114mm" />
<silkscreentext text="{NAME}" pcbX="-0.1397mm" pcbY="2.74809785mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-2.0534000000000106,"y":1.998097850000022},{"x":1.7739999999998872,"y":1.998097850000022},{"x":1.7739999999998872,"y":-2.108702149999999},{"x":-2.0534000000000106,"y":-2.108702149999999},{"x":-2.0534000000000106,"y":1.998097850000022}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 90,
        modelOriginPosition: { x: 0.004489450000050965, y: 0.000012700000070253736, z: -0.049083 },
      }}
      {...props}
    />
  )
}