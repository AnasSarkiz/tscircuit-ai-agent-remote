import { readFileSync, writeFileSync } from "node:fs"
import { any_circuit_element } from "circuit-json"
const dir = "evidence/hold-control-alternate-review-2026-10-03"
const elements = JSON.parse(readFileSync(`${dir}/circuit.json`, "utf8"))
const failures = elements.flatMap((element: unknown, index: number) => {
  const result = any_circuit_element.safeParse(element)
  if (result.success) return []
  return [{ index, type: (element as { type: string }).type, issues: result.error.issues.map(issue => ({ code: issue.code, path: issue.path, message: issue.message })) }]
})
const counts: Record<string, number> = {}
for (const element of elements) counts[element.type] = (counts[element.type] ?? 0) + 1
writeFileSync(`${dir}/native-schema-summary.json`, JSON.stringify({ schema: "circuit-json@0.0.510 any_circuit_element, unchanged", elements: elements.length, counts, failing_elements: failures.length, failures }, null, 2) + "\n")
console.log(JSON.stringify({ counts, failing_elements: failures.length }))
