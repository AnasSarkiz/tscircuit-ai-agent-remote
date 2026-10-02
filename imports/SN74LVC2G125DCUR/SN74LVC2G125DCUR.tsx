import objPath from "./SN74LVC2G125DCUR.obj"
import stepPath from "./SN74LVC2G125DCUR.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["N_1OE"],
  pin2: ["1A"],
  pin3: ["2Y"],
  pin4: ["GND"],
  pin5: ["2A"],
  pin6: ["1Y"],
  pin7: ["N_2OE"],
  pin8: ["VCC"]
} as const

const pinAttributes = {
  pin4: {requiresGround: true},
  pin8: {requiresPower: true}
} as const

export const SN74LVC2G125DCUR = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C21404"
  ]
}}
      manufacturerPartNumber="SN74LVC2G125DCUR"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="-0.762mm" pcbY="-1.550035mm" width="0.2500122mm" height="0.700024mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="-0.254mm" pcbY="-1.550035mm" width="0.2500122mm" height="0.700024mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="0.254mm" pcbY="-1.550035mm" width="0.2500122mm" height="0.700024mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="0.762mm" pcbY="-1.550035mm" width="0.2500122mm" height="0.700024mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="0.762mm" pcbY="1.550035mm" width="0.2500122mm" height="0.700024mm" shape="rect" />
<smtpad portHints={["pin6"]} pcbX="0.254mm" pcbY="1.550035mm" width="0.2500122mm" height="0.700024mm" shape="rect" />
<smtpad portHints={["pin7"]} pcbX="-0.254mm" pcbY="1.550035mm" width="0.2500122mm" height="0.700024mm" shape="rect" />
<smtpad portHints={["pin8"]} pcbX="-0.762mm" pcbY="1.550035mm" width="0.2500122mm" height="0.700024mm" shape="rect" />
<silkscreenpath route={[{"x":1.1998706000000539,"y":1.0001250000000255},{"x":1.1998706000000539,"y":-0.9998709999999846}]} />
<silkscreenpath route={[{"x":-1.2000484000000142,"y":-0.9998709999999846},{"x":-1.2000484000000142,"y":1.0001250000000255}]} />
<silkscreenpath route={[{"x":-1.2000484000000142,"y":-0.9998709999999846},{"x":-1.0003028000000995,"y":-0.9998709999999846}]} />
<silkscreenpath route={[{"x":-0.5239512000000559,"y":-0.9998709999999846},{"x":-0.4923028000000613,"y":-0.9998709999999846}]} />
<silkscreenpath route={[{"x":-0.015951200000017707,"y":-0.9998709999999846},{"x":0.015697199999976874,"y":-0.9998709999999846}]} />
<silkscreenpath route={[{"x":0.4920487999999068,"y":-0.9998709999999846},{"x":0.5236971999999014,"y":-0.9998709999999846}]} />
<silkscreenpath route={[{"x":1.0000487999998313,"y":-0.9998709999999846},{"x":1.1998706000000539,"y":-0.9998709999999846}]} />
<silkscreenpath route={[{"x":-1.2000484000000142,"y":1.0001250000000255},{"x":-1.0003028000000995,"y":1.0001250000000255}]} />
<silkscreenpath route={[{"x":-0.5239512000000559,"y":1.0001250000000255},{"x":-0.4923028000000613,"y":1.0001250000000255}]} />
<silkscreenpath route={[{"x":-0.015951200000017707,"y":1.0001250000000255},{"x":0.015697199999976874,"y":1.0001250000000255}]} />
<silkscreenpath route={[{"x":0.4920487999999068,"y":1.0001250000000255},{"x":0.5236971999999014,"y":1.0001250000000255}]} />
<silkscreenpath route={[{"x":1.0000487999998313,"y":1.0001250000000255},{"x":1.1998706000000539,"y":1.0001250000000255}]} />
<silkscreencircle pcbX="-1.27mm" pcbY="-1.777873mm" radius="0.0999998mm" />
<silkscreentext text="{NAME}" pcbX="-0.089154mm" pcbY="2.905127mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-1.6218539999999848,"y":2.155126999999993},{"x":1.4435459999998557,"y":2.155126999999993},{"x":1.4435459999998557,"y":-2.1548729999999523},{"x":-1.6218539999999848,"y":-2.1548729999999523},{"x":-1.6218539999999848,"y":2.155126999999993}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 270,
        modelOriginPosition: { x: 0.00011430000006384944, y: 0.00012700000002041634, z: 0.000795 },
      }}
      {...props}
    />
  )
}