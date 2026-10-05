import { readFileSync, writeFileSync } from "node:fs"
import { AutoroutingPipelineSolver9_PreloadedTraceGraph } from "@tscircuit/capacity-autorouter"

const [capturePath, outputPath] = process.argv.slice(2)
if (!capturePath || !outputPath) throw new Error("Provide native start-event JSON and output JSON")
const capturedStart = JSON.parse(readFileSync(capturePath, "utf8"))
if (
  capturedStart.solverName !== "AutoroutingPipelineSolver9_PreloadedTraceGraph" ||
  capturedStart.autorouterVersion !== "beta_pipeline9" ||
  !capturedStart.simpleRouteJson
) {
  throw new Error("Expected an actual native Pipeline9 start event")
}
// Use the documented library API on the exact captured input, without generating
// intermediate visualization frames or modifying geometry or tolerances.
const solver = new AutoroutingPipelineSolver9_PreloadedTraceGraph(capturedStart.simpleRouteJson, {
  effort: capturedStart.effort ?? 1,
})
let lastReportAt = 0
while (!solver.solved && !solver.failed) {
  solver.step()
  if (Date.now() - lastReportAt >= 10000) {
    lastReportAt = Date.now()
    console.log(
      JSON.stringify({
        phase: solver.getCurrentPhase(),
        progress: solver.progress,
        iterations: solver.iterations,
      }),
    )
    await new Promise((resolve) => setTimeout(resolve, 0))
  }
}
if (solver.failed) throw new Error(solver.error ?? "Pipeline9 failed")
writeFileSync(outputPath, JSON.stringify(solver.getOutputSimpleRouteJson(), null, 2))
console.log(JSON.stringify({ solved: solver.solved, timeSpentOnPhase: solver.timeSpentOnPhase }))
