import { expect, test } from "bun:test"
import { any_circuit_element } from "circuit-json"
import { getTestFixture } from "tests/fixtures/get-test-fixture"

test("generated position and optional ownership metadata match circuit-json", async () => {
  const { circuit } = getTestFixture()
  circuit.add(
    <board width="30mm" height="25mm" routingDisabled>
      <group name="G1" pcbX={0} pcbY={0}>
        <resistor
          name="R1"
          resistance="1k"
          footprint="0402"
          pcbX={3}
          pcbY={-2}
        />
      </group>
      <silkscreentext text="Board label" pcbX={-8} pcbY={8} />
      <hole name="H1" diameter="1mm" pcbX={10} pcbY={8} />
    </board>,
  )
  await circuit.renderUntilSettled()
  const elements = circuit.getCircuitJson()
  for (const element of elements) {
    const result = any_circuit_element.safeParse(element)
    expect(result.success, element.type).toBe(true)
  }
  const resistor = circuit.db.pcb_component.list()[0]!
  expect(resistor.display_offset_x).toBe("3mm")
  expect(resistor.display_offset_y).toBe("-2mm")
  expect(resistor.center).toEqual({ x: 3, y: -2 })
})
