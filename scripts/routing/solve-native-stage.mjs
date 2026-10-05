import { readFileSync, writeFileSync } from "node:fs"
import { SOLVERS } from "@tscircuit/core"

const [stage, startPath, connectionName, outputPath, sourceComponentId, paddingArgument] =
  process.argv.slice(2)
if (!startPath || !connectionName || !outputPath || !["bus_lanes", "fanout"].includes(stage)) {
  throw new Error(
    "Provide bus_lanes|fanout, native start JSON, connection name, output JSON and optional fanout component ID",
  )
}
const capturedStart = JSON.parse(readFileSync(startPath, "utf8"))
const input = structuredClone(capturedStart.simpleRouteJson)
if (!input?.connections || !input.obstacles)
  throw new Error("Expected captured native Simple Route JSON")
input.connections = input.connections.filter((connection) => connection.name === connectionName)
if (input.connections.length !== 1)
  throw new Error("Expected exactly one selected original connection")
if (input.differentialPairs?.some((pair) => pair.connectionNames.includes(connectionName)))
  throw new Error("Single-connection diagnostics cannot split a differential pair")
if (input.buses?.some((bus) => bus.connectionNames.includes(connectionName)))
  throw new Error("Single-connection diagnostics cannot split a constrained bus")
if (stage === "fanout" && !sourceComponentId)
  throw new Error("Fanout diagnostics require a source component ID")
// Select one native connection while preserving all captured obstacles, existing
// copper and constraints. These diagnostic results require native regeneration
// and independent physical auditing before any route can be accepted.
writeFileSync(`${outputPath}.input.json`, JSON.stringify(input, null, 2))
const options =
  stage === "fanout"
    ? {
        sourceComponentId,
        escapeLayers: ["top", "bottom"],
        traceWidth: input.connections[0].width ?? input.minTraceWidth,
        viaDiameter: input.minViaPadDiameter,
        viaHoleDiameter: input.minViaHoleDiameter,
        clearance: input.minTraceToPadEdgeClearance,
        completeOriginalEndpoints: true,
      }
    : undefined
if (paddingArgument !== undefined) {
  if (stage !== "fanout" || !sourceComponentId)
    throw new Error("Fanout padding requires a source component")
  const paddingMm = Number(paddingArgument)
  if (!Number.isFinite(paddingMm) || paddingMm <= 0)
    throw new Error("Fanout padding must be positive millimeters")
  const sourcePads = input.obstacles.filter(
    (obstacle) => obstacle.componentId === sourceComponentId && !obstacle.isCopperPour,
  )
  if (sourcePads.length === 0) throw new Error("No source pads found for fanout boundary")
  options.sharedBoundary = {
    minX: Math.min(...sourcePads.map((pad) => pad.center.x - pad.width / 2)) - paddingMm,
    maxX: Math.max(...sourcePads.map((pad) => pad.center.x + pad.width / 2)) + paddingMm,
    minY: Math.min(...sourcePads.map((pad) => pad.center.y - pad.height / 2)) - paddingMm,
    maxY: Math.max(...sourcePads.map((pad) => pad.center.y + pad.height / 2)) + paddingMm,
  }
}
writeFileSync(
  `${outputPath}.request.json`,
  JSON.stringify({ stage, sourceComponentId, options }, null, 2),
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
if (solver.failed) throw new Error(solver.error ?? "Native solver failed")
const output = solver.getOutput()
writeFileSync(outputPath, JSON.stringify(output, null, 2))
console.log(JSON.stringify({ solved: solver.solved, outputPath }))
