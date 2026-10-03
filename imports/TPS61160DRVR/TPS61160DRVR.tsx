import objPath from "./TPS61160DRVR.obj"
import stepPath from "./TPS61160DRVR.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["FB"],
  pin2: ["COMP"],
  pin3: ["GND"],
  pin4: ["SW"],
  pin5: ["CTRL"],
  pin6: ["VIN"],
  pin7: ["EP"]
} as const

const pinAttributes = {
  pin3: {requiresGround: true},
  pin6: {requiresPower: true}
} as const

const footprinterPinLabels = {
  ...pinLabels,
  "pin7": [...pinLabels["pin7"], "thermalpad"],
} as const

export const TPS61160DRVR = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={footprinterPinLabels}
      pinAttributes={pinAttributes}
      supplierPartNumbers={{
  "jlcpcb": [
    "C165143"
  ]
}}
      manufacturerPartNumber="TPS61160DRVR"
      footprint="dfn6_thermalpad1mmx1.6mm_pillpads_p0.65mm_w2.67mm_pw0.36mm_pl0.61mm"
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 0, y: 0, z: 0 },
      }}
      {...props}
    />
  )
}