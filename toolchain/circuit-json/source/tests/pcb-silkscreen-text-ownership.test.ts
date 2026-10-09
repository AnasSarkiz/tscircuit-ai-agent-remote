import { expect, test } from "bun:test"
import { pcb_silkscreen_text } from "../src/pcb/pcb_silkscreen_text"

test("silkscreen supports board markings and preserves component ownership validation", () => {
  const marking = { type: "pcb_silkscreen_text", text: "M+", layer: "top" }
  expect(pcb_silkscreen_text.parse(marking).pcb_component_id).toBeUndefined()
  expect(pcb_silkscreen_text.parse({ ...marking, pcb_component_id: "pcb_component_1" }).pcb_component_id).toBe("pcb_component_1")
  expect(pcb_silkscreen_text.safeParse({ ...marking, pcb_component_id: null }).success).toBe(false)
  expect(pcb_silkscreen_text.safeParse({ ...marking, pcb_component_id: 3 }).success).toBe(false)
  expect(pcb_silkscreen_text.safeParse({ ...marking, layer: "invalid" }).success).toBe(false)
  expect(pcb_silkscreen_text.safeParse({ ...marking, text: 3 }).success).toBe(false)
})
