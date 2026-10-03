import { readFile, writeFile } from "node:fs/promises"
import { createHash } from "node:crypto"
import { convertCircuitJsonToBomRows, convertBomRowsToCsv } from "circuit-json-to-bom-csv"

const boardDirectory = new URL("../../../", import.meta.url)
const fixturePaths = [
  "evidence/mcu-usb-review-2026-10-03/circuit.json",
  "evidence/charger-battery-ready-review-2026-10-03/circuit.json",
  "evidence/hold-control-alternate-review-2026-10-03/circuit.json",
]
const fixtures = []
for (const fixturePath of fixturePaths) {
  const nativeBytes = await readFile(new URL(fixturePath, boardDirectory))
  const nativeElements = JSON.parse(nativeBytes.toString("utf8"))
  // Exact public API invocation used by the installed CLI's Gerber exporter.
  // No resolver, filtering, schema relaxation or native-output rewrite is added.
  const bomRows = await convertCircuitJsonToBomRows({ circuitJson: nativeElements })
  const resolvedCommentRows = await convertCircuitJsonToBomRows({
    circuitJson: nativeElements,
    resolvePart: async ({ source_component }) => ({ comment: source_component.manufacturer_part_number }),
  })
  fixtures.push({
    fixture: fixturePath,
    native_sha256: createHash("sha256").update(nativeBytes).digest("hex"),
    rows: bomRows.map((row) => {
      const sourceComponent = nativeElements.find(
        (element) => element.type === "source_component" && element.name === row.designator,
      )
      return { ...row, native_manufacturer_part_number: sourceComponent?.manufacturer_part_number }
    }),
    resolver_comment_examples: resolvedCommentRows.filter((row) => ["U1", "U25", "SW4"].includes(row.designator)),
    blank_comment_count: bomRows.filter((row) => !row.comment.trim()).length,
    supplier_code_as_footprint_count: bomRows.filter((row) => /^C[0-9]+$/.test(row.footprint)).length,
  })
  if (fixturePath.includes("hold-control")) {
    await writeFile(new URL("../NOT-FOR-FABRICATION-bom-characterization.csv", import.meta.url), convertBomRowsToCsv(bomRows))
  }
}
const characterization = {
  scope: "Isolated official BOM converter characterization, not a fabrication package or full-board gate pass",
  converter_version: "circuit-json-to-bom-csv@0.0.19",
  native_cli_invocation: "convertCircuitJsonToBomRows({ circuitJson }) without resolvePart, CLI@0.1.2235 Gerber export source",
  schema_status: "Known B-010 errors in untouched native fixtures remain unresolved and independently recorded",
  fixtures,
}
await writeFile(new URL("../native-bom-characterization.json", import.meta.url), JSON.stringify(characterization, null, 2) + "\n")
console.log(JSON.stringify(fixtures.map(({fixture, blank_comment_count, supplier_code_as_footprint_count}) => ({fixture, blank_comment_count, supplier_code_as_footprint_count}))))
