import { expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import { any_circuit_element } from "circuit-json"
import { z } from "zod"

const nativeElements = z
  .array(z.object({ type: z.string() }).passthrough())
  .parse(JSON.parse(readFileSync(new URL("../dist/index/circuit.json", import.meta.url), "utf8")))
const sourceElements = any_circuit_element
  .array()
  .parse(nativeElements.filter((element) => element.type.startsWith("source_")))
type SourceNetId = Extract<(typeof sourceElements)[number], { type: "source_net" }>["source_net_id"]

test("the genuine JST SH connector matches the standard UART target without power or reset contacts", () => {
  const connector = sourceElements.find(
    (element) => element.type === "source_component" && element.name === "J6",
  )
  if (!connector || connector.type !== "source_component") throw new Error("Missing J6")
  expect(connector.manufacturer_part_number).toBe("BM03B-SRSS-TB(LF)(SN)")
  expect(connector.supplier_part_numbers?.jlcpcb).toEqual(["C160389"])

  const ports = sourceElements.filter(
    (element) =>
      element.type === "source_port" &&
      element.source_component_id === connector.source_component_id,
  )
  expect(ports.map((port) => port.type === "source_port" && port.pin_number).sort()).toEqual([
    1, 2, 3, 4, 5,
  ])
  const nets = new Map<SourceNetId, string>(
    sourceElements
      .filter((element) => element.type === "source_net")
      .map((element) => [element.source_net_id, element.name]),
  )
  // Pin numbers refer to the manufacturer's mounting-face drawing. Pins 4/5
  // are hold-downs. The public programmer v0.8.0 is TX/GND/RX at its cable end.
  for (const [pinNumber, netName] of [
    [1, "MCU_UART_RX"],
    [2, "GND"],
    [3, "SERVICE_UART_TX"],
    [4, "GND"],
    [5, "GND"],
  ] as const) {
    const port = ports.find(
      (element) => element.type === "source_port" && element.pin_number === pinNumber,
    )
    if (!port || port.type !== "source_port") throw new Error(`Missing J6.${pinNumber}`)
    const connectedNets = new Set(
      sourceElements.flatMap((element) =>
        element.type === "source_trace" &&
        element.connected_source_port_ids.includes(port.source_port_id)
          ? element.connected_source_net_ids.map((identifier) => nets.get(identifier))
          : [],
      ),
    )
    expect([...connectedNets]).toEqual([netName])
  }
})
