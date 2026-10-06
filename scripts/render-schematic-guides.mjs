import { readFileSync, mkdirSync, writeFileSync } from "node:fs"
import { join } from "node:path"
import { convertCircuitJsonToSchematicSvg } from "circuit-to-svg"
import sharp from "sharp"

const [circuitPath, outputDirectory] = process.argv.slice(2)
if (!circuitPath || !outputDirectory)
  throw new Error("Provide native Circuit JSON and schematic output directory")
const circuitJson = JSON.parse(readFileSync(circuitPath, "utf8"))
mkdirSync(outputDirectory, { recursive: true })
const sheets = circuitJson.filter((element) => element.type === "schematic_sheet")
for (const sheet of sheets) {
  const svg = convertCircuitJsonToSchematicSvg(circuitJson, {
    schematicSheetId: sheet.schematic_sheet_id,
    width: 1600,
    height: 1000,
  })
  const basename = `${String(sheet.sheet_index).padStart(2, "0")}-${sheet.name}`
  writeFileSync(join(outputDirectory, `${basename}.svg`), svg)
  await sharp(Buffer.from(svg))
    .png()
    .toFile(join(outputDirectory, `${basename}.png`))
}
console.log(JSON.stringify({ sheets_rendered: sheets.length, native_circuit: circuitPath }))
