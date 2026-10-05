import { createHash } from "node:crypto"
import { readFileSync, realpathSync, writeFileSync } from "node:fs"
import { createRequire } from "node:module"
import { dirname, join, relative, resolve } from "node:path"
import { fileURLToPath } from "node:url"
import { parseArgs } from "node:util"
import { gunzipSync, gzipSync } from "node:zlib"
import { z } from "zod"

const projectDir = resolve(dirname(fileURLToPath(import.meta.url)), "..")
const verificationReceipt = z.object({
  version: z.string().regex(/^[^/]+\/[^@]+@.+$/),
  is_private: z.literal(false),
  is_unlisted: z.literal(false),
  missing_files: z.array(z.string()).min(1),
  missing_from_list: z.array(z.string()),
  extra_remote_files: z.array(z.string()).length(0),
  unverified_or_mismatched_files: z.array(z.string()).length(0),
  matching_files: z.number().int().nonnegative(),
  expected_files: z.number().int().positive(),
  files: z.array(
    z.object({
      path: z.string(),
      local_sha256: z.string().regex(/^[a-f0-9]{64}$/),
    }),
  ),
})
const uploadResponse = z.object({
  ok: z.literal(true),
  package_files: z.array(
    z.object({
      package_file_id: z.string(),
      file_path: z.string(),
    }),
  ),
})

function sha256(payload) {
  return createHash("sha256").update(payload).digest("hex")
}

function prepareArchive(options) {
  const receipt = verificationReceipt.parse(JSON.parse(readFileSync(options.receipt, "utf8")))
  if (receipt.matching_files + receipt.missing_files.length !== receipt.expected_files) {
    throw new Error("Every existing remote file must already be verified before resuming")
  }
  if (
    receipt.missing_files.slice().sort().join("\n") !==
    receipt.missing_from_list.slice().sort().join("\n")
  ) {
    throw new Error("Missing-file metadata must agree")
  }
  const stage = realpathSync(resolve(options.stage))
  for (const entry of receipt.files) {
    const localPath = realpathSync(resolve(stage, entry.path))
    if (relative(stage, localPath).startsWith("..")) throw new Error("File escapes package staging")
    if (sha256(readFileSync(localPath)) !== entry.local_sha256) {
      throw new Error(`Staged file changed after verification: ${entry.path}`)
    }
  }
  const originals = receipt.missing_files.map((filePath) => ({
    filePath,
    bytes: readFileSync(join(stage, filePath)),
  }))
  const files = originals.map((original) => {
    const text = original.bytes.toString("utf8")
    if (!Buffer.from(text).equals(original.bytes)) {
      throw new Error(
        `This text archive uploader does not support binary file: ${original.filePath}`,
      )
    }
    return { file_path: original.filePath, content_text: text }
  })
  const archive = gzipSync(JSON.stringify({ files }), { level: 9 })
  const decoded = JSON.parse(gunzipSync(archive).toString("utf8"))
  for (const [index, original] of originals.entries()) {
    if (
      decoded.files[index].file_path !== original.filePath ||
      !Buffer.from(decoded.files[index].content_text).equals(original.bytes)
    ) {
      throw new Error("Archive round-trip verification failed")
    }
  }
  const maxArchiveBytes = options["max-archive-bytes"]
    ? z.coerce.number().int().positive().parse(options["max-archive-bytes"])
    : undefined
  const fileGroups = []
  let currentFiles = []
  let currentCompressedBytes = 0
  for (const file of files) {
    const compressedBytes = gzipSync(JSON.stringify({ files: [file] }), { level: 9 }).length
    if (maxArchiveBytes && compressedBytes > maxArchiveBytes)
      throw new Error(`File exceeds the selected archive budget: ${file.file_path}`)
    if (
      maxArchiveBytes &&
      currentFiles.length &&
      currentCompressedBytes + compressedBytes > maxArchiveBytes
    ) {
      fileGroups.push(currentFiles)
      currentFiles = []
      currentCompressedBytes = 0
    }
    currentFiles.push(file)
    currentCompressedBytes += compressedBytes
  }
  if (currentFiles.length) fileGroups.push(currentFiles)
  const archives = fileGroups.map((group) => {
    const payload = gzipSync(JSON.stringify({ files: group }), { level: 9 })
    if (maxArchiveBytes && payload.length > maxArchiveBytes)
      throw new Error("Compressed archive exceeds the selected budget")
    const decodedGroup = JSON.parse(gunzipSync(payload).toString("utf8"))
    if (JSON.stringify(decodedGroup.files) !== JSON.stringify(group))
      throw new Error("Chunk archive round-trip verification failed")
    return { payload, paths: group.map((file) => file.file_path) }
  })
  return {
    receipt,
    archive,
    archives,
    files: originals.map((original) => ({
      path: original.filePath,
      bytes: original.bytes.length,
      sha256: sha256(original.bytes),
    })),
  }
}

async function uploadArchive(prepared) {
  const listingResponse = await fetch("https://registry-api.tscircuit.com/package_files/list", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ package_name_with_version: prepared.receipt.version }),
    signal: AbortSignal.timeout(30_000),
  })
  if (!listingResponse.ok)
    throw new Error(`Remote file listing failed with HTTP${listingResponse.status}`)
  const listing = z
    .object({
      package_files: z.array(z.object({ file_path: z.string() })),
    })
    .parse(await listingResponse.json())
  const remotePaths = new Set(
    listing.package_files.map((file) => file.file_path.replace(/^\//, "")),
  )
  const expectedPaths = prepared.receipt.files.map((file) => file.path)
  const currentlyMissing = expectedPaths.filter((path) => !remotePaths.has(path)).sort()
  if (
    currentlyMissing.join("\n") !== prepared.receipt.missing_files.slice().sort().join("\n") ||
    [...remotePaths].some((path) => !expectedPaths.includes(path))
  ) {
    throw new Error("Remote file set changed; obtain a fresh verification receipt before uploading")
  }
  // Use the public Conf SDK and the CLI's existing configured credential store.
  // Credentials stay in memory and are never printed, copied, or put in outputs.
  const require = createRequire(join(projectDir, ".tools/registry-client/package.json"))
  const { default: Conf } = await import(require.resolve("conf"))
  const config = new Conf({ projectName: "tscircuit", cwd: process.env.TSCIRCUIT_CONFIG_DIR })
  const handle = config.get("tscircuitHandle")
  const sessionToken = config.get("sessionToken")
  if (typeof sessionToken !== "string" || !sessionToken)
    throw new Error("Native CLI login is required")
  if (handle !== prepared.receipt.version.split("/")[0])
    throw new Error("Authenticated owner does not match release")
  const registryUrl = config.get("registryApiUrl") ?? "https://registry-api.tscircuit.com"
  if (registryUrl !== "https://registry-api.tscircuit.com")
    throw new Error("Unexpected registry destination")
  const uploadedFiles = []
  for (const [archiveIndex, archive] of prepared.archives.entries()) {
    const form = new FormData()
    form.set("package_name_with_version", prepared.receipt.version)
    form.set(
      "archive",
      new File([archive.payload], "missing-package-files.json.gz", {
        type: "application/gzip",
      }),
    )
    const response = await fetch(`${registryUrl}/package_files/upload_archive`, {
      method: "POST",
      headers: { Authorization: `Bearer ${sessionToken}` },
      body: form,
      signal: AbortSignal.timeout(300_000),
    })
    if (!response.ok) throw new Error(`Archive upload failed with HTTP${response.status}`)
    const uploaded = uploadResponse.parse(await response.json())
    const paths = uploaded.package_files.map((file) => file.file_path.replace(/^\//, "")).sort()
    if (paths.join("\n") !== archive.paths.slice().sort().join("\n")) {
      throw new Error("Registry response does not contain every requested file")
    }
    uploadedFiles.push(...uploaded.package_files)
    console.log(
      JSON.stringify({
        archive_index: archiveIndex,
        archive_bytes: archive.payload.length,
        archive_sha256: sha256(archive.payload),
        http_status: response.status,
        uploaded_files: uploaded.package_files,
      }),
    )
  }
  return {
    http_status: 200,
    verified_owner: handle,
    uploaded_files: uploadedFiles,
  }
}

async function main() {
  const { values: options } = parseArgs({
    options: {
      receipt: { type: "string" },
      output: { type: "string" },
      stage: { type: "string", default: ".publish/board" },
      upload: { type: "boolean", default: false },
      "max-archive-bytes": { type: "string" },
    },
  })
  if (!options.receipt || !options.output) throw new Error("Specify --receipt and --output")
  const prepared = prepareArchive(options)
  const record = {
    checked_at_utc: new Date().toISOString(),
    version: prepared.receipt.version,
    transport: "Official /package_files/upload_archive multipart form, existing release",
    archive_bytes: prepared.archive.length,
    archive_sha256: sha256(prepared.archive),
    archives: prepared.archives.map((archive) => ({
      bytes: archive.payload.length,
      sha256: sha256(archive.payload),
      paths: archive.paths,
    })),
    round_trip_byte_verified: true,
    files: prepared.files,
    uploaded: false,
  }
  writeFileSync(options.output, `${JSON.stringify(record, null, 2)}\n`)
  if (options.upload) {
    Object.assign(record, await uploadArchive(prepared), { uploaded: true })
    writeFileSync(options.output, `${JSON.stringify(record, null, 2)}\n`)
  }
  console.log(JSON.stringify(record, null, 2))
}

await main()
