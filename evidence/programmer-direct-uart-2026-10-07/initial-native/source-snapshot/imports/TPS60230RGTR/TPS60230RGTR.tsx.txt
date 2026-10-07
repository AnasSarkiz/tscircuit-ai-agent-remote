import objPath from "./TPS60230RGTR.obj"
import stepPath from "./TPS60230RGTR.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["ISET"],
  pin2: ["D5"],
  pin3: ["D4"],
  pin4: ["D3"],
  pin5: ["D2"],
  pin6: ["D1"],
  pin7: ["PGND"],
  pin8: ["VOUT"],
  pin9: ["C2_POS"],
  pin10: ["C1_POS"],
  pin11: ["C1_NEG"],
  pin12: ["C2_NEG"],
  pin13: ["VIN"],
  pin14: ["GND"],
  pin15: ["EN1"],
  pin16: ["EN2"],
  pin17: ["EP"]
} as const

const pinAttributes = {
  pin7: {requiresGround: true},
  pin13: {requiresPower: true},
  pin14: {requiresGround: true}
} as const

export const TPS60230RGTR = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C1848364"
  ]
}}
      manufacturerPartNumber="TPS60230RGTR"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="-1.499997mm" pcbY="0.750189mm" width="0.7999984mm" height="0.270002mm" radius="0.135001mm" shape="pill" />
<smtpad portHints={["pin2"]} pcbX="-1.499997mm" pcbY="0.250063mm" width="0.7999984mm" height="0.270002mm" radius="0.135001mm" shape="pill" />
<smtpad portHints={["pin3"]} pcbX="-1.499997mm" pcbY="-0.249809mm" width="0.7999984mm" height="0.270002mm" radius="0.135001mm" shape="pill" />
<smtpad portHints={["pin4"]} pcbX="-1.499997mm" pcbY="-0.749935mm" width="0.7999984mm" height="0.270002mm" radius="0.135001mm" shape="pill" />
<smtpad portHints={["pin5"]} pcbX="-0.750189mm" pcbY="-1.499997mm" width="0.2800096mm" height="0.850011mm" radius="0.1400048mm" shape="pill" />
<smtpad portHints={["pin6"]} pcbX="-0.250063mm" pcbY="-1.499997mm" width="0.2800096mm" height="0.850011mm" radius="0.1400048mm" shape="pill" />
<smtpad portHints={["pin7"]} pcbX="0.249809mm" pcbY="-1.499997mm" width="0.2800096mm" height="0.850011mm" radius="0.1400048mm" shape="pill" />
<smtpad portHints={["pin8"]} pcbX="0.749935mm" pcbY="-1.499997mm" width="0.2800096mm" height="0.850011mm" radius="0.1400048mm" shape="pill" />
<smtpad portHints={["pin9"]} pcbX="1.499997mm" pcbY="-0.749935mm" width="0.7999984mm" height="0.270002mm" radius="0.135001mm" shape="pill" />
<smtpad portHints={["pin10"]} pcbX="1.499997mm" pcbY="-0.249809mm" width="0.7999984mm" height="0.270002mm" radius="0.135001mm" shape="pill" />
<smtpad portHints={["pin11"]} pcbX="1.499997mm" pcbY="0.250063mm" width="0.7999984mm" height="0.270002mm" radius="0.135001mm" shape="pill" />
<smtpad portHints={["pin12"]} pcbX="1.499997mm" pcbY="0.750189mm" width="0.7999984mm" height="0.270002mm" radius="0.135001mm" shape="pill" />
<smtpad portHints={["pin13"]} pcbX="0.749935mm" pcbY="1.499997mm" width="0.2800096mm" height="0.850011mm" radius="0.1400048mm" shape="pill" />
<smtpad portHints={["pin14"]} pcbX="0.249809mm" pcbY="1.499997mm" width="0.2800096mm" height="0.850011mm" radius="0.1400048mm" shape="pill" />
<smtpad portHints={["pin15"]} pcbX="-0.250063mm" pcbY="1.499997mm" width="0.2800096mm" height="0.850011mm" radius="0.1400048mm" shape="pill" />
<smtpad portHints={["pin16"]} pcbX="-0.750189mm" pcbY="1.499997mm" width="0.2800096mm" height="0.850011mm" radius="0.1400048mm" shape="pill" />
<smtpad portHints={["pin17"]} pcbX="-0.000127mm" pcbY="0.000127mm" width="1.499997mm" height="1.499997mm" shape="rect" />
<silkscreenpath route={[{"x":1.2750038000000075,"y":-1.724837800000003},{"x":1.7248378000000173,"y":-1.724837800000003},{"x":1.7248378000000173,"y":-1.2750037999999932}]} />
<silkscreenpath route={[{"x":1.2750038000000075,"y":1.7249902000000006},{"x":1.7248378000000173,"y":1.7249902000000006},{"x":1.7248378000000173,"y":1.275156200000005}]} />
<silkscreenpath route={[{"x":-1.7249901999999864,"y":1.275156200000005},{"x":-1.7249901999999864,"y":1.7249902000000006},{"x":-1.2751561999999907,"y":1.7249902000000006}]} />
<silkscreenpath route={[{"x":-1.2751561999999907,"y":-1.724837800000003},{"x":-1.7249901999999864,"y":-1.724837800000003},{"x":-1.7249901999999864,"y":-1.2750037999999932}]} />
<silkscreenpath route={[{"x":-2.0501101999999776,"y":1.5001239999999996},{"x":-2.200752229703909,"y":1.6488650559976676},{"x":-2.350129624014727,"y":1.4988539999999944},{"x":-2.200752229703909,"y":1.3488429440023353},{"x":-2.0501101999999776,"y":1.4975839999999963}]} />
<silkscreentext text="{NAME}" pcbX="-0.233299mm" pcbY="2.922399mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-2.1499961999999897,"y":2.175002499999998},{"x":2.149996200000004,"y":2.175002499999998},{"x":2.149996200000004,"y":-2.175002499999998},{"x":-2.1499961999999897,"y":-2.175002499999998},{"x":-2.1499961999999897,"y":2.175002499999998}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: -0.000012700000013410317, y: 0.000012699999999199463, z: -0.03 },
      }}
      {...props}
    />
  )
}