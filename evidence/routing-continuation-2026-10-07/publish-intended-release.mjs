// Supported registry RPCs, verified against the official create/update routes.
// Use the CLI's existing credential store; never print or persist its token.
import { createRequire } from 'node:module'
import { readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { parseArgs } from 'node:util'
import { z } from 'zod'

const root = resolve(import.meta.dirname, '../..')
const { values } = parseArgs({ options: {
  operation: { type: 'string' }, output: { type: 'string' }, verification: { type: 'string' },
} })
const operation = z.enum(['initialize', 'mark-ready']).parse(values.operation)
if (!values.output) throw Error('Specify output receipt')
const packageJson = JSON.parse(readFileSync(resolve(root, '.publish/board/package.json'), 'utf8'))
const packageName = 'AnasSarkiz/tscircuit-ai-agent-remote'
const version = `${packageName}@${z.string().parse(packageJson.version)}`
if (packageJson.name !== '@tsci/AnasSarkiz.tscircuit-ai-agent-remote') throw Error('Unexpected board package')
const require = createRequire(resolve(root, '.tools/registry-client/package.json'))
const { default: Conf } = await import(require.resolve('conf'))
const config = new Conf({ projectName: 'tscircuit', cwd: process.env.TSCIRCUIT_CONFIG_DIR })
if (config.get('tscircuitHandle') !== 'AnasSarkiz') throw Error('Unexpected authenticated owner')
const token = z.string().min(1).parse(config.get('sessionToken'))
const registry = config.get('registryApiUrl') ?? 'https://registry-api.tscircuit.com'
if (registry !== 'https://registry-api.tscircuit.com') throw Error('Unexpected registry')

async function rpc(endpoint, body) {
  return fetch(`${registry}/${endpoint}`, {
    method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
    body: JSON.stringify(body), signal: AbortSignal.timeout(30_000),
  })
}

const receipt = { checked_at_utc: new Date().toISOString(), version, operation,
  official_route_source_commit: '0b71fe1931d6b2fec518e4b036740ec01f864dec', actions: [] }
if (operation === 'initialize') {
  const existing = await rpc('package_releases/get', { package_name_with_version: version })
  if (existing.status !== 404) throw Error(`Expected verified missing intended release; HTTP${existing.status}`)
  const source = JSON.parse(readFileSync(resolve(root, 'evidence/routing-continuation-2026-10-07/github-publication-receipt.json'), 'utf8'))
  if (!source.passed || source.checked_files !== 126) throw Error('Exact public source must be verified first')
  const response = await rpc('package_releases/create', {
    package_name_with_version: version, is_latest: false, ready_to_build: false, commit_sha: source.commit,
  })
  if (!response.ok) throw Error(`Release creation failed: HTTP${response.status}`)
  const created = z.object({ ok: z.literal(true), package_release: z.object({
    package_release_id: z.string().uuid(), version: z.literal(packageJson.version),
    is_latest: z.literal(false), ready_to_build: z.literal(false),
  }).passthrough() }).parse(await response.json())
  receipt.package_release_id = created.package_release.package_release_id
  receipt.source_commit = source.commit
  receipt.actions.push({ endpoint: 'package_releases/create', http_status: response.status,
    ready_to_build: false, is_latest: false })
  const wrongVersion = `${packageName}@${packageJson.version}-${packageJson.version}`
  const previous = JSON.parse(readFileSync(resolve(root, 'evidence/routing-continuation-2026-10-07/actual-cli-tag-registry-receipt.json'), 'utf8'))
  if (previous.version !== wrongVersion || previous.matching_files !== 124) throw Error('Unexpected accidental tag verification')
  const deactivate = await rpc('package_releases/update', {
    package_name_with_version: wrongVersion, ready_to_build: false, is_latest: false,
  })
  if (!deactivate.ok) throw Error(`Accidental tag deactivation failed: HTTP${deactivate.status}`)
  z.object({ ok: z.literal(true) }).parse(await deactivate.json())
  receipt.actions.push({ endpoint: 'package_releases/update', version: wrongVersion,
    http_status: deactivate.status, ready_to_build: false, is_latest: false })
} else {
  if (!values.verification) throw Error('Specify complete anonymous file verification receipt')
  const verified = JSON.parse(readFileSync(values.verification, 'utf8'))
  if (verified.version !== version || verified.matching_files !== 126 || verified.expected_files !== 126 ||
      verified.is_private !== false || verified.is_unlisted !== false || verified.missing_from_list.length ||
      verified.extra_remote_files.length || verified.unverified_or_mismatched_files.length) {
    throw Error('All exact public files must be verified before marking ready')
  }
  const response = await rpc('package_releases/update', {
    package_name_with_version: version, ready_to_build: true, is_latest: true,
  })
  if (!response.ok) throw Error(`Release readiness update failed: HTTP${response.status}`)
  z.object({ ok: z.literal(true) }).parse(await response.json())
  receipt.actions.push({ endpoint: 'package_releases/update', http_status: response.status,
    ready_to_build: true, is_latest: true })
}
writeFileSync(values.output, `${JSON.stringify(receipt, null, 2)}\n`)
console.log(JSON.stringify(receipt))
