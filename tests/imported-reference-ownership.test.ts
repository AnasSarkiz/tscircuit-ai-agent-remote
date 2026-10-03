import { describe, expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import { any_circuit_element } from "circuit-json"
import { z } from "zod"

const fixtures = [
  { name: "comparator", references: ["U7"] },
  { name: "usb", references: ["D2"] },
  { name: "amplifier", references: ["Q1", "Q2"] },
]

describe("native imported reference labels belong to the correct component", () => {
  for (const fixture of fixtures) {
    test(fixture.name, () => {
      const nativeElements = z
        .array(z.object({ type: z.string() }).passthrough())
        .parse(
          JSON.parse(
            readFileSync(
              new URL(
                `../evidence/blocker-recheck-2026-10-03-1357/${fixture.name}/native-output/circuit.json`,
                import.meta.url,
              ),
              "utf8",
            ),
          ),
        )
      const relevantElements = any_circuit_element
        .array()
        .parse(
          nativeElements.filter((element) =>
            ["source_component", "schematic_component", "schematic_text"].includes(element.type),
          ),
        )
      for (const reference of fixture.references) {
        const component = relevantElements.find(
          (element) => element.type === "source_component" && element.name === reference,
        )
        if (!component || component.type !== "source_component") throw new Error(reference)
        const schematic = relevantElements.find(
          (element) =>
            element.type === "schematic_component" &&
            element.source_component_id === component.source_component_id,
        )
        if (!schematic || schematic.type !== "schematic_component") throw new Error(reference)
        expect(
          relevantElements.filter(
            (element) =>
              element.type === "schematic_text" &&
              element.text === reference &&
              element.schematic_component_id === schematic.schematic_component_id,
          ),
        ).toHaveLength(1)
      }
      expect(
        nativeElements.filter(
          (element) => element.styling_issue_type === "missing_reference_designator_text",
        ),
      ).toHaveLength(0)
    })
  }
})
