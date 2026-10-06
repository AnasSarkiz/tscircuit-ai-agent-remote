import assert from "node:assert/strict"
import { readFileSync, writeFileSync } from "node:fs"
import { createHash } from "node:crypto"
import { any_circuit_element } from "circuit-json"
import { componentExplanations, guideSheets } from "../../src/board/ComponentNotes"

const directory = "evidence/schematic-component-notes-2026-10-06"
const nativePath = process.argv[2] ?? `${directory}/native/circuit.json`
const nativeBytes = readFileSync(nativePath)
const circuitJson = JSON.parse(nativeBytes)
const previous = JSON.parse(
  readFileSync("evidence/board-corrections-2026-10-06/final-native/circuit.json", "utf8"),
)
const unchangedTypes = [...new Set(previous.map((element) => element.type))].filter(
  (type) =>
    (type.startsWith("pcb_") || type.startsWith("source_") || type === "cad_component") &&
    type !== "source_missing_manufacturer_part_number_warning" &&
    type !== "source_project_metadata",
)
const unchangedRecords = unchangedTypes.map((type) => {
  const before = previous.filter((element) => element.type === type)
  const after = circuitJson.filter((element) => element.type === type)
  if (type === "source_component") {
    assert.equal(after.length, before.length)
    const emptySupplierMaps = []
    for (const [index, component] of after.entries()) {
      const previousComponent = before[index]
      if (previousComponent.supplier_part_numbers === undefined &&
          JSON.stringify(component.supplier_part_numbers) === "{}") {
        assert(component.name.startsWith("TP"), "Empty map changed a purchased component")
        const { supplier_part_numbers, ...remainingFields } = component
        assert.deepEqual(remainingFields, previousComponent)
        emptySupplierMaps.push(component.name)
      } else assert.deepEqual(component, previousComponent)
    }
    return { type, records: after.length, exact_equal: emptySupplierMaps.length === 0,
      supported_cli_empty_supplier_maps_only: emptySupplierMaps }
  }
  assert.deepEqual(after, before, `Annotation changed ${type}`)
  return { type, records: after.length, exact_equal: true }
})
const projectMetadata = circuitJson.filter((element) => element.type === "source_project_metadata")
assert.equal(projectMetadata.length, 1)
if (projectMetadata[0].source_filesystem_md5_hash !== undefined) {
  assert.match(projectMetadata[0].source_filesystem_md5_hash, /^[0-9a-f]{32}$/)
  assert.deepEqual(Object.keys(projectMetadata[0]).sort(), ["source_filesystem_md5_hash", "type"])
} else assert.deepEqual(projectMetadata, previous.filter((element) => element.type === "source_project_metadata"))
const missingPartWarnings = circuitJson.filter(
  (element) => element.type === "source_missing_manufacturer_part_number_warning",
)
const previousMissingPartWarnings = previous.filter(
  (element) => element.type === "source_missing_manufacturer_part_number_warning",
)
assert.equal(missingPartWarnings.length, previousMissingPartWarnings.length)
for (const [index, warning] of missingPartWarnings.entries()) {
  const { message, ...warningFields } = warning
  const { message: previousMessage, ...previousWarningFields } = previousMissingPartWarnings[index]
  assert.deepEqual(warningFields, previousWarningFields)
  // New annotation primitives change only diagnostic component-instance serials.
  assert.equal(message.replace(/#\d+(?=\()/g, "#instance"), previousMessage.replace(/#\d+(?=\()/g, "#instance"))
}
const sources = circuitJson.filter((element) => element.type === "source_component")
const coveredReferences = []
const guides = guideSheets.map((guide) => {
  const diagram = circuitJson.find(
    (element) => element.type === "schematic_sheet" && element.name === guide.name,
  )
  const sheet = circuitJson.find(
    (element) =>
      element.type === "schematic_sheet" && element.name === `component-guide-${guide.name}`,
  )
  assert(diagram && sheet, `Missing paired sheet for ${guide.name}`)
  assert.equal(sheet.sheet_size, "a4")
  assert.equal(sheet.sheet_index, guide.guideIndex)
  const actualReferences = circuitJson
    .filter(
      (element) =>
        element.type === "schematic_component" &&
        element.schematic_sheet_id === diagram.schematic_sheet_id,
    )
    .map((component) => {
      const source = sources.find(
        (element) => element.source_component_id === component.source_component_id,
      )
      assert(source, "Schematic component without source")
      return source.name
    })
    .sort()
  const expectedReferences = componentExplanations[guide.name].map(([reference]) => reference).sort()
  assert.deepEqual(expectedReferences, actualReferences, `Incomplete guide ${guide.name}`)
  const annotations = circuitJson.filter(
    (element) => element.schematic_sheet_id === sheet.schematic_sheet_id,
  )
  any_circuit_element.array().parse(annotations)
  for (const [reference, explanation] of componentExplanations[guide.name]) {
    const texts = annotations.filter(
      (element) => element.type === "schematic_text" && element.text === `${reference}: ${explanation}`,
    )
    assert.equal(texts.length, 1, `Missing or duplicate explanation ${reference}`)
    assert.equal(texts[0].font_size, 0.45)
    assert(texts[0].position.y > -10 && texts[0].position.y < 10)
    coveredReferences.push(reference)
  }
  const link = circuitJson.find(
    (element) =>
      element.type === "schematic_text" &&
      element.schematic_sheet_id === diagram.schematic_sheet_id &&
      element.text === `Component explanations: schematic sheet ${guide.guideIndex}.`,
  )
  assert(link, `Missing diagram cross-reference ${guide.name}`)
  return { diagram: guide.name, guide_index: guide.guideIndex, references: actualReferences }
})
assert.equal(new Set(coveredReferences).size, coveredReferences.length)
assert.deepEqual(coveredReferences.slice().sort(), sources.map((source) => source.name).sort())
assert.equal(coveredReferences.length, 135)
assert.equal(circuitJson.filter((element) => element.type === "schematic_sheet").length, 26)
const record = {
  native_path: nativePath,
  native_sha256: createHash("sha256").update(nativeBytes).digest("hex"),
  diagram_sheets: 13,
  guide_sheets: 13,
  component_explanations: coveredReferences.length,
  missing_or_duplicate_references: [],
  native_annotation_schema_passed: true,
  actual_project_metadata: projectMetadata,
  cli_metadata_differences_are_not_electrical_or_physical_changes: true,
  retained_native_pad_manufacturer_warnings: missingPartWarnings.length,
  warning_message_changes_only_internal_instance_serials: true,
  unchanged_electrical_and_physical_records: unchangedRecords,
  native_open_port_errors: circuitJson.filter((element) => element.type === "pcb_port_not_connected_error")
    .length,
  guides,
  whole_board_fabrication_pass_inferred: false,
}
writeFileSync(`${directory}/annotation-audit.json`, `${JSON.stringify(record, null, 2)}\n`)
console.log(JSON.stringify({ component_explanations: 135, paired_guides: 13, pcb_and_nets_unchanged: true }))
