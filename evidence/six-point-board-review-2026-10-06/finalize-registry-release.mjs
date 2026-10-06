import { readFileSync, writeFileSync } from "node:fs"
import { createRequire } from "node:module"
import { resolve } from "node:path"
const folder = "evidence/six-point-board-review-2026-10-06"
const receipt = JSON.parse(readFileSync(`${folder}/after-bun-resume-registry-receipt.json`, "utf8"))
const version = "AnasSarkiz/tscircuit-ai-agent-remote@0.0.5-wip-style-vias-power"
if (receipt.version !== version || receipt.is_private !== false || receipt.is_unlisted !== false || receipt.matching_files !== 123 || receipt.expected_files !== 123 || [receipt.missing_files, receipt.missing_from_list, receipt.extra_remote_files, receipt.unverified_or_mismatched_files].some(items => items.length)) throw new Error("Complete exact-byte public release verification is required")
const body = { package_name_with_version: version }
const current = await fetch("https://registry-api.tscircuit.com/package_releases/get", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body), signal: AbortSignal.timeout(30_000) })
if (!current.ok) throw new Error(`Release readback HTTP${current.status}`)
const { package_release: release } = await current.json()
if (release?.package_release_id !== "436cf0a3-fcb3-4479-a6b7-7fbbc616cc27") throw new Error("Missing exact release identity")
let changed = false
if (release.ready_to_build !== true) {
  const require = createRequire(resolve(".tools/registry-client/package.json"))
  const { default: Conf } = await import(require.resolve("conf"))
  const config = new Conf({ projectName: "tscircuit", cwd: process.env.TSCIRCUIT_CONFIG_DIR })
  const handle = config.get("tscircuitHandle")
  const sessionToken = config.get("sessionToken")
  if (handle !== "AnasSarkiz" || typeof sessionToken !== "string" || !sessionToken) throw new Error("Existing owner login is required")
  const registry = config.get("registryApiUrl") ?? "https://registry-api.tscircuit.com"
  if (registry !== "https://registry-api.tscircuit.com") throw new Error("Unexpected registry destination")
  // Finish the exact supported publication transition after the failed CLI
  // upload was repaired. No explicit build/rebuild/queue endpoint is called.
  const response = await fetch(`${registry}/package_releases/update`, { method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${sessionToken}` }, body: JSON.stringify({ ...body, ready_to_build: true }), signal: AbortSignal.timeout(30_000) })
  if (!response.ok) throw new Error(`Publication update HTTP${response.status}`)
  const result = await response.json()
  if (result.ok === false) throw new Error("Registry rejected publication update")
  changed = true
}
const record = { checked_at_utc: new Date().toISOString(), version, package_release_id: release.package_release_id, exact_public_files_verified: 123, ready_transition_performed: changed, endpoint: "package_releases/update", explicit_build_or_rebuild_requested: false, fabrication_ready: false }
writeFileSync(`${folder}/registry-finalization-receipt.json`, JSON.stringify(record, null, 2) + "\n")
console.log(JSON.stringify(record))
