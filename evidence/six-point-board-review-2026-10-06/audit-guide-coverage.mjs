import assert from "node:assert/strict"
import { readFileSync, writeFileSync } from "node:fs"
import { createHash } from "node:crypto"
import { any_circuit_element } from "circuit-json"
import { componentExplanations, guideSheets } from "../../src/board/ComponentNotes"
const nativePath = "evidence/six-point-board-review-2026-10-06/final-native/circuit.json"
const nativeBytes = readFileSync(nativePath)
const circuitJson = JSON.parse(nativeBytes)
// The original annotation-only audit retains its unchanged-PCB assertions.
// This audit reuses its complete guide/schema/coverage assertions for the
// explicitly changed board; independent whole-PCB checks run separately.
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
const record = { native_sha256: createHash("sha256").update(nativeBytes).digest("hex"), annotation_schema_passed: true, component_coverage: coveredReferences.length, guides, physical_geometry_gate: "separate final-native-compliance.json and final-copper-audit.json", fabrication_ready: false }
writeFileSync("evidence/six-point-board-review-2026-10-06/final-guide-coverage.json", JSON.stringify(record, null, 2) + "\n")
console.log(JSON.stringify({ component_coverage: coveredReferences.length, annotation_schema_passed: true, guide_sheets: guides.length }))
