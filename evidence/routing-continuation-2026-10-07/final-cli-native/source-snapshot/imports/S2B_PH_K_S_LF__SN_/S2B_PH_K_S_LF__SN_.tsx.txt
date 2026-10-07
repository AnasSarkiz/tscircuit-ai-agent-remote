import objPath from "./S2B_PH_K_S_LF__SN_.obj"
import stepPath from "./S2B_PH_K_S_LF__SN_.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["pin1"],
  pin2: ["pin2"]
} as const

export const S2B_PH_K_S_LF__SN_ = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C173752"
  ]
}}
      manufacturerPartNumber="S2B-PH-K-S(LF)(SN)"
      footprint={<footprint>
        <platedhole  portHints={["pin1"]} pcbX="0.97499805mm" pcbY="0mm" holeWidth="0.8499856mm" holeHeight="0.8499856mm" outerWidth="1.499997mm" outerHeight="1.3999972mm" rectPad={true} pcbRotation="0deg" shape="pill" />
<platedhole  portHints={["pin2"]} pcbX="-1.02499795mm" pcbY="0mm" outerDiameter="1.3999972mm" holeDiameter="0.8499856mm" shape="circle" />
<silkscreenpath route={[{"x":-3.0249939500000664,"y":6.200013000000126},{"x":2.9749940500000776,"y":6.200013000000126}]} />
<silkscreenpath route={[{"x":-3.0249939500000664,"y":6.200013000000126},{"x":-3.0249939500000664,"y":-1.400022599999943}]} />
<silkscreenpath route={[{"x":2.9749940500000776,"y":-1.400022599999943},{"x":2.9749940500000776,"y":6.159017399999925}]} />
<silkscreenpath route={[{"x":-3.0249939500000664,"y":-1.400022599999943},{"x":-2.0249959499999477,"y":-1.400022599999943},{"x":-2.0249959499999477,"y":0.19999960000006922}]} />
<silkscreenpath route={[{"x":2.9749432500001376,"y":-1.399971800000003},{"x":1.9749452500000189,"y":-1.399971800000003},{"x":1.9749452500000189,"y":0.19999960000006922}]} />
<silkscreenpath route={[{"x":-2.0249959499999477,"y":0.19999960000006922},{"x":-2.0249959499999477,"y":4.000017400000047},{"x":-1.4249717499999406,"y":4.000017400000047},{"x":-1.4249717499999406,"y":0.19999960000006922}]} />
<silkscreenpath route={[{"x":1.3749718500000654,"y":0.19999960000006922},{"x":1.3749718500000654,"y":4.000017400000047},{"x":1.9749960499999588,"y":4.000017400000047},{"x":1.9749960499999588,"y":0.19999960000006922}]} />
<silkscreenpath route={[{"x":-1.0249979499999426,"y":6.200013000000126},{"x":-1.0249979499999426,"y":1.8999962000000323},{"x":0.9749980499999538,"y":1.8999962000000323},{"x":0.9749980499999538,"y":6.100038600000062}]} />
<silkscreenpath route={[{"x":-2.0249959499999477,"y":0.19999960000006922},{"x":-2.006149149999942,"y":0.19999960000006922}]} />
<silkscreenpath route={[{"x":-0.043846750000057,"y":0.19999960000006922},{"x":-0.006153149999931884,"y":0.19999960000006922}]} />
<silkscreenpath route={[{"x":1.956149249999953,"y":0.19999960000006922},{"x":1.9749452500000189,"y":0.19999960000006922}]} />
<silkscreentext text="{NAME}" pcbX="0.02580005mm" pcbY="7.2992mm" anchorAlignment="center" fontSize="1mm" />
<fabricationnotepath route={[{"x":3.1749936499999194,"y":6.30001279999999},{"x":3.1749936499999194,"y":2.099995799999988},{"x":3.1749936499999194,"y":6.30001279999999}]} strokeWidth="0.254mm" />
<courtyardoutline outline={[{"x":-3.2749939500000664,"y":6.524993799999947},{"x":3.2249940500000776,"y":6.524993799999947},{"x":3.2249940500000776,"y":-1.6749907999999323},{"x":-3.2749939500000664,"y":-1.6749907999999323},{"x":-3.2749939500000664,"y":6.524993799999947}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 180,
        modelOriginPosition: { x: 0.9750000500000624, y: 0.02500150000000767, z: -0.000006999999999646178 },
      }}
      {...props}
    />
  )
}