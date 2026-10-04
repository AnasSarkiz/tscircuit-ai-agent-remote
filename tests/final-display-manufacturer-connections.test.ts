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

// Manufacturer pin maps: TI TPS7A20 / SN74LVC245A; BuyDisplay ER-TFT022-1 Rev2.0 pages 9-11 / ILI9341 unused pins.
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
      [18, 38, "LCD_CS_N"],
      [17, 10, "LCD_RESET_N"],
      [16, 36, "LCD_DC"],
      [15, 37, "LCD_SCLK"],
      [14, 34, "LCD_SDA"],
    ] as const) {
      expectPinNet({ name: "U14", pinNumber: bufferPin, netName })
      expectPinNet({ name: "J7", pinNumber: 51 - lcdPin, netName })
    }
    for (const [pinNumber, netName] of [
      [1, "LCD_BACKLIGHT_OUTPUT"],
      [2, "LCD_BACKLIGHT_RETURN_1"],
      [3, "LCD_BACKLIGHT_RETURN_2"],
      [4, "LCD_BACKLIGHT_RETURN_3"],
      [7, "VLCD"],
      [8, "VLCD"],
      [9, "VLCD"],
      [35, "VLCD"],
      [40, "VLCD"],
      [41, "VLCD"],
      [42, "VLCD"],
    ] as const)
      expectPinNet({ name: "J7", pinNumber: 51 - pinNumber, netName })
    for (const pinNumber of [
      6,
      ...Array.from({ length: 22 }, (_, index) => index + 11),
      43,
      48,
      49,
      50,
      51,
      52,
    ])
      expectPinNet({
        name: "J7",
        pinNumber: pinNumber <= 50 ? 51 - pinNumber : pinNumber,
        netName: "GND",
      })
  })
  test("genuine top-contact connector pin 50 is north for the single right-edge fold", () => {
    const connector = sourceElements.find(
      (element) => element.type === "source_component" && element.name === "J7",
    )
    if (!connector || connector.type !== "source_component") throw new Error("Missing J7")
    expect(connector.manufacturer_part_number).toBe("AFC07-S50ECA-00")
    expect(connector.supplier_part_numbers?.jlcpcb).toEqual(["C262650"])
    const terminalPositions = [1, 50].map((pinNumber) => {
      const sourcePort = sourceElements.find(
        (element) =>
          element.type === "source_port" &&
          element.source_component_id === connector.source_component_id &&
          element.pin_number === pinNumber,
      )
      if (!sourcePort || sourcePort.type !== "source_port") throw new Error("Missing terminal")
      const terminal = rawElements.find(
        (element) =>
          element.type === "pcb_port" && element.source_port_id === sourcePort.source_port_id,
      )
      const parsedTerminal = any_circuit_element.parse(terminal)
      if (parsedTerminal.type !== "pcb_port") throw new Error("Missing native pad")
      return parsedTerminal
    })
    expect(terminalPositions[1].y).toBeGreaterThan(terminalPositions[0].y)
    expect(Math.abs(terminalPositions[1].x - terminalPositions[0].x)).toBeLessThan(0.01)
    expect(terminalPositions[1].y - terminalPositions[0].y).toBeCloseTo(24.5, 2)
  })
  test("unused buffer inputs are grounded and unused outputs, display NC and LDO NC remain open", () => {
    for (const pinNumber of [7, 8, 9]) expectPinNet({ name: "U14", pinNumber, netName: "GND" })
    for (const [name, pinNumbers] of [
      ["U14", [11, 12, 13]],
      ["U13", [4]],
      ["J7", [46, 18, 12, 7, 6, 5, 4]],
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
