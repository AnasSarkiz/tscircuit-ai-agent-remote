import { expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import { any_circuit_element } from "circuit-json"
import { z } from "zod"

// Preserve the full native JSON and its separate schema failures. This checks
// manufacturer source connections without claiming full JSON qualification.
const elements = any_circuit_element.array().parse(
  z
    .array(z.object({ type: z.string() }).passthrough())
    .parse(
      JSON.parse(
        readFileSync(
          new URL(
            "../evidence/charger-battery-ready-review-2026-10-03/circuit.json",
            import.meta.url,
          ),
          "utf8",
        ),
      ),
    )
    .filter((element) => element.type.startsWith("source_")),
)

test("battery supervisor senses charger BAT and cannot be overridden by the MCU", () => {
  const component = elements.find(
    (element) => element.type === "source_component" && element.name === "U25",
  )
  if (!component || component.type !== "source_component") throw new Error("Missing supervisor")
  expect(component.supplier_part_numbers?.jlcpcb).toEqual(["C43698"])
  expect(component.manufacturer_part_number).toBe("TPS3808G33DBVR")
  for (const [pin, name] of [
    [1, "BUCK_ENABLE"],
    [2, "GND"],
    [3, "VSYS"],
    [5, "PACK_BAT"],
    [6, "VSYS"],
  ] as const) {
    const port = elements.find(
      (element) =>
        element.type === "source_port" &&
        element.source_component_id === component.source_component_id &&
        element.pin_number === pin,
    )
    const net = elements.find((element) => element.type === "source_net" && element.name === name)
    if (!port || port.type !== "source_port" || !net || net.type !== "source_net")
      throw new Error(`Missing pin${pin} or${name}`)
    expect(
      elements.some(
        (element) =>
          element.type === "source_trace" &&
          element.connected_source_port_ids.includes(port.source_port_id) &&
          element.connected_source_net_ids.includes(net.source_net_id),
      ),
    ).toBe(true)
  }
  const ct = elements.find(
    (element) =>
      element.type === "source_port" &&
      element.source_component_id === component.source_component_id &&
      element.pin_number === 4,
  )
  if (!ct || ct.type !== "source_port") throw new Error("Missing CT")
  expect(
    elements.some(
      (element) =>
        element.type === "source_trace" &&
        element.connected_source_port_ids.includes(ct.source_port_id),
    ),
  ).toBe(false)
  const enable = elements.find(
    (element) => element.type === "source_net" && element.name === "BUCK_ENABLE",
  )
  if (!enable || enable.type !== "source_net") throw new Error("Missing enable")
  const ids = elements.flatMap((element) =>
    element.type === "source_trace" &&
    element.connected_source_net_ids.includes(enable.source_net_id)
      ? element.connected_source_port_ids
      : [],
  )
  const components = elements.flatMap((element) =>
    element.type === "source_port" && ids.includes(element.source_port_id)
      ? [element.source_component_id]
      : [],
  )
  const names = elements.flatMap((element) =>
    element.type === "source_component" && components.includes(element.source_component_id)
      ? [element.name]
      : [],
  )
  expect(names.sort()).toEqual(["C77", "R96", "R97", "U25"])
})
