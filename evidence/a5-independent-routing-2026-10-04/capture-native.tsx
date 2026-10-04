import { RootCircuit } from "tscircuit"
import { relative } from "node:path"
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
const root = new RootCircuit()
const events: unknown[] = []
const writes: Promise<number>[] = []
const routingEvent = z.object({subcircuit_id:z.string(),phaseName:z.string().optional(),pcbTracePaths:z.array(z.unknown()).optional(),pcbTracePathsUnavailableReason:z.string().optional()}).passthrough()
root.on("autorouting:end", (raw: unknown) => {
  const event=routingEvent.parse(raw)
  events.push(raw)
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
root.add(<Board />)
await root.renderUntilSettled()
await Promise.all(writes)
const circuitJson=root.getCircuitJson()
await Bun.write(`${directory}/circuit.json`,JSON.stringify(circuitJson,null,2))
await Bun.write(`${directory}/events.json`,JSON.stringify(events,null,2))
const counts:Record<string,number>={}
for(const element of circuitJson) counts[element.type]=(counts[element.type]??0)+1
console.log(JSON.stringify({counts},null,2))
