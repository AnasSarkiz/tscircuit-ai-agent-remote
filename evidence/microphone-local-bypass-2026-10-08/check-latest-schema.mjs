// Read-only qualification against the exact official schema package. Never
// rewrite native records or change the active board's locked dependencies.
import { createHash } from 'node:crypto'
import { readFileSync, writeFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import { resolve } from 'node:path'
import { gzipSync, gunzipSync } from 'node:zlib'

const folder = resolve('evidence/microphone-local-bypass-2026-10-08')
const require = createRequire(resolve('.tools/schema-latest/package.json'))
const schemaPath = require.resolve('circuit-json')
const { any_circuit_element } = await import(schemaPath)
const packageJson = JSON.parse(readFileSync(resolve('.tools/schema-latest/node_modules/circuit-json/package.json'), 'utf8'))
if (packageJson.version !== '0.0.521') throw Error('Wrong isolated official schema version')
const payload = readFileSync('dist/index/circuit.json')
const native = JSON.parse(payload)
const failures = [], by_type = {}
for (const [index, record] of native.entries()) {
  const result = any_circuit_element.safeParse(record)
  if (result.success) continue
  by_type[record.type] = (by_type[record.type] ?? 0) + 1
  failures.push({ index, type: record.type, issues: result.error.issues })
}
const raw = Buffer.from(JSON.stringify({ failures }, null, 2) + '\n')
const compressed = gzipSync(raw, { level: 5 })
if (!gunzipSync(compressed).equals(raw)) throw Error('Failure-tree round trip failed')
writeFileSync(`${folder}/latest-schema-failures.json.gz`, compressed)
const receipt = {
  native_sha256: createHash('sha256').update(payload).digest('hex'),
  schema_package: `circuit-json@${packageJson.version}`,
  schema_entrypoint_sha256: createHash('sha256').update(readFileSync(schemaPath)).digest('hex'),
  checked_native_elements: native.length, failing_elements: failures.length, by_type,
  full_failure_tree: 'latest-schema-failures.json.gz',
  full_failure_tree_uncompressed_sha256: createHash('sha256').update(raw).digest('hex'),
  full_failure_tree_archive_sha256: createHash('sha256').update(compressed).digest('hex'),
  exact_archive_round_trip: true, schema_passed: failures.length === 0,
  active_board_dependency_pins_changed: false, native_modified: false, fabrication_ready: false,
}
writeFileSync(`${folder}/latest-schema-receipt.json`, JSON.stringify(receipt, null, 2) + '\n')
console.log(JSON.stringify(receipt))
process.exitCode = failures.length ? 1 : 0
