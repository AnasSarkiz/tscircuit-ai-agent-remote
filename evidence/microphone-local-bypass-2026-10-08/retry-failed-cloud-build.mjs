// A single supported owned-release rebuild after both automatic platform jobs
// failed before source execution. Never change readiness or inject board props.
import { createHash } from 'node:crypto'
import { readFileSync, writeFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import { resolve } from 'node:path'

const folder = resolve('evidence/microphone-local-bypass-2026-10-08')
const read = name => JSON.parse(readFileSync(`${folder}/${name}`, 'utf8'))
const publication = read('final-registry-receipt.json')
const preview = read('final-public-preview-receipt.json')
if (!publication.complete_public_upload || publication.matching_files !== 128 ||
    publication.version !== 'AnasSarkiz/tscircuit-ai-agent-remote@0.0.10-wip-microphone-bypass' ||
    !preview.exact_native_object_equality) throw Error('Exact public release must be verified first')
for (const file of publication.files) {
  const bytes = readFileSync(resolve('.publish/board', file.path))
  if (createHash('sha256').update(bytes).digest('hex') !== file.local_sha256)
    throw Error('Staged source changed after publication verification')
}
const release = preview.release_id
const listingResponse = await fetch(`https://registry-api.tscircuit.com/package_builds/list?package_release_id=${release}`)
if (!listingResponse.ok) throw Error(`Build listing HTTP ${listingResponse.status}`)
const listing = await listingResponse.json()
if (!Array.isArray(listing.package_builds) || listing.package_builds.length !== 2)
  throw Error('Build set changed; review actual jobs before another request')
const previous = []
for (const entry of listing.package_builds) {
  const response = await fetch(`https://registry-api.tscircuit.com/package_builds/get?package_build_id=${entry.package_build_id}`)
  if (!response.ok) throw Error(`Build read HTTP ${response.status}`)
  const build = (await response.json()).package_build
  if (!build.user_code_job_completed_at || build.build_in_progress ||
      build.user_code_job_error?.error_code !== 'user_code_job_infrastructure_error')
    throw Error('Another job is active or the failure needs code review; no duplicate requested')
  previous.push({ build_id: build.package_build_id, completed_at: build.user_code_job_completed_at,
    error_code: build.user_code_job_error.error_code })
}
const require = createRequire(resolve('.tools/registry-client/package.json'))
const { default: Conf } = await import(require.resolve('conf'))
const config = new Conf({ projectName: 'tscircuit', cwd: process.env.TSCIRCUIT_CONFIG_DIR })
if (config.get('tscircuitHandle') !== 'AnasSarkiz' ||
    (config.get('registryApiUrl') ?? 'https://registry-api.tscircuit.com') !== 'https://registry-api.tscircuit.com')
  throw Error('Configured account or registry does not match verified owned release')
const token = config.get('sessionToken')
if (typeof token !== 'string' || !token) throw Error('Existing native CLI login is required')
const response = await fetch('https://registry-api.tscircuit.com/package_builds/create', {
  method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
  body: JSON.stringify({ package_release_id: release }), signal: AbortSignal.timeout(30_000),
})
if (!response.ok) throw Error(`Supported owned-release rebuild HTTP ${response.status}`)
const result = await response.json()
if (result.ok !== true || !/^[a-f0-9-]{36}$/.test(result.package_build_id)) throw Error('Unexpected rebuild response')
const receipt = { requested_at_utc: new Date().toISOString(), release_id: release,
  package_build_id: result.package_build_id, previous_completed_infrastructure_failures: previous,
  endpoint: 'Official session-authenticated /package_builds/create; no props injected',
  automatic_retry_count: 1, manual_readiness_override: false, credentials_printed_or_saved: false,
  public_native_exact_before_request: true, cloud_build_passed: false, fabrication_ready: false }
writeFileSync(`${folder}/cloud-rebuild-request.json`, JSON.stringify(receipt, null, 2) + '\n')
console.log(JSON.stringify(receipt))
