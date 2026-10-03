import objPath from "./AFC07_S10FCC_00.obj"
import stepPath from "./AFC07_S10FCC_00.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["pin1"],
  pin2: ["pin2"],
  pin3: ["pin3"],
  pin4: ["pin4"],
  pin5: ["pin5"],
  pin6: ["pin6"],
  pin7: ["pin7"],
  pin8: ["pin8"],
  pin9: ["pin9"],
  pin10: ["pin10"],
  pin11: ["pin11"],
  pin12: ["pin12"]
} as const

export const AFC07_S10FCC_00 = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C11050"
  ]
}}
      manufacturerPartNumber="AFC07-S10FCC-00"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="-2.2500082mm" pcbY="-1.19014875mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="-1.7500092mm" pcbY="-1.19014875mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="-1.2500102mm" pcbY="-1.19014875mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="-0.7500112mm" pcbY="-1.19014875mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="-0.2499868mm" pcbY="-1.19014875mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin6"]} pcbX="0.2499868mm" pcbY="-1.19014875mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin7"]} pcbX="0.7500112mm" pcbY="-1.19014875mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin8"]} pcbX="1.2500102mm" pcbY="-1.19014875mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin9"]} pcbX="1.7500092mm" pcbY="-1.19014875mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin10"]} pcbX="2.2500082mm" pcbY="-1.19014875mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin11"]} pcbX="-4.1999916mm" pcbY="0.54015005mm" width="1.999996mm" height="2.7999944mm" shape="rect" />
<smtpad portHints={["pin12"]} pcbX="4.1999916mm" pcbY="0.54015005mm" width="1.999996mm" height="2.7999944mm" shape="rect" />
<silkscreenpath route={[{"x":5.300091000000009,"y":3.675221249999993},{"x":5.300091000000009,"y":5.0252312500000045},{"x":5.299989400000001,"y":5.0901282500000065},{"x":5.224398999999991,"y":5.09000125},{"x":5.224398999999991,"y":5.09000125}]} />
<silkscreenpath route={[{"x":-5.224983199999997,"y":5.0901282500000065},{"x":5.224322799999996,"y":5.0901282500000065}]} />
<silkscreenpath route={[{"x":5.299989400000001,"y":2.1482494500000087},{"x":5.299989400000001,"y":3.6751450499999976}]} />
<silkscreenpath route={[{"x":5.299989400000001,"y":3.6751450499999976},{"x":-5.299989400000015,"y":3.6751450499999976},{"x":-5.299989400000015,"y":2.1482494500000087}]} />
<silkscreenpath route={[{"x":-5.300090999999995,"y":3.675221249999993},{"x":-5.300090999999995,"y":5.09000125},{"x":-5.300090999999995,"y":5.09000125},{"x":-5.224907000000016,"y":5.09000125}]} />
<silkscreenpath route={[{"x":2.631160599999987,"y":-0.6248463499999986},{"x":2.9688535999999885,"y":-0.6248463499999986}]} />
<silkscreenpath route={[{"x":-2.968853600000017,"y":-0.6248463499999986},{"x":-2.6313638000000026,"y":-0.6248463499999986}]} />
<silkscreentext text="xx" pcbX="3.4649918mm" pcbY="3.98830165mm" anchorAlignment="bottom_left" fontSize="2.032mm" />
<silkscreentext text="A" pcbX="-4.8599852mm" pcbY="3.83013585mm" anchorAlignment="bottom_left" fontSize="2.032mm" />
<silkscreentext text="{NAME}" pcbX="-0.005969mm" pcbY="6.09965325mm" anchorAlignment="center" fontSize="1mm" />
<fabricationnotepath route={[{"x":-2.2860000000000156,"y":-0.19799935000001767},{"x":-2.2860000000000156,"y":-0.19799935000001767},{"x":-2.5400000000000205,"y":0.3100006499999921},{"x":-2.0320000000000107,"y":0.3100006499999921},{"x":-2.0320000000000107,"y":0.3100006499999921},{"x":-2.2860000000000156,"y":-0.19799935000001767}]} strokeWidth="0.254mm" />
<courtyardoutline outline={[{"x":-5.499976800000013,"y":4.755140849999989},{"x":5.500002199999997,"y":4.755140849999989},{"x":5.500002199999997,"y":-2.1901472500000096},{"x":-5.499976800000013,"y":-2.1901472500000096},{"x":-5.499976800000013,"y":4.755140849999989}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 10.299986800000015, y: -5.570148249999993, z: 0 },
      }}
      {...props}
    />
  )
}