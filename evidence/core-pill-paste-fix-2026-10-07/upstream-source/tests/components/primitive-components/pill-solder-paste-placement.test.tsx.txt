import { expect, test } from "bun:test"
import { getTestFixture } from "tests/fixtures/get-test-fixture"

test("pill paste follows emitted pad geometry on both layers and all quarter turns", async () => {
  const { circuit } = getTestFixture()
  circuit.add(
    <board width={24} height={20} routingDisabled>
      {(["top", "bottom"] as const).flatMap((layer, layerIndex) =>
        (["pill", "rotated_pill"] as const).flatMap((shape, shapeIndex) =>
          [0, 90, 180, 270].map((pcbRotation, rotationIndex) => (
            <chip
              key={`${layer}-${shape}-${pcbRotation}`}
              name={`U${layerIndex * 8 + shapeIndex * 4 + rotationIndex + 1}`}
              layer={layer}
              pcbX={rotationIndex * 5 - 7.5}
              pcbY={(layerIndex * 2 + shapeIndex) * 4 - 6}
              pcbRotation={pcbRotation}
              pinLabels={{ 1: "PAD" }}
              footprint={
                <footprint>
                  <smtpad
                    shape={shape}
                    ccwRotation={35}
                    width={2}
                    height={1}
                    radius={0.5}
                    pcbX={0.6}
                    pcbY={0.3}
                    portHints={["pin1"]}
                  />
                </footprint>
              }
            />
          )),
        ),
      )}
      <pcbnotetext
        text="Pill paste: top / bottom; 0 / 90 / 180 / 270 degrees"
        pcbY={9}
        fontSize={0.4}
      />
    </board>,
  )
  await circuit.renderUntilSettled()
  const pads = circuit.db.pcb_smtpad.list()
  const pastes = circuit.db.pcb_solder_paste.list()
  expect(pads).toHaveLength(16)
  expect(pastes).toHaveLength(pads.length)
  for (const pad of pads) {
    const paste = pastes.find(
      (paste) => paste.pcb_smtpad_id === pad.pcb_smtpad_id,
    )
    if (
      (pad.shape !== "pill" && pad.shape !== "rotated_pill") ||
      (paste?.shape !== "pill" && paste?.shape !== "rotated_pill")
    )
      throw new Error("Expected a rounded pad and its rounded paste aperture")
    expect(paste.shape).toBe(pad.shape)
    expect(paste.layer).toBe(pad.layer)
    expect(paste.pcb_component_id).toBe(pad.pcb_component_id)
    expect(paste.subcircuit_id).toBe(pad.subcircuit_id)
    expect(paste.pcb_group_id).toBe(pad.pcb_group_id)
    expect(paste.x).toBeCloseTo(pad.x)
    expect(paste.y).toBeCloseTo(pad.y)
    expect(paste.width).toBeCloseTo(pad.width * 0.7)
    expect(paste.height).toBeCloseTo(pad.height * 0.7)
    expect(paste.radius).toBeCloseTo(pad.radius * 0.7)
    if (pad.shape === "rotated_pill" && paste.shape === "rotated_pill")
      expect(paste.ccw_rotation).toBe(pad.ccw_rotation)
  }
  await expect(circuit).toMatchPcbSnapshot(import.meta.path, {
    showSolderPaste: true,
  })
})
