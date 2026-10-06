import objPath from "./AFC07_S50ECA_00.obj"
import stepPath from "./AFC07_S50ECA_00.step"
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
  pin12: ["pin12"],
  pin13: ["pin13"],
  pin14: ["pin14"],
  pin15: ["pin15"],
  pin16: ["pin16"],
  pin17: ["pin17"],
  pin18: ["pin18"],
  pin19: ["pin19"],
  pin20: ["pin20"],
  pin21: ["pin21"],
  pin22: ["pin22"],
  pin23: ["pin23"],
  pin24: ["pin24"],
  pin25: ["pin25"],
  pin26: ["pin26"],
  pin27: ["pin27"],
  pin28: ["pin28"],
  pin29: ["pin29"],
  pin30: ["pin30"],
  pin31: ["pin31"],
  pin32: ["pin32"],
  pin33: ["pin33"],
  pin34: ["pin34"],
  pin35: ["pin35"],
  pin36: ["pin36"],
  pin37: ["pin37"],
  pin38: ["pin38"],
  pin39: ["pin39"],
  pin40: ["pin40"],
  pin41: ["pin41"],
  pin42: ["pin42"],
  pin43: ["pin43"],
  pin44: ["pin44"],
  pin45: ["pin45"],
  pin46: ["pin46"],
  pin47: ["pin47"],
  pin48: ["pin48"],
  pin49: ["pin49"],
  pin50: ["pin50"],
  pin51: ["pin51"],
  pin52: ["pin52"]
} as const

export const AFC07_S50ECA_00 = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C262650"
  ]
}}
      manufacturerPartNumber="AFC07-S50ECA-00"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="-12.248007mm" pcbY="1.5361031mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="-11.749913mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="-11.250041mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="-10.749915mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="-10.250043mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin6"]} pcbX="-9.749917mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin7"]} pcbX="-9.250045mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin8"]} pcbX="-8.749919mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin9"]} pcbX="-8.250047mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin10"]} pcbX="-7.749921mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin11"]} pcbX="-7.250049mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin12"]} pcbX="-6.749923mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin13"]} pcbX="-6.250051mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin14"]} pcbX="-5.749925mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin15"]} pcbX="-5.250053mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin16"]} pcbX="-4.749927mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin17"]} pcbX="-4.250055mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin18"]} pcbX="-3.749929mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin19"]} pcbX="-3.250057mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin20"]} pcbX="-2.749931mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin21"]} pcbX="-2.250059mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin22"]} pcbX="-1.749933mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin23"]} pcbX="-1.250061mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin24"]} pcbX="-0.749935mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin25"]} pcbX="-0.250063mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin26"]} pcbX="0.250063mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin27"]} pcbX="0.749935mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin28"]} pcbX="1.250061mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin29"]} pcbX="1.749933mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin30"]} pcbX="2.250059mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin31"]} pcbX="2.749931mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin32"]} pcbX="3.250057mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin33"]} pcbX="3.749929mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin34"]} pcbX="4.250055mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin35"]} pcbX="4.749927mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin36"]} pcbX="5.250053mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin37"]} pcbX="5.749925mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin38"]} pcbX="6.250051mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin39"]} pcbX="6.749923mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin40"]} pcbX="7.250049mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin51"]} pcbX="13.849985mm" pcbY="-0.6358509mm" width="2.1999956mm" height="3.2999934mm" shape="rect" />
<smtpad portHints={["pin52"]} pcbX="-13.849985mm" pcbY="-0.6361049mm" width="2.1999956mm" height="3.2999934mm" shape="rect" />
<smtpad portHints={["pin41"]} pcbX="7.751953mm" pcbY="1.5361031mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin42"]} pcbX="8.249539mm" pcbY="1.5340711mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin43"]} pcbX="8.749665mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin44"]} pcbX="9.250045mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin45"]} pcbX="9.750425mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin46"]} pcbX="10.251059mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin47"]} pcbX="10.751185mm" pcbY="1.5350871mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin48"]} pcbX="11.249533mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin49"]} pcbX="11.749913mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin50"]} pcbX="12.248515mm" pcbY="1.5345791mm" width="0.2999994mm" height="1.499997mm" shape="rect" />
<silkscreenpath route={[{"x":15.200020399999858,"y":-3.8499923000001672},{"x":15.200020399999858,"y":-4.585982700000159}]} />
<silkscreenpath route={[{"x":-15.300020200000063,"y":-3.8499415},{"x":-15.300020200000063,"y":-4.585957300000018}]} />
<silkscreenpath route={[{"x":-15.29999480000015,"y":-4.585957300000018},{"x":15.199918799999978,"y":-4.585982700000159}]} />
<silkscreenpath route={[{"x":-14.699996000000056,"y":1.1500485000000253},{"x":-12.629057800000055,"y":1.1500485000000253}]} />
<silkscreenpath route={[{"x":-14.699996000000056,"y":-2.5171781000001374},{"x":-14.699996000000056,"y":-2.6499439000000393},{"x":-15.300020200000063,"y":-2.6499439000000393},{"x":-15.300020200000063,"y":-3.8499415}]} />
<silkscreenpath route={[{"x":14.799995800000033,"y":-2.5171527000001106},{"x":14.799995800000033,"y":-2.6499439000000393},{"x":15.200020399999858,"y":-2.6499439000000393},{"x":15.200020399999858,"y":-3.8499923000001672}]} />
<silkscreenpath route={[{"x":12.699999999999818,"y":1.1500485000000253},{"x":15.000020799999902,"y":1.1500485000000253}]} />
<silkscreencircle pcbX="-13.095986mm" pcbY="1.7090009mm" radius="0.1999996mm" />
<silkscreentext text="{NAME}" pcbX="-0.025781mm" pcbY="3.2909911mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-15.549969400000009,"y":2.5361015999998244},{"x":15.549969399999782,"y":2.5361015999998244},{"x":15.549969399999782,"y":-3.9749481000001197},{"x":-15.549969400000009,"y":-3.9749481000001197},{"x":-15.549969400000009,"y":2.5361015999998244}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 0, y: 0.8499601999999413, z: 0 },
      }}
      {...props}
    />
  )
}