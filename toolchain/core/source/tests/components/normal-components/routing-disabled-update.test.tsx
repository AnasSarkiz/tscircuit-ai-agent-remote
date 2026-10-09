import { expect, test } from "bun:test"
import { Group } from "lib/components/primitive-components/Group/Group"
import { getTestFixture } from "tests/fixtures/get-test-fixture"

for (const control of ["platform", "board"] as const) {
  test(`PCB routing updates respect the ${control} disabled flag`, async () => {
    const { circuit } = getTestFixture({
      platform: { routingDisabled: control === "platform" },
    })
    const starts: object[] = []
    circuit.on("autorouting:start", (event) => { starts.push(event) })
    circuit.add(
      <board width={10} height={10} routingDisabled={control === "board"} autorouter={{ preset: "auto_local" }}>
        <resistor name="R1" resistance="1k" footprint="0402" pcbX={-2} />
        <resistor name="R2" resistance="1k" footprint="0402" pcbX={2} />
        <trace from=".R1 > .pin1" to=".R2 > .pin1" />
      </board>,
    )
    await circuit.renderUntilSettled()
    const board = circuit.firstChild
    if (!(board instanceof Group)) throw Error("Expected the actual board routing group")
    // Async footprint/layout changes revisit this lifecycle method after the
    // initial pass. It must enforce the same controls as the initial pass.
    board.updatePcbTraceRender()
    await circuit.renderUntilSettled()
    expect(starts).toHaveLength(0)
    expect(circuit.getCircuitJson().filter(element => ["pcb_trace", "pcb_via"].includes(element.type))).toHaveLength(0)
  })
}

test("routing-enabled boards still produce actual copper", async () => {
  const { circuit } = getTestFixture()
  circuit.add(
    <board width={10} height={10} autorouter={{ preset: "auto_local" }}>
      <resistor name="R1" resistance="1k" footprint="0402" pcbX={-2} />
      <resistor name="R2" resistance="1k" footprint="0402" pcbX={2} />
      <trace from=".R1 > .pin1" to=".R2 > .pin1" />
    </board>,
  )
  await circuit.renderUntilSettled()
  expect(circuit.getCircuitJson().filter(element => element.type === "pcb_trace").length).toBeGreaterThan(0)
})
