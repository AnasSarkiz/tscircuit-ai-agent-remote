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
function portNet(connection: { reference: string; pinNumber: number; netName: string }) {
  const component = sourceElements.find(
    (element) => element.type === "source_component" && element.name === connection.reference,
  )
  if (!component || component.type !== "source_component")
    throw new Error(`Missing ${connection.reference}`)
  const port = sourceElements.find(
    (element) =>
      element.type === "source_port" &&
      element.source_component_id === component.source_component_id &&
      element.pin_number === connection.pinNumber,
  )
  const net = sourceElements.find(
    (element) => element.type === "source_net" && element.name === connection.netName,
  )
  if (!port || port.type !== "source_port" || !net || net.type !== "source_net")
    throw new Error(`Missing ${connection.reference} pin or ${connection.netName} net`)
  expect(
    sourceElements.some(
      (element) =>
        element.type === "source_trace" &&
        element.connected_source_port_ids.includes(port.source_port_id) &&
        element.connected_source_net_ids.includes(net.source_net_id),
    ),
  ).toBe(true)
}
describe("Native A4 board boundaries and fabrication gate", () => {
  test("board has top-only physical components within the accepted PCB dimensions", () => {
    expect(rawElements.filter((element) => element.type === "pcb_component")).toHaveLength(135)
    expect(
      rawElements.filter((element) => element.type === "pcb_component" && element.layer !== "top"),
    ).toEqual([])
    expect(rawElements.find((element) => element.type === "pcb_board")).toMatchObject({
      width: 50,
      height: 65,
      thickness: 1.0,
    })
  })
  test("fabrication requires nonempty actual copper and zero unresolved native errors", () => {
    expect(rawElements.filter((element) => element.type === "pcb_trace").length).toBeGreaterThan(0)
    expect(rawElements.filter((element) => element.type.includes("error"))).toEqual([])
  })
  test("there is one shared instance of each inter-sheet rail", () => {
    for (const netName of ["GND", "V3V3", "VSYS", "VBUS", "VMIC", "PACK_BAT", "HOLD_HARDWARE"])
      expect(
        sourceElements.filter(
          (element) => element.type === "source_net" && element.name === netName,
        ),
      ).toHaveLength(1)
    for (const connection of [
      { reference: "U16", pinNumber: 13, netName: "VBUS" },
      { reference: "U16", pinNumber: 10, netName: "VSYS" },
      { reference: "U2", pinNumber: 10, netName: "VSYS" },
      { reference: "U2", pinNumber: 6, netName: "V3V3" },
      { reference: "U1", pinNumber: 2, netName: "V3V3" },
      { reference: "J3", pinNumber: 2, netName: "PACK_NTC" },
    ])
      portNet(connection)
  })
  test("hardware hold and privacy remain distinct from buffered MCU readback", () => {
    for (const connection of [
      { reference: "SW4", pinNumber: 2, netName: "HOLD_HARDWARE" },
      { reference: "U26", pinNumber: 2, netName: "HOLD_HARDWARE" },
      { reference: "U23", pinNumber: 3, netName: "HOLD_HARDWARE" },
      { reference: "SW5", pinNumber: 2, netName: "MIC_INPUT" },
      { reference: "U23", pinNumber: 1, netName: "MIC_INPUT" },
      { reference: "U1", pinNumber: 23, netName: "MCU_HOLD_READ" },
    ])
      portNet(connection)
  })
  test("dual microphones, external loads and GPIO interfaces have actual source connections", () => {
    for (const connection of [
      { reference: "U4", pinNumber: 5, netName: "VMIC" },
      { reference: "U5", pinNumber: 5, netName: "VMIC" },
      { reference: "U4", pinNumber: 2, netName: "GND" },
      { reference: "U5", pinNumber: 2, netName: "VMIC" },
      { reference: "J4", pinNumber: 1, netName: "SPEAKER_P" },
      { reference: "J4", pinNumber: 2, netName: "SPEAKER_N" },
      { reference: "TP_MOTOR_P", pinNumber: 1, netName: "VMOTOR" },
      { reference: "TP_MOTOR_N", pinNumber: 1, netName: "HAPTIC_N" },
      { reference: "U1", pinNumber: 8, netName: "MCU_MIC_BCLK" },
      { reference: "U1", pinNumber: 9, netName: "MCU_MIC_WS" },
      { reference: "U1", pinNumber: 10, netName: "MCU_MIC_SD" },
      { reference: "U1", pinNumber: 17, netName: "MCU_AUDIO_BCLK" },
      { reference: "U1", pinNumber: 24, netName: "MCU_BACKLIGHT_PWM" },
    ])
      portNet(connection)
  })
})
