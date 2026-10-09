import { expect, test } from "bun:test"
import { createHash } from "node:crypto"
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs"
import { tmpdir } from "node:os"
import { join, resolve } from "node:path"

function fixture() {
  const directory = mkdtempSync(join(tmpdir(), "registry-binary-"))
  const files = [
    { path: "circuit.json", data: Buffer.from('{"label":"µ-controller"}') },
    { path: "runtime.tgz", data: Buffer.from([0x1f, 0x8b, 0, 0xff, 0x80, 0, 0x61]) },
  ]
  for (const file of files) writeFileSync(join(directory, file.path), file.data)
  const receipt = join(directory, "receipt.json")
  writeFileSync(
    receipt,
    JSON.stringify({
      version: "AnasSarkiz/tscircuit-ai-agent-remote@test-only",
      is_private: false,
      is_unlisted: false,
      missing_files: files.map((file) => file.path),
      missing_from_list: files.map((file) => file.path),
      extra_remote_files: [],
      unverified_or_mismatched_files: [],
      matching_files: 0,
      expected_files: files.length,
      files: files.map((file) => ({
        path: file.path,
        local_sha256: createHash("sha256").update(file.data).digest("hex"),
      })),
    }),
  )
  const output = join(directory, "output.json")
  const run = () =>
    Bun.spawnSync([
      process.execPath,
      resolve("scripts/resume-registry-upload.mjs"),
      "--receipt",
      receipt,
      "--output",
      output,
      "--stage",
      directory,
    ])
  return { directory, files, output, run }
}

test("registry archives retain binary bytes and Unicode JSON without uploading", () => {
  const f = fixture()
  try {
    const result = f.run()
    expect(result.exitCode).toBe(0)
    const record = JSON.parse(readFileSync(f.output, "utf8"))
    expect(record.round_trip_byte_verified).toBe(true)
    expect(record.uploaded).toBe(false)
    expect(record.files.map((file: { sha256: string }) => file.sha256)).toEqual(
      f.files.map((file) => createHash("sha256").update(file.data).digest("hex")),
    )
  } finally {
    rmSync(f.directory, { recursive: true, force: true })
  }
})

test("registry resume rejects binary artifact changes after anonymous verification", () => {
  const f = fixture()
  try {
    writeFileSync(join(f.directory, "runtime.tgz"), Buffer.from([0, 0xff, 0x7f]))
    const result = f.run()
    expect(result.exitCode).not.toBe(0)
    expect(result.stderr.toString()).toContain("Staged file changed after verification")
  } finally {
    rmSync(f.directory, { recursive: true, force: true })
  }
})
