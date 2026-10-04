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
  pin14: ["pin14"]
} as const

export const AFC07_S12FCC_00 = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C11051"
  ]
}}
      manufacturerPartNumber="AFC07-S12FCC-00"
      footprint={<footprint>
        <smtpad portHints={["pin13"]} pcbX="4.429887mm" pcbY="0.75504675mm" width="1.999996mm" height="2.999994mm" shape="rect" />
<smtpad portHints={["pin14"]} pcbX="-4.429887mm" pcbY="0.74895075mm" width="1.999996mm" height="2.999994mm" shape="rect" />
<smtpad portHints={["pin12"]} pcbX="2.745613mm" pcbY="-1.50504525mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin11"]} pcbX="2.245487mm" pcbY="-1.50504525mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin10"]} pcbX="1.745615mm" pcbY="-1.50504525mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin9"]} pcbX="1.245489mm" pcbY="-1.50504525mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin8"]} pcbX="0.745617mm" pcbY="-1.50504525mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin7"]} pcbX="0.245491mm" pcbY="-1.50504525mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin6"]} pcbX="-0.254381mm" pcbY="-1.50504525mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin5"]} pcbX="-0.754507mm" pcbY="-1.50504525mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin4"]} pcbX="-1.254379mm" pcbY="-1.50504525mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="-1.754505mm" pcbY="-1.50504525mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="-2.254377mm" pcbY="-1.50504525mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin1"]} pcbX="-2.753995mm" pcbY="-1.50504525mm" width="0.299974mm" height="1.499997mm" shape="rect" />
<silkscreenpath route={[{"x":-5.343905999999947,"y":-0.9821608500000139},{"x":-5.343905999999947,"y":-1.2642024500000844},{"x":-3.1849059999998417,"y":-1.2642024500000844}]} />
<silkscreenpath route={[{"x":5.31106380000017,"y":2.4859551499998815},{"x":5.31106380000017,"y":3.307797550000032},{"x":-5.343905999999947,"y":3.307797550000032},{"x":-5.343905999999947,"y":2.4801385499999924}]} />
<silkscreenpath route={[{"x":3.0976823999999397,"y":-1.163237449999997},{"x":5.31106380000017,"y":-1.163237449999997},{"x":5.31106380000017,"y":-0.9760902500000839}]} />
<silkscreencircle pcbX="-4.190873mm" pcbY="-1.64525325mm" radius="0.127mm" />
<silkscreentext text="{NAME}" pcbX="-0.211455mm" pcbY="4.89001635mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-5.679885000000013,"y":4.140651349999871},{"x":5.679885000000127,"y":4.140651349999871},{"x":5.679885000000127,"y":-2.5050437499999134},{"x":-5.679885000000013,"y":-2.5050437499999134},{"x":-5.679885000000013,"y":4.140651349999871}]} />
      </footprint>}
      cadModel={{
        objUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C11051.obj?uuid=8755d8e369b347d39865d1aa9a958bef",
        stepUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C11051.step?uuid=8755d8e369b347d39865d1aa9a958bef",
        pcbRotationOffset: 180,
        modelOriginPosition: { x: -0.0023621999999932086, y: 0.7406573499998559, z: -0.01 },
      }}
      {...props}
    />
  )
}