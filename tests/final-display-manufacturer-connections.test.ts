import { describe, expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import { any_circuit_element } from "circuit-json"
import { z } from "zod"

const rawElements = z
  .array(z.object({ type: z.string() }).passthrough())
  .parse(JSON.parse(readFileSync(new URL("../dist/index/circuit.json", import.meta.url), "utf8")))
const sourceElements = any_circuit_element
  .array()
  .parse(rawElements.filter((element) => element.type.startsWith("source_")))

// Manufacturer pin maps: TI TPS7A20 / SN74LVC245A; HS20HS072RX C5329582 drawing/page 11.
// This checks the native full-board source connections; mechanical flex fit remains open.
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
      [18, 2, "LCD_CS_N"],
      [17, 6, "LCD_RESET_N"],
      [16, 3, "LCD_DC"],
      [15, 4, "LCD_SCLK"],
      [14, 5, "LCD_SDA"],
    ] as const) {
      expectPinNet({ name: "U14", pinNumber: bufferPin, netName })
      expectPinNet({ name: "J7", pinNumber: lcdPin, netName })
    }
    for (const [pinNumber, netName] of [
      [1, "GND"],
      [8, "VLCD"],
      [9, "VLCD"],
      [10, "LCD_BACKLIGHT_OUTPUT"],
      [11, "LCD_BACKLIGHT_RETURN"],
      [12, "GND"],
      [13, "GND"],
      [14, "GND"],
    ] as const)
      expectPinNet({ name: "J7", pinNumber, netName })
  })
  test("unused buffer inputs are grounded and unused outputs, display NC and LDO NC remain open", () => {
    for (const pinNumber of [7, 8, 9]) expectPinNet({ name: "U14", pinNumber, netName: "GND" })
    for (const [name, pinNumbers] of [
      ["U14", [11, 12, 13]],
      ["U13", [4]],
      ["J7", [7]],
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
