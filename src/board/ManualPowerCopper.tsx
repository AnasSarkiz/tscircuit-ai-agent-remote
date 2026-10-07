import { z } from "zod"
import manualPowerCopper from "./manual-power-copper.json"
import { viaHoleDiameterMm, viaPadDiameterMm } from "./viaGeometry"

const point = z.object({ x: z.number(), y: z.number() })
const region = z.object({
  net: z.string(),
  layer: z.enum(["top", "inner1", "inner2", "bottom"]),
  outline: point.array().min(3),
  nominal_width_mm: z.number().positive(),
  branch_terminal: z.string().optional(),
})
const throughVia = z.object({
  net: z.string(),
  x: z.number(),
  y: z.number(),
  hole_mm: z.literal(viaHoleDiameterMm),
  outer_mm: z.literal(viaPadDiameterMm),
})
const regions = region.array().parse(manualPowerCopper.pours)
const retiredRegionIndices = new Set(
  z
    .object({
      retired_connection_region_indices: z
        .array(
          z
            .number()
            .int()
            .min(0)
            .max(regions.length - 1),
        )
        .default([]),
    })
    .parse(manualPowerCopper).retired_connection_region_indices,
)
const vias = throughVia.array().parse(manualPowerCopper.vias)
const highCurrentNets = new Set(["PACK_BAT", "VSYS", "VBUS", "V3V3", "VMOTOR", "HAPTIC_N"])
if (manualPowerCopper.unresolved.length) throw new Error("Unresolved authored power routes")
for (const region of regions) {
  if (!highCurrentNets.has(region.net) || ["top", "bottom"].includes(region.layer)) continue
  const branch = manualPowerCopper.branch_requirements.find(
    (branch) => branch.net === region.net && branch.terminal === region.branch_terminal,
  )
  if (
    !branch ||
    !branch.layers.includes(region.layer) ||
    branch.nominal_width_mm !== region.nominal_width_mm
  )
    throw new Error(`High-current distribution cannot use ${region.layer}: ${region.net}`)
}

// Board copper features, not purchased components or autorouter replay caches.
export function ManualPowerCopper({ placementOnly = false }: { placementOnly?: boolean } = {}) {
  if (placementOnly) return null
  return (
    <>
      {regions.map((region, index) =>
        retiredRegionIndices.has(index) ? null : (
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
        ),
      )}
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
