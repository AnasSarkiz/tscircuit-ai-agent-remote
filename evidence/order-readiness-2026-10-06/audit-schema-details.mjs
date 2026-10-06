import { readFileSync, writeFileSync } from "node:fs"
import { createHash } from "node:crypto"
import { pcb_component, pcb_group, schematic_group, pcb_silkscreen_text, pcb_hole } from "circuit-json"

const folder = "evidence/order-readiness-2026-10-06"
const nativeBytes = readFileSync(`${folder}/native-build/circuit.json`)
const schemas = { pcb_component, pcb_group, schematic_group, pcb_silkscreen_text, pcb_hole }
const failures = []
for (const [index, element] of JSON.parse(nativeBytes.toString("utf8")).entries()) {
  const schema = schemas[element.type]
  if (!schema) continue
  const result = schema.safeParse(element)
  if (!result.success) failures.push({ index, type: element.type, issues: result.error.issues })
}
const summary = {
  source_sha256: createHash("sha256").update(nativeBytes).digest("hex"),
  scope: "Specific unmodified installed schemas for the five types that failed the full any_circuit_element audit; full union failure tree separately archived. This does not replace or relax full schema validation.",
  failing_elements: failures.length, failures,
}
writeFileSync(`${folder}/schema-details.json`, JSON.stringify(summary, null, 2) + "\n")
console.log(JSON.stringify({ failing_elements: failures.length }))
process.exit(failures.length ? 1 : 0)
