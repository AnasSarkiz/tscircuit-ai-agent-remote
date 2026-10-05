import { z } from "zod"
import manualPowerCopper from "./manual-power-copper.json"

const point = z.object({ x: z.number(), y: z.number() })
const region = z.object({
  net: z.string(),
  layer: z.enum(["inner2", "bottom"]),
  outline: point.array().min(3),
  nominal_width_mm: z.number().positive(),
})
const throughVia = z.object({
  net: z.string(),
  x: z.number(),
  y: z.number(),
  hole_mm: z.number().min(0.3),
  outer_mm: z.number().min(0.7),
})
const regions = region.array().parse(manualPowerCopper.pours)
const vias = throughVia.array().parse(manualPowerCopper.vias)

// Board copper features, not purchased components or autorouter replay caches.
export function ManualPowerCopper({ placementOnly = false }: { placementOnly?: boolean } = {}) {
  if (placementOnly) return null
  return (
    <>
      {regions.map((region, index) => (
        <copperpour
          name={`POWER_${region.net}_${index}`}
          connectsTo={`net.${region.net}`}
          layer={region.layer}
          outline={region.outline}
          clearance={0.21}
          cutoutMargin={0.26}
          // These outlines already include the 0.26 mm board-edge reserve.
          // The pour engine applies this margin to the region's own perimeter.
          boardEdgeMargin={0}
          coveredWithSolderMask
          useThermalReliefs={false}
        />
      ))}
      {vias.map((via, index) => (
        <via
          name={`POWER_VIA_${index}`}
          connectsTo={`net.${via.net}`}
          pcbX={via.x}
          pcbY={via.y}
          holeDiameter={via.hole_mm}
          outerDiameter={via.outer_mm}
          fromLayer="top"
          toLayer="bottom"
          tented
        />
      ))}
    </>
  )
}
