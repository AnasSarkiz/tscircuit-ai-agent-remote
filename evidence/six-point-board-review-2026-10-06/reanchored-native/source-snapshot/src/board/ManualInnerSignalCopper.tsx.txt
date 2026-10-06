import { pcbPath } from "@tscircuit/props"
import { z } from "zod"
import innerSignals from "./inner-signal-copper.json"
import { viaHoleDiameterMm, viaPadDiameterMm } from "./viaGeometry"

const escape = z.object({
  from: z.string(),
  to: z.string(),
  pcbPathRelativeTo: z.string(),
  pcbPath,
})
const relocation = z.object({
  original_path_index: z.number().int().nonnegative(),
  net: z.string(),
  width: z.number().positive(),
  escapes: escape.array().min(1).max(2),
  regions: z
    .array(
      z.object({
        layer: z.enum(["inner1", "inner2"]),
        outline: z.array(z.object({ x: z.number(), y: z.number() })).min(3),
      }),
    )
    .min(1),
})
const throughVia = z.object({
  net: z.string(),
  x: z.number(),
  y: z.number(),
  hole_mm: z.literal(viaHoleDiameterMm),
  outer_mm: z.literal(viaPadDiameterMm),
})
const relocations = relocation.array().parse(innerSignals.paths)
const vias = throughVia.array().parse(innerSignals.vias)
if (innerSignals.unresolved.length) throw new Error("Unresolved authored inner signal routes")
export const relocatedSignalPathIndices = new Set(
  relocations.map((relocation) => relocation.original_path_index),
)

// Authored regions free the bottom layer for high-current distribution. The
// original logical traces remain in ManualSignalPaths. Every pad escape uses
// a native top-to-bottom through via; no partial-depth vias are introduced.
export function ManualInnerSignalCopper() {
  return (
    <>
      {relocations.flatMap((relocation) =>
        relocation.escapes.map((escape, index) => (
          <trace
            key={`${relocation.original_path_index}-${index}`}
            name={`MANUAL_INNER_ESCAPE_${relocation.original_path_index}_${index}`}
            from={escape.from}
            to={escape.to}
            width={relocation.width}
            pcbPathRelativeTo={escape.pcbPathRelativeTo}
            pcbPath={escape.pcbPath}
          />
        )),
      )}
      {relocations.flatMap((relocation) =>
        relocation.regions.map((region, index) => (
          <copperpour
            name={`INNER_SIGNAL_${relocation.original_path_index}_${index}`}
            connectsTo={`net.${relocation.net}`}
            layer={region.layer}
            outline={region.outline}
            clearance={0.21}
            cutoutMargin={0.26}
            boardEdgeMargin={0}
            coveredWithSolderMask
            useThermalReliefs={false}
          />
        )),
      )}
      {vias.map((via, index) => (
        <via
          name={`INNER_SIGNAL_VIA_${index}`}
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
