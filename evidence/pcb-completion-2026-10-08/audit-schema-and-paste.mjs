import { readFileSync, writeFileSync } from "node:fs"
import { createHash } from "node:crypto"
import * as schemas from "circuit-json"
const path = process.argv[2]
const directory = process.argv[3]
const bytes = readFileSync(path)
const circuit = JSON.parse(bytes)
const failures = []
for (const [index, element] of circuit.entries()) {
  if (schemas.any_circuit_element.safeParse(element).success) continue
  const schema = schemas[element.type]
  const parsed = schema?.safeParse(element)
  failures.push({ index, type: element.type, issues: parsed?.error?.issues })
}
const pads = circuit.filter(element => element.type === "pcb_smtpad" && !element.is_covered_with_solder_mask)
const paste = circuit.filter(element => element.type === "pcb_solder_paste")
const missing = pads.filter(pad => !paste.some(aperture => aperture.pcb_smtpad_id === pad.pcb_smtpad_id))
const pillPads = pads.filter(pad => ["pill", "rotated_pill"].includes(pad.shape))
const wrongPillGeometry = []
for (const pad of pillPads) {
  const apertures = paste.filter(aperture => aperture.pcb_smtpad_id === pad.pcb_smtpad_id)
  if (apertures.length !== 1 || apertures.some(aperture => aperture.layer !== pad.layer || aperture.x !== pad.x || aperture.y !== pad.y || (aperture.ccw_rotation ?? 0) !== (pad.ccw_rotation ?? 0))) wrongPillGeometry.push(pad.pcb_smtpad_id)
}
const result = { source_sha256: createHash("sha256").update(bytes).digest("hex"), schema_version: "0.0.521-board-fixes.1", schema_failures: failures.length, failures, exposed_smt_pad_count: pads.length, paste_count: paste.length, missing_paste_count: missing.length, missing_paste: missing.map(pad => pad.pcb_smtpad_id), pill_pad_count: pillPads.length, wrong_pill_paste_geometry: wrongPillGeometry, fabrication_ready: false }
writeFileSync(`${directory}/schema-and-paste.json`, JSON.stringify(result, null, 2) + "\n")
console.log(JSON.stringify({ ...result, failures: undefined, missing_paste: undefined }))
process.exit(failures.length || missing.length || wrongPillGeometry.length ? 1 : 0)
