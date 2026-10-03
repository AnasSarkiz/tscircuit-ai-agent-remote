import { describe, expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import { any_circuit_element } from "circuit-json"
import { z } from "zod"

const rawElements = z
  .array(z.object({ type: z.string() }).passthrough())
  .parse(
    JSON.parse(
      readFileSync(
        new URL("../evidence/haptic-review-2026-10-03/driver-circuit.json", import.meta.url),
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

describe("haptic application manufacturer requirements", () => {
  test("TI SOT-23 supply, ground, enable and output retain their physical pin numbers", () => {
    for (const [pinNumber, netName] of [
      [1, "VSYS"],
      [2, "GND"],
      [3, "MCU_HAPTIC_ENABLE"],
      [5, "VMOTOR"],
    ] as const)
      expectPinNet({ name: "U22", pinNumber, netName })
    const regulator = sourceElements.find(
      (element) => element.type === "source_component" && element.name === "U22",
    )
    if (!regulator || regulator.type !== "source_component") throw new Error("Missing regulator")
    const ncPort = sourceElements.find(
      (element) =>
        element.type === "source_port" &&
        element.source_component_id === regulator.source_component_id &&
        element.pin_number === 4,
    )
    if (!ncPort || ncPort.type !== "source_port") throw new Error("Missing regulator NC pin")
    expect(
      sourceElements.some(
        (element) =>
          element.type === "source_trace" &&
          element.connected_source_port_ids.includes(ncPort.source_port_id),
      ),
    ).toBe(false)
    const pcbPads = any_circuit_element
      .array()
      .parse(rawElements.filter((element) => element.type === "pcb_smtpad"))
      .filter(
        (element) =>
          element.type === "pcb_smtpad" &&
          element.pcb_component_id ===
            rawElements.find(
              (candidate) =>
                candidate.type === "pcb_component" &&
                candidate.source_component_id === regulator.source_component_id,
            )?.pcb_component_id,
      )
    // TI DBV top view: IN/GND/EN on one side, NC/OUT on the other.
    const centers = [1, 2, 3, 4, 5].map((pinNumber) => {
      const pad = pcbPads.find(
        (element) =>
          element.type === "pcb_smtpad" && element.port_hints?.includes(String(pinNumber)),
      )
      if (!pad || pad.type !== "pcb_smtpad" || !("x" in pad) || !("y" in pad)) {
        throw new Error(`Missing physical pad center ${pinNumber}`)
      }
      return { x: pad.x, y: pad.y }
    })
    expect(centers[0].x).toBe(centers[1].x)
    expect(centers[1].x).toBe(centers[2].x)
    expect(centers[3].x).toBe(centers[4].x)
    expect(centers[0].x).not.toBe(centers[4].x)
    expect(centers[0].y).toBe(centers[4].y)
    expect(centers[2].y).toBe(centers[3].y)
  })
  test("AOS G/S/D and MDD cathode/anode close the intended flyback loop and retain default-off paths", () => {
    for (const [name, pinNumber, netName] of [
      ["Q9", 1, "HAPTIC_NMOS_GATE"],
      ["Q9", 2, "GND"],
      ["Q9", 3, "HAPTIC_N"],
      ["D3", 1, "VMOTOR"],
      ["D3", 2, "HAPTIC_N"],
      ["R84", 1, "HAPTIC_NMOS_GATE"],
      ["R84", 2, "GND"],
      ["R85", 1, "MCU_HAPTIC_ENABLE"],
      ["R85", 2, "GND"],
      ["R82", 1, "VMOTOR"],
      ["R82", 2, "GND"],
    ] as const)
      expectPinNet({ name, pinNumber, netName })
  })
})
