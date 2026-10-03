import { describe, expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import { any_circuit_element } from "circuit-json"
import { z } from "zod"

const rawElements = z
  .array(z.object({ type: z.string() }).passthrough())
  .parse(
    JSON.parse(
      readFileSync(
        new URL("../evidence/type-c-current-review-2026-10-03/circuit.json", import.meta.url),
        "utf8",
      ),
    ),
  )
const sourceElements = any_circuit_element
  .array()
  .parse(rawElements.filter((element) => element.type.startsWith("source_")))

// TI TUSB320LAI Rev D, TPS3839 Rev G, TPS7A20 and SN74LVC1G08 physical pin drawings.
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
    throw new Error(`Missing Type-C component ${name}`)
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

describe("Type-C controller manufacturer requirements", () => {
  test("UFP strap, GPIO mode and local supply prevent conflicting Rd and rail backpower", () => {
    for (const [name, pinNumber, netName] of [
      ["U15", 1, "VSYS"],
      ["U15", 2, "GND"],
      ["U15", 3, "VSYS"],
      ["U15", 5, "USB_CTRL_V3V3"],
      ["U18", 1, "USB_CC1"],
      ["U18", 2, "USB_CC2"],
      ["U18", 3, "GND"],
      ["U18", 4, "VBUS_DETECT"],
      ["U18", 7, "USB_HIGH_CURRENT_N"],
      ["U18", 8, "USB_CURRENT_OUT2"],
      ["U18", 10, "GND"],
      ["U18", 11, "GND"],
      ["U18", 12, "USB_CTRL_V3V3"],
      ["R74", 1, "USB_CTRL_V3V3"],
      ["R74", 2, "USB_HIGH_CURRENT_N"],
      ["R75", 1, "USB_CTRL_V3V3"],
      ["R75", 2, "USB_CURRENT_OUT2"],
    ] as const)
      expectPinNet({ name, pinNumber, netName })
    const controller = sourceElements.find((e) => e.type === "source_component" && e.name === "U18")
    if (!controller || controller.type !== "source_component") throw new Error("U18")
    for (const pinNumber of [5, 6, 9]) {
      const port = sourceElements.find(
        (e) =>
          e.type === "source_port" &&
          e.source_component_id === controller.source_component_id &&
          e.pin_number === pinNumber,
      )
      if (!port || port.type !== "source_port") throw new Error(`U18.${pinNumber}`)
      expect(
        sourceElements.filter(
          (e) =>
            e.type === "source_trace" && e.connected_source_port_ids.includes(port.source_port_id),
        ),
      ).toHaveLength(0)
    }
    for (const netName of ["USB_CC1", "USB_CC2"]) {
      const net = sourceElements.find((e) => e.type === "source_net" && e.name === netName)
      if (!net || net.type !== "source_net") throw new Error(netName)
      expect(
        sourceElements.filter(
          (e) =>
            e.type === "source_trace" && e.connected_source_net_ids.includes(net.source_net_id),
        ),
      ).toHaveLength(1)
    }
  })
  test("higher current requires stable controller power and advertised 1.5A or 3A", () => {
    for (const [name, pinNumber, netName] of [
      ["U19", 1, "GND"],
      ["U19", 2, "USB_CTRL_READY"],
      ["U19", 3, "USB_CTRL_V3V3"],
      ["U20", 2, "USB_HIGH_CURRENT_N"],
      ["U20", 3, "GND"],
      ["U20", 4, "USB_HIGH_CURRENT_DETECTED"],
      ["U20", 5, "USB_CTRL_V3V3"],
      ["U21", 1, "USB_CTRL_READY"],
      ["U21", 2, "USB_HIGH_CURRENT_DETECTED"],
      ["U21", 3, "GND"],
      ["U21", 4, "USB_CHARGER_EN2"],
      ["U21", 5, "USB_CTRL_V3V3"],
      ["R76", 1, "USB_CHARGER_EN2"],
      ["R76", 2, "GND"],
    ] as const)
      expectPinNet({ name, pinNumber, netName })
    // TI gate Ioff maximum 10uA; +/-1.6% provisional pull-down tolerance.
    expect(10e-6 * resistanceOhms("R76") * 1.016).toBeLessThan(0.4)
    // TI gate VOH >=2.4V at 3V, -24mA; BQ24074 VIH >=1.4V, 1k pull-down is <24mA.
    expect((3.3 * 1.015) / (resistanceOhms("R76") * 0.984)).toBeLessThan(0.024)
  })
  test("VBUS detection resistors meet TI's 855k–920k allowed range", () => {
    for (const [name, pinNumber, netName] of [
      ["R71", 1, "VBUS"],
      ["R71", 2, "VBUS_DETECT_MID"],
      ["R72", 1, "VBUS_DETECT_MID"],
      ["R72", 2, "VBUS_DETECT"],
      ["R73", 1, "USB_CTRL_V3V3"],
      ["R73", 2, "GND"],
    ] as const)
      expectPinNet({ name, pinNumber, netName })
    const total = resistanceOhms("R71") + resistanceOhms("R72")
    expect(total * 0.984).toBeGreaterThanOrEqual(855000)
    expect(total * 1.016).toBeLessThanOrEqual(920000)
    // Dedicated LDO minimum load >1mA at its +/-1.5% 3.3V corner.
    expect((3.3 * 0.985) / (resistanceOhms("R73") * 1.016)).toBeGreaterThan(0.001)
    expect(
      rawElements.filter(
        (e) => e.type === "pcb_trace" || e.type === "pcb_via" || e.type.endsWith("_error"),
      ),
    ).toHaveLength(0)
  })
})
function resistanceOhms(name: string) {
  const resistor = sourceElements.find((e) => e.type === "source_component" && e.name === name)
  if (
    !resistor ||
    resistor.type !== "source_component" ||
    !("resistance" in resistor) ||
    typeof resistor.resistance !== "number"
  )
    throw new Error(name)
  return resistor.resistance
}
