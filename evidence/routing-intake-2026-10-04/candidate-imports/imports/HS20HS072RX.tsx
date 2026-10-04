import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["GND"]
} as const

const pinAttributes = {
  pin1: {requiresGround: true}
} as const

export const HS20HS072RX = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C5329582"
  ]
}}
      manufacturerPartNumber="HS20HS072RX"
      footprint={<footprint>
        <smtpad portHints={["pin1"]} pcbX="0mm" pcbY="0mm" width="1.524mm" height="1.524mm" shape="rect" />
<silkscreentext text="非PCB焊接件" pcbX="-4.953mm" pcbY="-2.794mm" anchorAlignment="bottom_left" fontSize="2.032mm" />
<silkscreentext text="Non-soldered components" pcbX="-4.699mm" pcbY="-5.715mm" anchorAlignment="bottom_left" fontSize="2.032mm" />
<silkscreentext text="{NAME}" pcbX="14.3891mm" pcbY="5.953mm" anchorAlignment="center" fontSize="1mm" />
<fabricationnotepath route={[{"x":1.2699999999999818,"y":4.9529999999999745},{"x":1.2699999999999818,"y":-0.3809999999999718},{"x":5.333999999999946,"y":-0.3809999999999718},{"x":5.333999999999946,"y":0.3810000000000855},{"x":2.158999999999992,"y":0.3810000000000855},{"x":2.158999999999992,"y":4.9529999999999745},{"x":1.2699999999999818,"y":4.9529999999999745}]} strokeWidth="0.254mm" />
<fabricationnotepath route={[{"x":-2.7940000000000964,"y":4.9529999999999745},{"x":0,"y":4.9529999999999745},{"x":0,"y":4.317999999999984},{"x":-2.286000000000058,"y":4.317999999999984},{"x":-2.286000000000058,"y":2.921000000000049},{"x":0,"y":2.921000000000049},{"x":0,"y":2.413000000000011},{"x":-2.286000000000058,"y":2.413000000000011},{"x":-2.286000000000058,"y":-0.3809999999999718},{"x":-2.7940000000000964,"y":-0.3809999999999718},{"x":-2.7940000000000964,"y":4.9529999999999745}]} strokeWidth="0.254mm" />
<courtyardoutline outline={[{"x":-5.101400000000012,"y":5.2029999999999745},{"x":33.879599999999755,"y":5.2029999999999745},{"x":33.879599999999755,"y":-6.498399999999947},{"x":-5.101400000000012,"y":-6.498399999999947},{"x":-5.101400000000012,"y":5.2029999999999745}]} />
      </footprint>}
      
      {...props}
    />
  )
}