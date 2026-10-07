import { RootCircuit } from "tscircuit"
import { getPlatformConfig } from "@tscircuit/eval"
import { relative } from "node:path"
import { plugin } from "bun"

plugin({
  name: "board-asset-paths",
  setup(builder) {
    builder.onLoad({ filter: /\.(obj|step)$/ }, ({ path }) => ({
      contents: `export default ${JSON.stringify(`./${relative(process.cwd(), path)}`)}`,
      loader: "js",
    }))
  },
})
const { default: Board } = await import("../../main")
const outputPath = Bun.argv[2]
if (!outputPath) throw new Error("Provide native placement output path")
// Use the official supplier/asset platform, as the CLI does. This generates
// real supplier orientation metadata; no routed JSON is copied into placement.
const root = new RootCircuit({ platform: getPlatformConfig() })
root.on("autorouting:start", () => {
  throw new Error("Placement-only mode must never run a router")
})
root.add(<Board placementOnly />)
await root.renderUntilSettled()
const circuitJson = root.getCircuitJson()
if (
  circuitJson.some((element) => ["pcb_trace", "pcb_via", "pcb_copper_pour"].includes(element.type))
) {
  throw new Error("Placement-only mode emitted copper")
}
await Bun.write(outputPath, JSON.stringify(circuitJson, null, 2))
console.log(
  JSON.stringify({
    outputPath,
    nativeErrors: circuitJson.filter((element) => element.type.includes("error")).length,
  }),
)
