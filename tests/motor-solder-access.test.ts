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

test("motor connector is removed while two accessible solder pads retain the motor circuit", () => {
  expect(
    sourceElements.some((element) => element.type === "source_component" && element.name === "J8"),
  ).toBe(false)
  for (const terminal of [
    { name: "TP_MOTOR_P", net: "VMOTOR", x: 22, y: -8 },
    { name: "TP_MOTOR_N", net: "HAPTIC_N", x: 22, y: -11 },
  ]) {
    const component = sourceElements.find(
      (element) => element.type === "source_component" && element.name === terminal.name,
    )
    if (!component || component.type !== "source_component")
      throw new Error(`Missing ${terminal.name}`)
    expect(component).toMatchObject({
      ftype: "simple_test_point",
      footprint_variant: "pad",
      pad_diameter: 2,
    })
    const port = sourceElements.find(
      (element) =>
        element.type === "source_port" &&
        element.source_component_id === component.source_component_id &&
        element.pin_number === 1,
    )
    const net = sourceElements.find(
      (element) => element.type === "source_net" && element.name === terminal.net,
    )
    if (!port || port.type !== "source_port" || !net || net.type !== "source_net")
      throw new Error(`Missing ${terminal.name} connection`)
    expect(
      sourceElements.some(
        (element) =>
          element.type === "source_trace" &&
          element.connected_source_port_ids.includes(port.source_port_id) &&
          element.connected_source_net_ids.includes(net.source_net_id),
      ),
    ).toBe(true)
    const pcbComponent = rawElements.find(
      (element) =>
        element.type === "pcb_component" &&
        element.source_component_id === component.source_component_id,
    )
    if (!pcbComponent) throw new Error(`Missing ${terminal.name} PCB geometry`)
    expect(pcbComponent.layer).toBe("top")
    expect(
      rawElements.filter(
        (element) =>
          element.type === "pcb_smtpad" &&
          element.pcb_component_id === pcbComponent.pcb_component_id,
      ),
    ).toEqual([
      expect.objectContaining({
        shape: "circle",
        radius: 1,
        x: terminal.x,
        y: terminal.y,
        layer: "top",
      }),
    ])
    expect(
      rawElements.filter(
        (element) =>
          element.type === "pcb_plated_hole" &&
          element.pcb_component_id === pcbComponent.pcb_component_id,
      ),
    ).toEqual([])
  }
  expect(
    sourceElements.some((element) => element.type === "source_component" && element.name === "Q9"),
  ).toBe(true)
  expect(
    sourceElements.some((element) => element.type === "source_component" && element.name === "J6"),
  ).toBe(true)
})
