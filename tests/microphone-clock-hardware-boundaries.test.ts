import { describe, expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import { any_circuit_element } from "circuit-json"
import { z } from "zod"

const rawElements = z
  .array(z.object({ type: z.string() }).passthrough())
  .parse(
    JSON.parse(
      readFileSync(
        new URL(
          "../evidence/microphone-open-drain-review-2026-10-03/circuit.json",
          import.meta.url,
        ),
        "utf8",
      ),
    ),
  )
const sourceElements = any_circuit_element
  .array()
  .parse(rawElements.filter((element) => element.type.startsWith("source_")))

const expectPinNet = ({
  name,
  pinNumber,
  netName,
}: {
  name: string
  pinNumber: number
  netName: string
}) => {
  const component = sourceElements.find(
    (element) => element.type === "source_component" && element.name === name,
  )
  if (!component || component.type !== "source_component") throw new Error(name)
  const port = sourceElements.find(
    (element) =>
      element.type === "source_port" &&
      element.source_component_id === component.source_component_id &&
      element.pin_number === pinNumber,
  )
  const net = sourceElements.find(
    (element) => element.type === "source_net" && element.name === netName,
  )
  if (!port || port.type !== "source_port" || !net || net.type !== "source_net") {
    throw new Error(`Missing ${name}.${pinNumber} or ${netName}`)
  }
  expect(
    sourceElements.some(
      (element) =>
        element.type === "source_trace" &&
        element.connected_source_port_ids.includes(port.source_port_id) &&
        element.connected_source_net_ids.includes(net.source_net_id),
    ),
  ).toBe(true)
}

describe("microphone clock hardware boundaries", () => {
  test("TI regulator enable belongs only to the hardware hold net", () => {
    for (const [pinNumber, netName] of [
      [1, "V3V3"],
      [2, "GND"],
      [3, "HOLD_HARDWARE"],
      [5, "VMIC"],
    ] as const)
      expectPinNet({ name: "U23", pinNumber, netName })
    const holdNet = sourceElements.find(
      (element) => element.type === "source_net" && element.name === "HOLD_HARDWARE",
    )
    if (!holdNet || holdNet.type !== "source_net") throw new Error("Missing hardware hold net")
    const holdTraces = sourceElements.filter(
      (element) =>
        element.type === "source_trace" &&
        element.connected_source_net_ids.includes(holdNet.source_net_id),
    )
    const holdPortIds = holdTraces.flatMap((element) =>
      element.type === "source_trace" ? element.connected_source_port_ids : [],
    )
    const holdPorts = sourceElements.filter(
      (element) => element.type === "source_port" && holdPortIds.includes(element.source_port_id),
    )
    const holdComponentIds = holdPorts.flatMap((element) =>
      element.type === "source_port" ? [element.source_component_id] : [],
    )
    const holdComponentNames = sourceElements.flatMap((element) =>
      element.type === "source_component" && holdComponentIds.includes(element.source_component_id)
        ? [element.name]
        : [],
    )
    expect(holdComponentNames.sort()).toEqual(["R87", "U23"])
    expectPinNet({ name: "R87", pinNumber: 1, netName: "HOLD_HARDWARE" })
    expectPinNet({ name: "R87", pinNumber: 2, netName: "GND" })
  })
  test("Nexperia open-drain clocks obtain both high levels only from VMIC", () => {
    const buffer = sourceElements.find(
      (element) => element.type === "source_component" && element.name === "U24",
    )
    if (!buffer || buffer.type !== "source_component") throw new Error("Missing clock buffer")
    expect(buffer.manufacturer_part_number).toBe("74LVC2G07GW,125")
    expect(buffer.supplier_part_numbers?.jlcpcb).toEqual(["C24478"])
    for (const [pinNumber, netName] of [
      [1, "MIC_BCLK_INPUT"],
      [2, "GND"],
      [3, "MIC_WS_INPUT"],
      [4, "MIC_WS"],
      [5, "VMIC"],
      [6, "MIC_BCLK"],
    ] as const)
      expectPinNet({ name: "U24", pinNumber, netName })
    for (const [name, clockNet] of [
      ["R92", "MIC_BCLK"],
      ["R93", "MIC_WS"],
    ] as const) {
      expectPinNet({ name, pinNumber: 1, netName: "VMIC" })
      expectPinNet({ name, pinNumber: 2, netName: clockNet })
      const pullup = sourceElements.find(
        (element) => element.type === "source_component" && element.name === name,
      )
      if (!pullup || pullup.type !== "source_component" || pullup.ftype !== "simple_resistor")
        throw new Error("Missing clock pullup")
      expect(pullup.resistance).toBe(330)
      expect(pullup.supplier_part_numbers?.jlcpcb).toEqual(["C105881"])
    }
    for (const [name, inputNet, clockNet] of [
      ["R88", "MCU_MIC_BCLK", "MIC_BCLK_INPUT"],
      ["R89", "MCU_MIC_WS", "MIC_WS_INPUT"],
    ] as const) {
      expectPinNet({ name, pinNumber: 1, netName: inputNet })
      expectPinNet({ name, pinNumber: 2, netName: clockNet })
    }
  })
})
