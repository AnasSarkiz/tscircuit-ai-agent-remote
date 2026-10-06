import { createHash } from "node:crypto"
import { readFileSync, writeFileSync } from "node:fs"
import { any_circuit_element } from "circuit-json"
import { convertCircuitJsonToPickAndPlaceRows, convertCircuitJsonToPickAndPlaceCsv } from "circuit-json-to-pnp-csv"
import { convertCircuitJsonToBomRows, convertBomRowsToCsv } from "../bom-export-review-2026-10-03/runtime/node_modules/circuit-json-to-bom-csv/dist/index.js"

const folder = process.argv[3] ?? "evidence/order-readiness-2026-10-06"
const nativeBytes = readFileSync(process.argv[2] ?? `${folder}/native-build/circuit.json`)
const circuitJson = JSON.parse(nativeBytes.toString("utf8"))
const source_sha256 = createHash("sha256").update(nativeBytes).digest("hex")
const by_type = {}
const failures = []
for (const [index, element] of circuitJson.entries()) {
  const result = any_circuit_element.safeParse(element)
  if (result.success) continue
  by_type[element.type] = (by_type[element.type] ?? 0) + 1
  failures.push({ index, type: element.type, issues: result.error.issues })
}
writeFileSync(`${folder}/schema-audit.json`, JSON.stringify({
  source_sha256, schema_package: "circuit-json@0.0.517", failing_elements: failures.length, by_type, failures,
}, null, 2) + "\n")

// Exact official converter calls on the untouched native array. These are
// diagnostic exports, explicitly withheld from a fabrication package.
const bomRows = await convertCircuitJsonToBomRows({ circuitJson })
const rotationWarnings = []
const pnpOptions = { supplier: "jlcpcb", onRotationWarning: warning => rotationWarnings.push(warning) }
const pnpRows = convertCircuitJsonToPickAndPlaceRows(circuitJson, pnpOptions)
writeFileSync(`${folder}/NOT-FOR-FABRICATION-bom.csv`, convertBomRowsToCsv(bomRows))
writeFileSync(`${folder}/NOT-FOR-FABRICATION-pick-and-place.csv`, convertCircuitJsonToPickAndPlaceCsv(circuitJson, { supplier: "jlcpcb", onRotationWarning: warning => console.warn(JSON.stringify(warning)) }))
let strict_rotation_error = null
try {
  convertCircuitJsonToPickAndPlaceRows(circuitJson, { supplier: "jlcpcb", requireSupplierRotation: true })
} catch (error) {
  strict_rotation_error = error.message
}
const summary = {
  source_sha256, fabrication_ready: false,
  scope: "Official BOM 0.0.19 and PnP 0.0.16 converters, not a fabrication package. Full installed schema tested independently without changing the input. Strict supplier rotation qualification error retained.",
  bom_rows: bomRows.length,
  blank_bom_comment_count: bomRows.filter(row => !row.comment.trim()).length,
  supplier_code_as_footprint_count: bomRows.filter(row => /^C[0-9]+$/.test(row.footprint)).length,
  pnp_rows: pnpRows.length, all_pnp_top: pnpRows.every(row => row.layer === "top"),
  rotationWarnings, strict_rotation_error,
}
writeFileSync(`${folder}/assembly-export-audit.json`, JSON.stringify(summary, null, 2) + "\n")
console.log(JSON.stringify({ failing_schema_elements: failures.length, by_type, ...summary }))
process.exit(failures.length || summary.blank_bom_comment_count || summary.supplier_code_as_footprint_count || strict_rotation_error ? 1 : 0)
