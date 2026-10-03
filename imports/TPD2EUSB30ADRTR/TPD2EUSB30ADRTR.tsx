import objPath from "./TPD2EUSB30ADRTR.obj"
import stepPath from "./TPD2EUSB30ADRTR.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["D_POS"],
  pin2: ["D_NEG"],
  pin3: ["GND"]
} as const

const pinAttributes = {
  pin3: {requiresGround: true}
} as const

export const TPD2EUSB30ADRTR = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      symbol={
        <symbol>
          <schematictext schX={-0.44} schY={-0.568125} text="GND" fontSize={0.2} anchor="left" color="#0000FF" schRotation={0} />
          <schematicpath points={[{"x":-0.1,"y":0.32},{"x":-0.14,"y":0.28}]} strokeColor="#8D2323" />
          <port name="pin3" pinNumber={3} aliases={["GND"]} direction="down" schX={0} schY={-0.8} schStemLength={0.2} />
          <port name="pin1" pinNumber={1} aliases={["D_POS"]} direction="right" schX={1} schY={0.2} schStemLength={0.2} />
          <port name="pin2" pinNumber={2} aliases={["D_NEG"]} direction="left" schX={-1} schY={0.2} schStemLength={0.2} />
          <schematiccircle center={{ x: 0, y: -0.4 }} radius={0.02} strokeWidth={0.02} color="#880000" />
          <schematiccircle center={{ x: 0, y: 0.8 }} radius={0.02} strokeWidth={0.02} color="#880000" />
          <schematicpath points={[{"x":0.4,"y":-0.4},{"x":-0.4,"y":-0.4}]} strokeColor="#880000" />
          <schematicpath points={[{"x":0.4,"y":0.8},{"x":-0.4,"y":0.8}]} strokeColor="#880000" />
          <schematicpath points={[{"x":0,"y":-0.6},{"x":0,"y":0.8}]} strokeColor="#880000" />
          <schematicpath points={[{"x":0.4,"y":-0.4},{"x":0.4,"y":0.8}]} strokeColor="#880000" />
          <schematiccircle center={{ x: 0.4, y: 0.2 }} radius={0.02} strokeWidth={0.02} color="#880000" />
          <schematicpath points={[{"x":0.3,"y":-0.2},{"x":0.4,"y":0},{"x":0.5,"y":-0.2},{"x":0.3,"y":-0.2}]} strokeColor="#880000" isFilled fillColor="#880000" />
          <schematicpath points={[{"x":0.4,"y":0},{"x":0.3,"y":0}]} strokeColor="#8D2323" />
          <schematicpath points={[{"x":0.5,"y":0},{"x":0.4,"y":0}]} strokeColor="#8D2323" />
          <schematicpath points={[{"x":0.3,"y":0.4},{"x":0.4,"y":0.6},{"x":0.5,"y":0.4},{"x":0.3,"y":0.4}]} strokeColor="#880000" isFilled fillColor="#880000" />
          <schematicpath points={[{"x":0.4,"y":0.6},{"x":0.3,"y":0.6}]} strokeColor="#8D2323" />
          <schematicpath points={[{"x":0.5,"y":0.6},{"x":0.4,"y":0.6}]} strokeColor="#8D2323" />
          <schematicpath points={[{"x":0.8,"y":0.2},{"x":0.4,"y":0.2}]} strokeColor="#880000" />
          <schematicpath points={[{"x":-0.4,"y":-0.4},{"x":-0.4,"y":0.8}]} strokeColor="#880000" />
          <schematiccircle center={{ x: -0.4, y: 0.2 }} radius={0.02} strokeWidth={0.02} color="#880000" />
          <schematicpath points={[{"x":-0.3,"y":-0.2},{"x":-0.4,"y":0},{"x":-0.5,"y":-0.2},{"x":-0.3,"y":-0.2}]} strokeColor="#880000" isFilled fillColor="#880000" />
          <schematicpath points={[{"x":-0.4,"y":0},{"x":-0.3,"y":0}]} strokeColor="#8D2323" />
          <schematicpath points={[{"x":-0.5,"y":0},{"x":-0.4,"y":0}]} strokeColor="#8D2323" />
          <schematicpath points={[{"x":-0.3,"y":0.4},{"x":-0.4,"y":0.6},{"x":-0.5,"y":0.4},{"x":-0.3,"y":0.4}]} strokeColor="#880000" isFilled fillColor="#880000" />
          <schematicpath points={[{"x":-0.4,"y":0.6},{"x":-0.3,"y":0.6}]} strokeColor="#8D2323" />
          <schematicpath points={[{"x":-0.5,"y":0.6},{"x":-0.4,"y":0.6}]} strokeColor="#8D2323" />
          <schematicpath points={[{"x":-0.8,"y":0.2},{"x":-0.4,"y":0.2}]} strokeColor="#880000" />
          <schematicpath points={[{"x":0.1,"y":0.12},{"x":0,"y":0.32},{"x":-0.1,"y":0.12},{"x":0.1,"y":0.12}]} strokeColor="#880000" isFilled fillColor="#880000" />
          <schematicpath points={[{"x":0.14,"y":0.36},{"x":0.1,"y":0.32}]} strokeColor="#8D2323" />
          <schematicpath points={[{"x":0,"y":0.32},{"x":0.1,"y":0.32}]} strokeColor="#8D2323" />
          <schematicpath points={[{"x":-0.1,"y":0.32},{"x":0,"y":0.32}]} strokeColor="#8D2323" />
          <schematicrect schX={0} schY={0.2} width={1.6} height={1.6} strokeWidth={0.02} color="#880000" />
        </symbol>
      }
      supplierPartNumbers={{
  "jlcpcb": [
    "C94934"
  ]
}}
      manufacturerPartNumber="TPD2EUSB30ADRTR"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="0.499999mm" pcbY="-0.350012mm" width="0.2999994mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin2"]} pcbX="0.499999mm" pcbY="0.350012mm" width="0.2999994mm" height="0.1999996mm" shape="rect" />
<smtpad portHints={["pin3"]} pcbX="-0.499999mm" pcbY="0mm" width="0.2999994mm" height="0.1999996mm" shape="rect" />
<silkscreenpath route={[{"x":0.3998467999999775,"y":0.018872200000146222},{"x":0.3998467999999775,"y":-0.018846799999892028}]} />
<silkscreenpath route={[{"x":-0.40010080000013204,"y":0.4999990000000025},{"x":-0.40010080000013204,"y":0.3311398000000736}]} />
<silkscreenpath route={[{"x":-0.40010080000013204,"y":-0.3311397999999599},{"x":-0.40010080000013204,"y":-0.49999899999988884}]} />
<silkscreenpath route={[{"x":-0.40010080000013204,"y":0.4999990000000025},{"x":0.12428219999992507,"y":0.4999990000000025}]} />
<silkscreenpath route={[{"x":-0.40010080000013204,"y":-0.49999899999988884},{"x":0.12428219999992507,"y":-0.49999899999988884}]} />
<silkscreentext text="{NAME}" pcbX="0.101473mm" pcbY="1.508mm" anchorAlignment="center" fontSize="1mm" />
<courtyardoutline outline={[{"x":-0.8999987000000829,"y":0.7480940000000373},{"x":0.8999986999999692,"y":0.7480940000000373},{"x":0.8999986999999692,"y":-0.7481193999999505},{"x":-0.8999987000000829,"y":-0.7481193999999505},{"x":-0.8999987000000829,"y":0.7480940000000373}]} />
      </footprint>}
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 90,
        modelOriginPosition: { x: 0.000012700000070253736, y: 0, z: 0 },
      }}
      {...props}
    />
  )
}