import { describe, expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import { z } from "zod"

// Compare untouched native outputs. Full strict schema failures remain separate gates.
const nativeElements = z.array(z.object({ type: z.string() }).passthrough())
const canonical = nativeElements.parse(
  JSON.parse(readFileSync(new URL("../dist/index/circuit.json", import.meta.url), "utf8")),
)
const placement = nativeElements.parse(
  JSON.parse(
    readFileSync(
      new URL("../evidence/a4-placement-gate-2026-10-04/placement-circuit.json", import.meta.url),
      "utf8",
    ),
  ),
)
const before = nativeElements.parse(
  JSON.parse(
    readFileSync(
      new URL("../evidence/a4-placement-gate-2026-10-04/before-circuit.json", import.meta.url),
      "utf8",
    ),
  ),
)

describe("Native placement review preserves the board", () => {
  test("the inspection output has no copper routes, vias or pours", () => {
    expect(
      placement.filter((element) =>
        ["pcb_trace", "pcb_via", "pcb_copper_pour"].includes(element.type),
      ),
    ).toEqual([])
  })

  test("all electrical connections and physical placement features match the canonical board", () => {
    for (const type of [
      "source_component",
      "source_port",
      "source_net",
      "source_trace",
      "pcb_component",
      "pcb_smtpad",
      "pcb_plated_hole",
      "pcb_hole",
      "pcb_keepout",
      "pcb_port",
    ]) {
      expect(placement.filter((element) => element.type === type)).toEqual(
        canonical.filter((element) => element.type === type),
      )
    }
  })

  test("the canonical four native traces remain exactly unchanged from the reviewed A4", () => {
    const canonicalCopper = canonical.filter((element) =>
      ["pcb_trace", "pcb_via"].includes(element.type),
    )
    expect(canonicalCopper).toHaveLength(4)
    expect(canonicalCopper).toEqual(
      before.filter((element) => ["pcb_trace", "pcb_via"].includes(element.type)),
    )
  })
})
