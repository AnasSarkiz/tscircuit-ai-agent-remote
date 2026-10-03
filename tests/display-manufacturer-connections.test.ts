import { describe, expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import { any_circuit_element } from "circuit-json"
import { z } from "zod"

const rawElements = z
  .array(z.object({ type: z.string() }).passthrough())
  .parse(
    JSON.parse(
      readFileSync(
        new URL("../evidence/display-review-2026-10-03/circuit.json", import.meta.url),
        "utf8",
      ),
    ),
  )
const sourceElements = any_circuit_element
  .array()
  .parse(rawElements.filter((element) => element.type.startsWith("source_")))

// Manufacturer pin maps: TI TPS7A20 / SN74LVC245A; HS17QS178RX contact drawing.
// This reviews the partial logic fixture; it does not qualify the backlight or cable.
const expectPinNet = ({
  name,
  pinNumber,
  netName,
}: {
  name: string
  pinNumber: number
  netName: string
}) => {
  const sourceComponent = sourceElements.find(
    (element) => element.type === "source_component" && element.name === name,
  )
  if (!sourceComponent || sourceComponent.type !== "source_component") {
    throw new Error(`Missing display component ${name}`)
  }
  const sourcePort = sourceElements.find(
    (element) =>
      element.type === "source_port" &&
      element.source_component_id === sourceComponent.source_component_id &&
      element.pin_number === pinNumber,
  )
  const sourceNet = sourceElements.find(
    (element) => element.type === "source_net" && element.name === netName,
  )
  if (
    !sourcePort ||
    sourcePort.type !== "source_port" ||
    !sourceNet ||
    sourceNet.type !== "source_net"
  ) {
    throw new Error(`Missing ${name}.${pinNumber} or ${netName}`)
  }
  expect(
    sourceElements.some(
      (element) =>
        element.type === "source_trace" &&
        element.connected_source_port_ids.includes(sourcePort.source_port_id) &&
        element.connected_source_net_ids.includes(sourceNet.source_net_id),
    ),
  ).toBe(true)
}

describe("display manufacturer physical pin requirements", () => {
  test("LDO power/enable and buffer direction, output-enable and power use TI pin numbers", () => {
    for (const [name, pinNumber, netName] of [
      ["U13", 1, "V3V3"],
      ["U13", 2, "GND"],
      ["U13", 3, "LCD_ENABLE"],
      ["U13", 5, "VLCD"],
      ["U14", 1, "VLCD"],
      ["U14", 10, "GND"],
      ["U14", 19, "GND"],
      ["U14", 20, "VLCD"],
    ] as const)
      expectPinNet({ name, pinNumber, netName })
  })
  test("buffer channel B pins match the manufacturer's LCD contact order and polarity", () => {
    for (const [bufferPin, lcdPin, netName] of [
      [18, 5, "LCD_CS_N"],
      [17, 6, "LCD_RESET_N"],
      [16, 7, "LCD_DC"],
      [15, 8, "LCD_SCLK"],
      [14, 9, "LCD_SDA"],
    ] as const) {
      expectPinNet({ name: "U14", pinNumber: bufferPin, netName })
      expectPinNet({ name: "J7", pinNumber: lcdPin, netName })
    }
    for (const [pinNumber, netName] of [
      [1, "LCD_BACKLIGHT_RETURN"],
      [2, "LCD_BACKLIGHT_OUTPUT"],
      [3, "VLCD"],
      [10, "GND"],
      [11, "GND"],
      [12, "GND"],
    ] as const)
      expectPinNet({ name: "J7", pinNumber, netName })
  })
  test("unused buffer inputs are grounded and unused outputs, TE and LDO NC remain open", () => {
    for (const pinNumber of [7, 8, 9]) expectPinNet({ name: "U14", pinNumber, netName: "GND" })
    for (const [name, pinNumbers] of [
      ["U14", [11, 12, 13]],
      ["U13", [4]],
      ["J7", [4]],
    ] as const) {
      const sourceComponent = sourceElements.find(
        (element) => element.type === "source_component" && element.name === name,
      )
      if (!sourceComponent || sourceComponent.type !== "source_component") throw new Error(name)
      const unusedPorts = sourceElements.filter(
        (element) =>
          element.type === "source_port" &&
          element.source_component_id === sourceComponent.source_component_id &&
          pinNumbers.some((pinNumber) => pinNumber === element.pin_number),
      )
      expect(unusedPorts).toHaveLength(pinNumbers.length)
      for (const sourcePort of unusedPorts) {
        if (sourcePort.type !== "source_port") throw new Error("Unexpected port")
        expect(
          sourceElements.filter(
            (element) =>
              element.type === "source_trace" &&
              element.connected_source_port_ids.includes(sourcePort.source_port_id),
          ),
        ).toHaveLength(0)
      }
    }
  })
})
