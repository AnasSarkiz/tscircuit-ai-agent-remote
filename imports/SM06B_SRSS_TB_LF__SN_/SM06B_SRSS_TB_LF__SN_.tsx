import objPath from "./SM06B_SRSS_TB_LF__SN_.obj"
import stepPath from "./SM06B_SRSS_TB_LF__SN_.step"
import type { ChipProps } from "@tscircuit/props"

const pinLabels = {
  pin1: ["pin1"],
  pin2: ["pin2"],
  pin3: ["pin3"],
  pin4: ["pin4"],
  pin5: ["pin5"],
  pin6: ["pin6"],
  pin7: ["pin7"],
  pin8: ["pin8"]
} as const

export const SM06B_SRSS_TB_LF__SN_ = (props: ChipProps<typeof pinLabels>) => {
  return (
    <chip
      pinLabels={pinLabels}
      supplierPartNumbers={{
  "jlcpcb": [
    "C160405"
  ]
}}
      manufacturerPartNumber="SM06B-SRSS-TB(LF)(SN)"
      footprint="fpc6_p1mm_pw0.6mm_pl1.55mm_mpx7.6mm_mpy3.88mm_mpw1.5mm_mpl2mm"
      cadModel={{
        objUrl: objPath,
        stepUrl: stepPath,
        pcbRotationOffset: 0,
        modelOriginPosition: { x: 2.4999238000000332, y: 0.3445008999999346, z: -0.01 },
      }}
      {...props}
    />
  )
}