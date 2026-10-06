import { pcbPath } from "@tscircuit/props"
import groundPaths from "./ground-paths.json"

// Explicit native ordinary-via paths, independent of autorouting caches.
// Placement renders omit these; imported component definitions remain untouched.
const paths: Record<string, unknown> = groundPaths
export function groundPath(port: string, placementOnly: boolean) {
  return placementOnly || !paths[port] ? undefined : pcbPath.parse(paths[port])
}
