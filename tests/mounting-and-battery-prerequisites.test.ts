import { expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import { any_circuit_element } from "circuit-json"
import { z } from "zod"

const elements = z
  .array(z.object({ type: z.string() }).passthrough())
  .parse(JSON.parse(readFileSync(new URL("../dist/index/circuit.json", import.meta.url), "utf8")))
const sourceElements = any_circuit_element
  .array()
  .parse(elements.filter((element) => element.type.startsWith("source_")))

test("AKY2945 centre NTC is connected and unresolved outer polarity is left open", () => {
  const connector = sourceElements.find(
    (element) => element.type === "source_component" && element.name === "J3",
  )
  if (!connector || connector.type !== "source_component") throw new Error("Missing J3")
  const ntc = sourceElements.find(
    (element) => element.type === "source_net" && element.name === "PACK_NTC",
  )
  if (!ntc || ntc.type !== "source_net") throw new Error("Missing PACK_NTC")
  for (const pinNumber of [1, 2, 3]) {
    const port = sourceElements.find(
      (element) =>
        element.type === "source_port" &&
        element.source_component_id === connector.source_component_id &&
        element.pin_number === pinNumber,
    )
    if (!port || port.type !== "source_port") throw new Error(`Missing J3 pin ${pinNumber}`)
    const connections = sourceElements.filter(
      (element) =>
        element.type === "source_trace" &&
        element.connected_source_port_ids.includes(port.source_port_id),
    )
    if (pinNumber !== 2) expect(connections).toHaveLength(0)
    else {
      expect(connections).toHaveLength(1)
      expect(connections[0]).toMatchObject({ connected_source_net_ids: [ntc.source_net_id] })
    }
  }
})

test("A4 trial M2 mounts are nonconductive holes with all-layer circular clearance", () => {
  const mounts = elements.filter(
    (element) => element.type === "pcb_hole" && element.hole_diameter === 2.2,
  )
  expect(mounts).toHaveLength(2)
  for (const [x, y] of [
    [22, -23],
    [-21.5, -29.5],
  ]) {
    expect(
      mounts.some(
        (element) => element.x === x && element.y === y && element.pcb_component_id === null,
      ),
    ).toBe(true)
    expect(
      elements.some(
        (element) =>
          element.type === "pcb_keepout" &&
          element.shape === "circle" &&
          element.radius === 3 &&
          JSON.stringify(element.center) === JSON.stringify({ x, y }) &&
          JSON.stringify(element.layers) === JSON.stringify(["top", "inner1", "inner2", "bottom"]),
      ),
    ).toBe(true)
  }
})
