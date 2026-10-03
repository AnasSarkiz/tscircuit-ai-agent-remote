import { readFileSync, writeFileSync } from "node:fs"
import { any_circuit_element, pcb_component, pcb_group, schematic_group } from "circuit-json"
import { z } from "zod"

const folder = "evidence/hold-readback-review-2026-10-03"
const elements = z.array(z.object({ type: z.string() }).passthrough()).parse(
  JSON.parse(readFileSync(`${folder}/circuit.json`, "utf8")),
)
const failures = elements.flatMap((element, index) => {
  const result = any_circuit_element.safeParse(element)
  if (result.success) return []
  const specificResult = element.type === "pcb_component" ? pcb_component.safeParse(element)
    : element.type === "pcb_group" ? pcb_group.safeParse(element)
    : element.type === "schematic_group" ? schematic_group.safeParse(element) : undefined
  return [{ index, type: element.type, issues: result.error.issues.map((issue) => ({
    code: issue.code, path: issue.path, message: issue.message,
  })), specific_unchanged_schema_issues: specificResult && !specificResult.success
    ? specificResult.error.issues.map((issue) => ({ code: issue.code, path: issue.path, message: issue.message }))
    : [] }]
})
const counts: Record<string, number> = {}
for (const element of elements) counts[element.type] = (counts[element.type] ?? 0) + 1
writeFileSync(`${folder}/native-schema-summary.json`, JSON.stringify({
  schema: "circuit-json@0.0.510 any_circuit_element, unchanged",
  elements: elements.length,
  counts,
  failing_elements: failures.length,
  failures,
}, null, 2) + "\n")
console.log(JSON.stringify({ counts, failing_elements: failures.length }))
