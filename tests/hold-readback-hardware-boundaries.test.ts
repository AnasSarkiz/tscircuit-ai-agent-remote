import { expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import { any_circuit_element } from "circuit-json"
import { z } from "zod"

// The complete native output and its strict schema failures remain separate evidence.
// These tests verify source connectivity, not dynamic privacy or fabrication readiness.
const elements = any_circuit_element.array().parse(
  z
    .array(z.object({ type: z.string() }).passthrough())
    .parse(
      JSON.parse(
        readFileSync(
          new URL("../evidence/hold-readback-review-2026-10-03/circuit.json", import.meta.url),
          "utf8",
        ),
      ),
    )
    .filter((element) => element.type.startsWith("source_")),
)

function getPinNets({ name, pinNumber }: { name: string; pinNumber: number }) {
  const component = elements.find(
    (element) => element.type === "source_component" && element.name === name,
  )
  if (!component || component.type !== "source_component") throw new Error(name)
  const port = elements.find(
    (element) =>
      element.type === "source_port" &&
      element.source_component_id === component.source_component_id &&
      element.pin_number === pinNumber,
  )
  if (!port || port.type !== "source_port") throw new Error(`${name}.pin${pinNumber}`)
  const netIds = elements.flatMap((element) =>
    element.type === "source_trace" &&
    element.connected_source_port_ids.includes(port.source_port_id)
      ? element.connected_source_net_ids
      : [],
  )
  return elements
    .flatMap((element) =>
      element.type === "source_net" && netIds.includes(element.source_net_id) ? [element.name] : [],
    )
    .sort()
}

test("MCU hold readback reaches the buffer output, without a direct hardware-enable connection", () => {
  const buffer = elements.find(
    (element) => element.type === "source_component" && element.name === "U26",
  )
  if (!buffer || buffer.type !== "source_component") throw new Error("Missing Schmitt buffer")
  expect(buffer.manufacturer_part_number).toBe("SN74LVC1G17DBVR")
  expect(buffer.supplier_part_numbers?.jlcpcb).toEqual(["C7836"])
  for (const [pinNumber, netName] of [
    [2, "HOLD_HARDWARE"],
    [3, "GND"],
    [4, "HOLD_BUFFER_OUT"],
    [5, "V3V3"],
  ] as const)
    expect(getPinNets({ name: "U26", pinNumber })).toEqual([netName])
  expect(getPinNets({ name: "U26", pinNumber: 1 })).toEqual([])
  expect(getPinNets({ name: "R100", pinNumber: 1 })).toEqual(["HOLD_BUFFER_OUT"])
  expect(getPinNets({ name: "R100", pinNumber: 2 })).toEqual(["MCU_HOLD_READ"])
  expect(getPinNets({ name: "R99", pinNumber: 1 })).toEqual(["HOLD_HARDWARE"])
  expect(getPinNets({ name: "R99", pinNumber: 2 })).toEqual(["GND"])
  for (const [name, resistance, lcsc] of [
    ["R99", 10000, "C98220"],
    ["R100", 1000, "C21190"],
  ] as const) {
    const resistor = elements.find(
      (element) => element.type === "source_component" && element.name === name,
    )
    if (!resistor || resistor.type !== "source_component" || resistor.ftype !== "simple_resistor")
      throw new Error(`Missing ${name}`)
    expect(resistor.resistance).toBe(resistance)
    expect(resistor.supplier_part_numbers?.jlcpcb).toEqual([lcsc])
  }
})
