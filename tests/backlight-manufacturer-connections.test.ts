import { expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import { any_circuit_element } from "circuit-json"
import { z } from "zod"

const rawElements = z
  .array(z.object({ type: z.string() }).passthrough())
  .parse(JSON.parse(readFileSync(new URL("../dist/index/circuit.json", import.meta.url), "utf8")))
const sourceElements = any_circuit_element
  .array()
  .parse(rawElements.filter((element) => element.type.startsWith("source_")))

test("TPS60231 current driver uses TI physical pins, three independent LED returns and same-rail enables", () => {
  const component = sourceElements.find(
    (element) => element.type === "source_component" && element.name === "U27",
  )
  if (!component || component.type !== "source_component")
    throw new Error("Missing genuine TPS60231")
  expect(component.manufacturer_part_number).toBe("TPS60231RGTR")
  for (const [pinNumber, netName] of [
    [4, "LCD_BACKLIGHT_RETURN_3"],
    [5, "LCD_BACKLIGHT_RETURN_2"],
    [6, "LCD_BACKLIGHT_RETURN_1"],
    [7, "GND"],
    [8, "LCD_BACKLIGHT_OUTPUT"],
    [13, "V3V3"],
    [14, "GND"],
    [15, "BACKLIGHT_GATE"],
    [16, "BACKLIGHT_GATE"],
    [17, "GND"],
  ] as const) {
    const port = sourceElements.find(
      (element) =>
        element.type === "source_port" &&
        element.source_component_id === component.source_component_id &&
        element.pin_number === pinNumber,
    )
    const net = sourceElements.find(
      (element) => element.type === "source_net" && element.name === netName,
    )
    if (!port || port.type !== "source_port" || !net || net.type !== "source_net")
      throw new Error(`Missing driver pin${pinNumber}/${netName}`)
    expect(
      sourceElements.some(
        (element) =>
          element.type === "source_trace" &&
          element.connected_source_port_ids.includes(port.source_port_id) &&
          element.connected_source_net_ids.includes(net.source_net_id),
      ),
    ).toBe(true)
  }
  for (const pinNumber of [2, 3]) {
    const port = sourceElements.find(
      (element) =>
        element.type === "source_port" &&
        element.source_component_id === component.source_component_id &&
        element.pin_number === pinNumber,
    )
    if (!port || port.type !== "source_port") throw new Error("Missing NC")
    expect(
      sourceElements.filter(
        (element) =>
          element.type === "source_trace" &&
          element.connected_source_port_ids.includes(port.source_port_id),
      ),
    ).toHaveLength(0)
  }
})
