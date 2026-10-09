import { readFileSync, writeFileSync, mkdirSync } from "node:fs"
import { createHash } from "node:crypto"
import { convertCircuitJsonToGerberFiles } from "circuit-json-to-gerber"
const path = process.argv[2]
const output = process.argv[3]
const bytes = readFileSync(path)
const files = convertCircuitJsonToGerberFiles(JSON.parse(bytes))
mkdirSync(output, { recursive: true })
const manifest = []
for (const [name, content] of Object.entries(files)) {
  writeFileSync(`${output}/${name}`, content)
  manifest.push({ name, bytes: Buffer.byteLength(content), sha256: createHash("sha256").update(content).digest("hex") })
}
writeFileSync(`${output}/manifest.json`, JSON.stringify({ source_sha256: createHash("sha256").update(bytes).digest("hex"), converter: "circuit-json-to-gerber@0.0.112-board-fixes.1", classification: "Actual unchanged-native Gerber and Excellon exports; engineering review only, NOT FOR FABRICATION", fabrication_ready: false, files: manifest }, null, 2) + "\n")
console.log(JSON.stringify(manifest.map(file => ({ name: file.name, bytes: file.bytes }))))
