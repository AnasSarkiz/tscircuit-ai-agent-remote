import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["pin1"],
  pin2: ["_POS"]
} as const

export const LCM0720A3176F = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C2942347"
  ]
}}
      manufacturerPartNumber="LCM0720A3176F"
      footprint={<footprint>
        <smtpad portHints={["pin2"]} pcbX="0mm" pcbY="-0.999998mm" width="2.499995mm" height="1.499997mm" shape="rect" />
<smtpad portHints={["pin1"]} pcbX="0mm" pcbY="0.999998mm" width="2.499995mm" height="1.499997mm" shape="rect" />
<silkscreenpath route={[{"x":-5.588000000000079,"y":-2.158999999999878},{"x":1.5239999999998872,"y":-2.158999999999878},{"x":1.5239999999998872,"y":2.032000000000039},{"x":-5.588000000000079,"y":2.032000000000039}]} />
<silkscreencircle pcbX="-9.017mm" pcbY="0mm" radius="3.999992mm" />
<silkscreentext text="{NAME}" pcbX="-5.7658mm" pcbY="5.0386mm" anchorAlignment="center" fontSize="1mm" />
<fabricationnotepath route={[{"x":-5.461000000000126,"y":2.032000000000039},{"x":1.5239999999998872,"y":2.032000000000039},{"x":1.5239999999998872,"y":-2.158999999999992},{"x":-5.461000000000126,"y":-2.158999999999992}]} strokeWidth="0.254mm" />
<courtyardoutline outline={[{"x":-6.053976200000079,"y":1.999996499999952},{"x":1.4999975000000632,"y":1.999996499999952},{"x":1.4999975000000632,"y":-1.9999964999998383},{"x":-6.053976200000079,"y":-1.9999964999998383},{"x":-6.053976200000079,"y":1.999996499999952}]} />
      </footprint>}
      cadModel={{
        objUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C2942347.obj?uuid=29bf731b7eb04e3fab88dbbeb5800a7a",
        stepUrl: "https://modelcdn.tscircuit.com/easyeda_models/assets/C2942347.step?uuid=29bf731b7eb04e3fab88dbbeb5800a7a",
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 8.99398130000004, y: 0.004634499999999875, z: -3.55 },
      }}
      {...props}
    />
  )
}