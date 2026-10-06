import { createHash } from "node:crypto"
import { readFileSync, writeFileSync } from "node:fs"
import { SOLVERS } from "@tscircuit/core"

const [inputPath, firstName, secondName, outputPath, stage = "bus_lanes", sourceComponentId] =
  process.argv.slice(2)
if (!outputPath) throw new Error("Expected native SRJ, both connection names and output path")
const raw = readFileSync(inputPath)
const input = JSON.parse(raw)
const selected = new Set([firstName, secondName])
const pair = input.differentialPairs?.find(
  (pair) =>
    pair.connectionNames.length === 2 && pair.connectionNames.every((name) => selected.has(name)),
)
if (!pair) throw new Error("Select the complete original differential pair")
input.connections = input.connections.filter((connection) => selected.has(connection.name))
if (input.connections.length !== 2) throw new Error("Expected both original connections")
input.differentialPairs = [pair]
if (input.buses?.some((bus) => bus.connectionNames.some((name) => selected.has(name))))
  throw new Error("Pair also belongs to a constrained bus; preserve the complete bus")
input.buses = []
// Preserve the genuine native obstacles, outline, pair constraints, widths and
// through-via geometry. A solver success is only a proposal: native regeneration
// and independent continuity, clearance and width audits remain mandatory.
writeFileSync(`${outputPath}.input.json`, JSON.stringify(input, null, 2))
if (!["bus_lanes", "fanout"].includes(stage)) throw new Error("Expected bus_lanes or fanout")
if (stage === "fanout" && !sourceComponentId)
  throw new Error("Fanout requires the actual native source component ID")
const options =
  stage === "fanout"
    ? {
        sourceComponentId,
        escapeLayers: ["top", "bottom"],
        traceWidth: 0.275,
        viaDiameter: input.minViaPadDiameter,
        viaHoleDiameter: input.minViaHoleDiameter,
        clearance: input.minTraceToPadEdgeClearance,
        completeOriginalEndpoints: true,
      }
    : undefined
writeFileSync(
  `${outputPath}.request.json`,
  JSON.stringify(
    {
      source_sha256: createHash("sha256").update(raw).digest("hex"),
      selected_connection_names: [...selected],
      differential_pair: pair,
      obstacle_count: input.obstacles.length,
      stage,
      options,
    },
    null,
    2,
  ),
)
const solver =
  stage === "fanout"
    ? new SOLVERS.FanoutSolver(input, options)
    : new SOLVERS.BusLanesPipelineSolver(input)
let lastReportAt = 0
while (!solver.solved && !solver.failed) {
  solver.step()
  if (Date.now() - lastReportAt >= 5000) {
    console.log(
      JSON.stringify({
        phase: solver.phase,
        progress: solver.progress,
        iterations: solver.iterations,
      }),
    )
    lastReportAt = Date.now()
    await new Promise((resolve) => setTimeout(resolve, 0))
  }
}
writeFileSync(
  `${outputPath}.solver-outcome.json`,
  JSON.stringify(
    {
      solved: solver.solved,
      failed: solver.failed,
      error: solver.error,
      phase: solver.phase,
      iterations: solver.iterations,
    },
    null,
    2,
  ),
)
if (solver.failed) throw new Error(solver.error ?? "Native paired solver failed")
const output = solver.getOutput()
writeFileSync(outputPath, JSON.stringify(output, null, 2))
console.log(JSON.stringify({ solved: solver.solved, outputPath }))
