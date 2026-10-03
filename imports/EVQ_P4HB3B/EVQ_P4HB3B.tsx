import objPath from "./EVQ_P4HB3B.obj"
import stepPath from "./EVQ_P4HB3B.step"
import type { PushButtonProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["pin1"],
  pin2: ["pin2"],
  pin3: ["pin3"],
  pin4: ["pin4"]
} as const

export const EVQ_P4HB3B = (props: PushButtonProps<typeof pinLabels>) => {
  const { name = "SW1", ...restProps } = props

  return (
    <pushbutton
      name={name}
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C6617702"
  ]
}}
      manufacturerPartNumber="EVQ-P4HB3B"
      footprint={<footprint>
        <cutout shape="polygon" points={[{"x":-2.666974600000003,"y":-1.5499905499999613},{"x":-2.666974600000003,"y":0.22800945000005868},{"x":2.667025400000057,"y":0.22800945000005868},{"x":2.667025400000057,"y":-1.5499905499999613}]} />
<smtpad portHints={["pin2"]} pcbX="2.274951mm" pcbY="1.02498525mm" width="1.4500098mm" height="1.0500106mm" shape="rect" />
<smtpad portHints={["pin1"]} pcbX="-2.274951mm" pcbY="1.02498525mm" width="1.4500098mm" height="1.0500106mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="3.200019mm" pcbY="-0.69992875mm" width="0.5999988mm" height="0.7999984mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="-3.200019mm" pcbY="-0.69992875mm" width="0.5999988mm" height="0.7999984mm" shape="rect" />
<silkscreenpath route={[{"x":2.600020200000017,"y":-1.5499905499999613},{"x":3.0999938000001066,"y":-1.5499905499999613}]} />
<silkscreenpath route={[{"x":3.0999938000001066,"y":-1.3311187499997459},{"x":3.0999938000001066,"y":-1.5374683499999264}]} />
<silkscreenpath route={[{"x":3.0999938000001066,"y":0.29189045000020997},{"x":3.0999938000001066,"y":-0.06884034999984578}]} />
<silkscreenpath route={[{"x":-1.318818800000031,"y":1.0125138500000048},{"x":1.3188696000000846,"y":1.0125138500000048}]} />
<silkscreenpath route={[{"x":-3.0999937999998792,"y":-0.06884034999984578},{"x":-3.0999937999998792,"y":0.2919158500001231}]} />
<silkscreenpath route={[{"x":-2.59996939999985,"y":-1.5499905499999613},{"x":-3.0999937999998792,"y":-1.5499905499999613},{"x":-3.0999937999998792,"y":-1.3311187499997459}]} />
<silkscreenpath route={[{"x":0.9000236000000541,"y":-2.5499885499998527},{"x":0.9000236000000541,"y":-1.5499905499999613}]} />
<silkscreenpath route={[{"x":-0.8999727999998868,"y":-2.5499885499998527},{"x":-0.8999727999998868,"y":-1.5499905499999613}]} />
<silkscreenpath route={[{"x":0.9000236000000541,"y":-2.5499885499998527},{"x":-0.8999727999998868,"y":-2.5499885499998527}]} />
<silkscreenpath route={[{"x":-2.59996939999985,"y":-1.5499905499999613},{"x":2.600020200000017,"y":-1.5499905499999613}]} />
<silkscreentext text="{NAME}" pcbX="0.011049mm" pcbY="2.55838525mm" anchorAlignment="center" fontSize="1mm" />
<fabricationnotepath route={[{"x":-0.8999982000000273,"y":-2.5374663499999315},{"x":0.8999982000000273,"y":-2.5374663499999315},{"x":0.8999982000000273,"y":-1.5374683499999264},{"x":-0.8999982000000273,"y":-1.5374683499999264},{"x":-0.8999982000000273,"y":-2.5374663499999315}]} strokeWidth="0.254mm" />
<courtyardoutline outline={[{"x":-3.750018399999931,"y":1.799990550000075},{"x":3.7500184000000445,"y":1.799990550000075},{"x":3.7500184000000445,"y":-2.653481349999879},{"x":-3.750018399999931,"y":-2.653481349999879},{"x":-3.750018399999931,"y":1.799990550000075}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: -0.000025400000140507473, y: 1.584984749999916, z: 0.39999569999999984 },
      }}
      {...restProps}
    />
  )
}