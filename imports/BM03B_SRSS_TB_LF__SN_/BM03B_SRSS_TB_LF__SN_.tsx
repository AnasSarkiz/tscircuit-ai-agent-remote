import objPath from "./BM03B_SRSS_TB_LF__SN_.obj"
import stepPath from "./BM03B_SRSS_TB_LF__SN_.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["pin1"],
  pin2: ["pin2"],
  pin3: ["pin3"],
  pin4: ["pin4"],
  pin5: ["pin5"]
} as const

export const BM03B_SRSS_TB_LF__SN_ = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C160389"
  ]
}}
      manufacturerPartNumber="BM03B-SRSS-TB(LF)(SN)"
      footprint={<footprint>
        <smtpad portHints={["pin5"]} pcbX="-2.299843mm" pcbY="-1.2000103mm" width="1.1999976mm" height="1.7999964mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="2.299843mm" pcbY="-1.1997563mm" width="1.1999976mm" height="1.7999964mm" shape="rect" />
<smtpad portHints={["pin1"]} pcbX="1.000125mm" pcbY="1.3250037mm" width="0.5999988mm" height="1.5500096mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="0.000127mm" pcbY="1.3250037mm" width="0.5999988mm" height="1.5500096mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="-0.999871mm" pcbY="1.3250037mm" width="0.5999988mm" height="1.5500096mm" shape="rect" />
<silkscreenpath route={[{"x":-1.5002509999999347,"y":2.0260437000000593},{"x":-2.8007563999999547,"y":2.0260437000000593},{"x":-2.799816599999872,"y":-0.03752849999978025}]} />
<silkscreenpath route={[{"x":-2.8007563999999547,"y":-2.2741508999998814},{"x":2.8011374000002434,"y":-2.2741508999998814}]} />
<silkscreenpath route={[{"x":1.5001240000001417,"y":2.0625181000001476},{"x":2.800146800000107,"y":2.0625181000001476},{"x":2.800146800000107,"y":-0.03752849999978025}]} />
<silkscreencircle pcbX="1.524mm" pcbY="2.3484967mm" radius="0.127mm" />
<silkscreentext text="{NAME}" pcbX="-0.013843mm" pcbY="3.4829897mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-3.1498417999998765,"y":2.350008500000058},{"x":3.14984179999999,"y":2.350008500000058},{"x":3.14984179999999,"y":-2.3500084999999444},{"x":-3.1498417999998765,"y":-2.3500084999999444},{"x":-3.1498417999998765,"y":2.350008500000058}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 180,
        modelOriginPosition: { x: 1.0000000000002274, y: -0.43250299999996966, z: -0.01 },
      }}
      {...props}
    />
  )
}