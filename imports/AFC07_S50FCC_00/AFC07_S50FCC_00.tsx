import objPath from "./AFC07_S50FCC_00.obj"
import stepPath from "./AFC07_S50FCC_00.step"
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

export const AFC07_S50FCC_00 = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C11063"
  ]
}}
      manufacturerPartNumber="AFC07-S50FCC-00"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="12.2499628mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="11.7499638mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="11.2499648mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="10.7499658mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="10.2499668mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin6"]} pcbX="9.7499678mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin7"]} pcbX="9.2499688mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin8"]} pcbX="8.7499698mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin9"]} pcbX="8.2499708mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin10"]} pcbX="7.7499718mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin11"]} pcbX="7.2499728mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin12"]} pcbX="6.7499738mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin13"]} pcbX="6.2499748mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin14"]} pcbX="5.7499758mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin15"]} pcbX="5.2499768mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin16"]} pcbX="4.7499778mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin17"]} pcbX="4.2499788mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin18"]} pcbX="3.7499798mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin19"]} pcbX="3.2499808mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin20"]} pcbX="2.7499818mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin21"]} pcbX="2.2499828mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin22"]} pcbX="1.7499838mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin23"]} pcbX="1.2499848mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin24"]} pcbX="0.7499858mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin25"]} pcbX="0.2499868mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin26"]} pcbX="-0.2499868mm" pcbY="1.55216225mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin27"]} pcbX="-0.7500112mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin28"]} pcbX="-1.2500102mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin29"]} pcbX="-1.7500092mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin30"]} pcbX="-2.2500082mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin31"]} pcbX="-2.7500072mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin32"]} pcbX="-3.2500062mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin33"]} pcbX="-3.7500052mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin34"]} pcbX="-4.2500042mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin35"]} pcbX="-4.7500032mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin36"]} pcbX="-5.2500022mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin37"]} pcbX="-5.7500012mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin38"]} pcbX="-6.2500002mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin39"]} pcbX="-6.7499992mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin40"]} pcbX="-7.2499982mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin41"]} pcbX="-7.7499972mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin42"]} pcbX="-8.2499962mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin43"]} pcbX="-8.7499952mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin44"]} pcbX="-9.2499942mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin45"]} pcbX="-9.7499932mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin46"]} pcbX="-10.2499922mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin47"]} pcbX="-10.7499912mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin48"]} pcbX="-11.2499902mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin49"]} pcbX="-11.7499892mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin50"]} pcbX="-12.2499882mm" pcbY="1.55140025mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin52"]} pcbX="13.999972mm" pcbY="-0.80190975mm" width="1.999996mm" height="2.999994mm" shape="rect" />
<smtpad portHints={["pin51"]} pcbX="-13.999972mm" pcbY="-0.80216375mm" width="1.999996mm" height="2.999994mm" shape="rect" />
<silkscreenpath route={[{"x":-12.76822439999998,"y":0.8478456499999822},{"x":-12.651993999999988,"y":0.8478456499999822}]} />
<silkscreenpath route={[{"x":12.651994000000016,"y":0.8478456499999822},{"x":15.295625999999999,"y":0.8478456499999822}]} />
<silkscreenpath route={[{"x":-15.304261999999994,"y":0.8478456499999822},{"x":-12.76822439999998,"y":0.8478456499999822}]} />
<silkscreenpath route={[{"x":-15.304261999999994,"y":0.8478456499999822},{"x":-15.304261999999994,"y":-3.1650495500000204}]} />
<silkscreenpath route={[{"x":-15.299334399999992,"y":-3.185039350000025},{"x":-15.299334399999992,"y":-3.885037950000026}]} />
<silkscreenpath route={[{"x":-15.299334399999992,"y":-4.185037350000016},{"x":15.3005536,"y":-4.185037350000016}]} />
<silkscreenpath route={[{"x":15.3005536,"y":-3.1650495500000204},{"x":15.3005536,"y":-3.865048150000021}]} />
<silkscreenpath route={[{"x":-15.299334399999992,"y":-3.1650495500000204},{"x":15.3005536,"y":-3.1650495500000204}]} />
<silkscreenpath route={[{"x":15.295625999999999,"y":0.8478456499999822},{"x":15.295625999999999,"y":-3.1650495500000204}]} />
<silkscreenpath route={[{"x":-15.304261999999994,"y":0.8478456499999822},{"x":-15.230500399999997,"y":0.8478456499999822}]} />
<silkscreentext text="{NAME}" pcbX="0.002032mm" pcbY="3.30959025mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-15.54996939999998,"y":2.5521607499999845},{"x":15.549969400000023,"y":2.5521607499999845},{"x":15.549969400000023,"y":-3.7550031500000216},{"x":-15.54996939999998,"y":-3.7550031500000216},{"x":-15.54996939999998,"y":2.5521607499999845}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 0, y: 0.805008550000025, z: 0 },
      }}
      {...props}
    />
  )
}