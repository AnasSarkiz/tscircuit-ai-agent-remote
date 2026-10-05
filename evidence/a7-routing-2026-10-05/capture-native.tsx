import { RootCircuit } from "tscircuit"
import { relative } from "node:path"
import { readdir } from "node:fs/promises"
import { plugin } from "bun"
import { z } from "zod"

// Standard asset module loading: retain supplier model paths, without changing models.
plugin({ name: "board-asset-paths", setup(builder) {
  builder.onLoad({filter: /\.(obj|step)$/}, ({path}) => ({
    contents: `export default ${JSON.stringify(`./${relative(process.cwd(), path)}`)}`,
    loader: "js",
  }))
}})
const {default: Board} = await import("../../main")
const directory = Bun.argv[2]
if (!directory) throw new Error("Provide output directory")
// Preserve the exact loaded board plan before every subsequent native attempt.
for (const sourcePath of ["main.tsx", "package.json", ...(await readdir("src/board")).filter(path => /\.(tsx?|json)$/.test(path)).map(path => `src/board/${path}`)]) {
  await Bun.write(`${directory}/source-snapshot/${sourcePath}.txt`, await Bun.file(sourcePath).arrayBuffer())
}
const root = new RootCircuit()
const observedRenderPhases = new Set<string>()
root.on("board:renderPhaseStarted", (event) => {
  if (observedRenderPhases.has(event.phase)) return
  observedRenderPhases.add(event.phase)
  console.log(JSON.stringify({ event: "board:renderPhaseStarted", phase: event.phase }))
})
const events: {file: string; phase: string | undefined}[] = []
const writes: Promise<number>[] = []
const routingEvent = z.object({subcircuit_id:z.string(),phaseName:z.string().optional(),pcbTracePaths:z.array(z.unknown()).optional(),pcbTracePathsUnavailableReason:z.string().optional()}).passthrough()
root.on("autorouting:end", (raw: unknown) => {
  const event=routingEvent.parse(raw)
  events.push({file: `event-${events.length + 1}.json`,phase: event.phaseName})
  writes.push(Bun.write(`${directory}/event-${events.length}.json`,JSON.stringify(raw,null,2)))
  console.log(JSON.stringify({event:"autorouting:end",subcircuit:event.subcircuit_id,phase:event.phaseName,paths:event.pcbTracePaths?.length,unavailable:event.pcbTracePathsUnavailableReason}))
})
root.on("autorouting:start", (raw: unknown) => {
  writes.push(Bun.write(`${directory}/start-${writes.length + 1}.json`, JSON.stringify(raw, null, 2)))
  console.log("autorouting:start")
})
let lastProgressAt = 0
root.on("autorouting:progress", (event) => {
  if (Date.now() - lastProgressAt < 10000) return
  lastProgressAt = Date.now()
  console.log(JSON.stringify({ event: event.type, phase: event.phaseName, progress: event.progress, iterationsPerSecond: event.iterationsPerSecond }))
})
// Bound a diagnostic trial, never treat an unfinished render as a passing build.
const budgetMs = Number(Bun.argv[3] ?? 0)
let phaseName: string | undefined
root.on("autorouting:start", (event) => { phaseName = event.phaseName })
const timer = budgetMs > 0 ? setTimeout(async () => {
  await Promise.all(writes)
  await Bun.write(`${directory}/circuit.json`, JSON.stringify(root.getCircuitJson(), null, 2))
  await Bun.write(`${directory}/end-event-index.json`, JSON.stringify(events, null, 2))
  await Bun.write(`${directory}/interruption.json`, JSON.stringify({status:"INCOMPLETE NATIVE RENDER", reason:"Per-trial computation budget reached; all actual native state retained, no passing result inferred", phaseName, budgetMs}, null, 2))
  console.log(JSON.stringify({interrupted:true,phaseName,budgetMs}))
  process.exit(124)
}, budgetMs) : undefined
root.add(<Board />)
await root.renderUntilSettled()
if (timer) clearTimeout(timer)
await Promise.all(writes)
const circuitJson=root.getCircuitJson()
await Bun.write(`${directory}/circuit.json`,JSON.stringify(circuitJson,null,2))
await Bun.write(`${directory}/end-event-index.json`,JSON.stringify(events,null,2))
const counts:Record<string,number>={}
for(const element of circuitJson) counts[element.type]=(counts[element.type]??0)+1
console.log(JSON.stringify({counts},null,2))
