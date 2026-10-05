import { pcbPath } from "@tscircuit/props"
import { z } from "zod"
import manualPaths from "./manual-signal-paths.json"

const manualTrace = z.object({
  net: z.string(),
  from: z.string(),
  to: z.string(),
  width: z.number().positive(),
  pcbPath,
})
const paths = manualTrace.array().parse(manualPaths.paths)

// Deliberately authored native paths, never represented as autorouter caches.
export function ManualSignalPaths({ placementOnly = false }: { placementOnly?: boolean } = {}) {
  if (placementOnly) return null
  return (
    <>
      {paths.map((path, index) => (
        <trace
          key={`${path.net}-${index}`}
          name={`MANUAL_${path.net}_${index}`}
          from={path.from}
          to={path.to}
          width={path.width}
          pcbPathRelativeTo={path.from}
          pcbPath={path.pcbPath}
        />
      ))}
    </>
  )
}
