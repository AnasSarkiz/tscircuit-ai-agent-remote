import { RootCircuit, getSimpleRouteJsonFromCircuitJson } from "@tscircuit/core"
import { createHash } from "node:crypto"
import { relative } from "node:path"
import { plugin } from "bun"

plugin({
  name: "routing-source-assets",
  setup(builder) {
    builder.onLoad({ filter: /\.(obj|step)$/ }, ({ path }) => ({
      contents: `export default ${JSON.stringify(`./${relative(process.cwd(), path)}`)}`,
      loader: "js",
    }))
  },
})
const [nativePath, outputPath] = Bun.argv.slice(2)
if (!nativePath || !outputPath) throw new Error("Provide untouched native JSON and output SRJ")
const { default: Board } = await import("../../main")
const nativeBytes = await Bun.file(nativePath).arrayBuffer()
// The installed public converter accepts native Circuit JSON. Its source
// component supplies the real differential-pair declarations; no constraints,
// pad shapes, endpoints, tolerances or saved routes are invented here.
// Use the native generator's declared output type. Full strict-schema
// qualification runs separately and its failures remain explicit; exporting
// this diagnostic does not assert that the installed schema accepts the board.
const native: ReturnType<RootCircuit["getCircuitJson"]> = JSON.parse(
  new TextDecoder().decode(nativeBytes),
)
const root = new RootCircuit()
root.pcbDisabled = true
root.schematicDisabled = true
root.add(<Board placementOnly />)
await root.renderUntilSettled()
const source = root.getCircuitJson()
const components = new Map(
  source.filter((r) => r.type === "source_component").map((r) => [r.source_component_id, r.name]),
)
const nativeComponents = new Map(
  native.filter((r) => r.type === "source_component").map((r) => [r.source_component_id, r.name]),
)
const sourceIds = new Map(
  source
    .filter((r) => r.type === "source_port")
    .map((r) => [`${components.get(r.source_component_id!)}.${r.name}`, r.source_port_id]),
)
for (const port of native.filter((r) => r.type === "source_port")) {
  if (!port.source_component_id || !nativeComponents.has(port.source_component_id)) continue
  const label = `${nativeComponents.get(port.source_component_id)}.${port.name}`
  if (sourceIds.get(label) !== port.source_port_id)
    throw new Error(`Source-only port identity differs from native input: ${label}`)
}
const board = root._getBoard()
if (!board) throw new Error("Actual source board is unavailable")
const nativeBoard = native.find((r) => r.type === "pcb_board")
if (!nativeBoard) throw new Error("The original native board is unavailable")
const { simpleRouteJson } = getSimpleRouteJsonFromCircuitJson({
  circuitJson: native,
  subcircuit_id: nativeBoard.subcircuit_id,
  subcircuitComponent: board,
  minTraceWidth: 0.2,
  minTraceToPadEdgeClearance: 0.2,
  minTraceToHoleEdgeClearance: 0.25,
  minPadEdgeToPadEdgeClearance: 0.1,
  minBoardEdgeClearance: 0.25,
  minViaEdgeToPadEdgeClearance: 0.2,
  minViaHoleEdgeToViaHoleEdgeClearance: 0.25,
  minPlatedHoleDrillEdgeToDrillEdgeClearance: 0.25,
  minViaHoleDiameter: 0.3,
  minViaPadDiameter: 0.45,
  ignoreExistingTopLevelPcbRouteState: false,
})
await Bun.write(outputPath, JSON.stringify(simpleRouteJson, null, 2))
const summary = {
  classification:
    "Installed native conversion of untouched copper with actual source pair declarations; diagnostic input, never a solver cache or fabrication approval",
  native_sha256: createHash("sha256").update(new Uint8Array(nativeBytes)).digest("hex"),
  source_port_identity_verified: true,
  connections: simpleRouteJson.connections.map((c) => ({
    name: c.name,
    points: c.pointsToConnect,
  })),
  differentialPairs: simpleRouteJson.differentialPairs,
  obstacles: simpleRouteJson.obstacles.length,
  existing_traces: simpleRouteJson.traces?.length,
}
await Bun.write(`${outputPath}.receipt.json`, JSON.stringify(summary, null, 2))
console.log(
  JSON.stringify({
    obstacles: summary.obstacles,
    connections: summary.connections.length,
    pairs: summary.differentialPairs?.length,
  }),
)
