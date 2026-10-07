import { createHash } from "node:crypto"
import { readFileSync, writeFileSync } from "node:fs"
import { isDeepStrictEqual } from "node:util"
import { pcb_component } from "circuit-json"

const folder = "evidence/routing-continuation-2026-10-07"
const beforeBytes = readFileSync(`${folder}/speaker-local-native-v7/circuit.json`)
const afterBytes = readFileSync(`${folder}/final-cli-native/circuit.json`)
const before = JSON.parse(beforeBytes)
const after = JSON.parse(afterBytes)
const geometryTypes = new Set([
  "pcb_board", "pcb_component", "pcb_port", "pcb_smtpad", "pcb_plated_hole",
  "pcb_hole", "cad_component", "pcb_trace", "pcb_via", "pcb_copper_pour", "pcb_keepout",
])
const geometry = (records) => records.filter((record) => geometryTypes.has(record.type)).map((record) => {
  if (record.type !== "pcb_component") return record
  const { supplier_pin1_location_map, ...physicalRecord } = record
  return physicalRecord
})
const additions = after.filter((record) => record.type === "pcb_component" && record.supplier_pin1_location_map)
for (const record of additions) {
  pcb_component.shape.supplier_pin1_location_map.parse(record.supplier_pin1_location_map)
}
const purchased = (records) => records.filter((record) => record.type === "source_component" && record.supplier_part_numbers?.jlcpcb)
const sourcePorts = (records) => records.filter((record) => record.type === "source_port")
const passed = isDeepStrictEqual(geometry(before), geometry(after)) && additions.length === 125 &&
  isDeepStrictEqual(purchased(before), purchased(after)) && isDeepStrictEqual(sourcePorts(before), sourcePorts(after))
const receipt = {
  before_native_sha256: createHash("sha256").update(beforeBytes).digest("hex"),
  official_cli_native_sha256: createHash("sha256").update(afterBytes).digest("hex"),
  all_physical_records_identical_except_added_supplier_pin1_location_map: isDeepStrictEqual(geometry(before), geometry(after)),
  supplier_maps_added_and_independently_field_schema_validated: additions.length,
  all_125_purchased_source_records_identical: isDeepStrictEqual(purchased(before), purchased(after)),
  all_numbered_source_ports_identical: isDeepStrictEqual(sourcePorts(before), sourcePorts(after)),
  full_native_schema_qualified: false,
  generated_json_modified: false,
  passed,
}
writeFileSync(`${folder}/verified-cli-enrichment.json`, `${JSON.stringify(receipt, null, 2)}\n`)
console.log(JSON.stringify(receipt))
if (!passed) process.exit(1)
