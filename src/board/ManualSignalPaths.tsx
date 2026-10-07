import { pcbPath } from "@tscircuit/props"
import { z } from "zod"
import manualPaths from "./manual-signal-paths.json"
import { ManualInnerSignalCopper, relocatedSignalPathIndices } from "./ManualInnerSignalCopper"
import { retiredManualConnectionPathIndices } from "./ManualConnectionCopper"

const manualTrace = z.object({
  net: z.string(),
  from: z.string(),
  to: z.string(),
  width: z.number().positive(),
  pcbPath,
})
const paths = manualTrace.array().parse(manualPaths.paths)
const retiredSourcePathIndices = new Set(
  z
    .object({
      retired_source_path_indices: z
        .array(
          z
            .number()
            .int()
            .min(0)
            .max(paths.length - 1),
        )
        .default([]),
    })
    .parse(manualPaths).retired_source_path_indices,
)

// Deliberately authored native paths, never represented as autorouter caches.
export function ManualSignalPaths({ placementOnly = false }: { placementOnly?: boolean } = {}) {
  if (placementOnly) return null
  return (
    <>
      {paths.map((path, index) =>
        retiredSourcePathIndices.has(index) ? null : (
          <trace
            key={`${path.net}-${index}`}
            name={`MANUAL_${path.net}_${index}`}
            from={path.from}
            to={path.to}
            width={path.width}
            pcbPathRelativeTo={path.from}
            pcbPath={
              relocatedSignalPathIndices.has(index) || retiredManualConnectionPathIndices.has(index)
                ? undefined
                : path.pcbPath
            }
          />
        ),
      )}
      <ManualInnerSignalCopper />
    </>
  )
}
