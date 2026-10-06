import { createHash } from "node:crypto"
import { readFileSync, writeFileSync } from "node:fs"
import { checkPcbBusLengthSkew } from "@tscircuit/checks"

const folder = new URL("./", import.meta.url)
const nativeBytes = readFileSync(new URL("speaker-named-pair-native/circuit.json", folder))
const circuitJson = JSON.parse(nativeBytes.toString("utf8"))
const errors = checkPcbBusLengthSkew(circuitJson)
const nativeError = circuitJson.find((record) => record.type === "pcb_bus_length_skew_error")
const reproduced = errors.some((error) => error.source_bus_id === nativeError.source_bus_id &&
  error.actual_length_skew === nativeError.actual_length_skew &&
  error.maximum_length_skew === nativeError.maximum_length_skew)
if (!reproduced) throw new Error("Installed check did not reproduce the original native finding")
const members = nativeError.source_trace_ids.map((sourceTraceId) => ({
  source_trace: circuitJson.find((record) => record.type === "source_trace" && record.source_trace_id === sourceTraceId),
  native_trace_lengths_mm: circuitJson.filter((record) => record.type === "pcb_trace" && record.source_trace_id === sourceTraceId)
    .map((record) => ({ pcb_trace_id: record.pcb_trace_id, trace_length_mm: record.trace_length })),
}))
const receipt = {
  native_sha256: createHash("sha256").update(nativeBytes).digest("hex"),
  installed_check: "@tscircuit/checks@0.0.237 checkPcbBusLengthSkew",
  input_native_json_changed: false,
  actual_native_error_reproduced: reproduced,
  errors, members,
  finding: "The checker compares each source trace separately. The SPEAKER_N escape and trunk share source_net_64 but are treated as two bus members. Existing SPEAKER_P BREP copper also has no pcb_trace length contribution. This does not qualify the actual full-net skew or coupling.",
  candidate_accepted: false,
  manufacturing_limits_changed: false,
}
writeFileSync(new URL("speaker-skew-reproduction.json", folder), `${JSON.stringify(receipt, null, 2)}\n`)
console.log(JSON.stringify({ reproduced, input_native_json_changed: false, candidate_accepted: false }))
