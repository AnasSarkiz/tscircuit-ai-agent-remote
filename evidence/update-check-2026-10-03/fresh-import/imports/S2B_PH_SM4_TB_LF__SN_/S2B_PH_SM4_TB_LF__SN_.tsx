import objPath from "./S2B_PH_SM4_TB_LF__SN_.obj"
import stepPath from "./S2B_PH_SM4_TB_LF__SN_.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["pin1"],
  pin2: ["pin2"],
  pin3: ["pin3"],
  pin4: ["pin4"]
} as const

export const S2B_PH_SM4_TB_LF__SN_ = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C295747"
  ]
}}
      manufacturerPartNumber="S2B-PH-SM4-TB(LF)(SN)"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="-0.999998mm" pcbY="2.8250642mm" width="0.999998mm" height="3.7999924mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="0.999998mm" pcbY="2.8250642mm" width="0.999998mm" height="3.7999924mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="3.350006mm" pcbY="-3.0250638mm" width="1.499997mm" height="3.3999932mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="-3.350006mm" pcbY="-3.0250638mm" width="1.499997mm" height="3.3999932mm" shape="rect" />
<silkscreenpath route={[{"x":-1.7322800000001735,"y":1.5489681999999902},{"x":-2.9997399999999743,"y":1.5489681999999902},{"x":-2.9997399999999743,"y":3.1237681999999722},{"x":-3.949700000000121,"y":3.1237681999999722}]} />
<silkscreenpath route={[{"x":0.2688590000000204,"y":1.5500095999998393},{"x":-0.2688590000000204,"y":1.5500095999998393}]} />
<silkscreenpath route={[{"x":3.950004799999874,"y":3.1249873999997817},{"x":2.999994000000015,"y":3.1249873999997817},{"x":2.999994000000015,"y":1.5500095999998393},{"x":1.7311369999999897,"y":1.5500095999998393}]} />
<silkscreenpath route={[{"x":3.950004799999874,"y":3.1249873999997817},{"x":3.950004799999874,"y":-1.093825600000173}]} />
<silkscreenpath route={[{"x":2.399995199999921,"y":-4.47499740000012},{"x":-2.399995200000035,"y":-4.47499740000012}]} />
<silkscreenpath route={[{"x":-3.950004799999988,"y":3.1249873999997817},{"x":-3.950004799999988,"y":-1.093825600000173}]} />
<silkscreentext text="{NAME}" pcbX="0.0127mm" pcbY="5.7315882mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-4.3500044999999545,"y":4.9750603999998475},{"x":4.350004499999841,"y":4.9750603999998475},{"x":4.350004499999841,"y":-4.975060399999961},{"x":-4.3500044999999545,"y":-4.975060399999961},{"x":-4.3500044999999545,"y":4.9750603999998475}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: -0.9999872999999297, y: 2.8499996000001833, z: 0 },
      }}
      {...props}
    />
  )
}