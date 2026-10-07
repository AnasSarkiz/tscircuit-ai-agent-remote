import { expect, test } from "bun:test"
import { SmtPad } from "lib/components/primitive-components/SmtPad"
import { getTestFixture } from "tests/fixtures/get-test-fixture"

test("pill paste respects absolute margins, coverage and layout movement", async () => {
  const { circuit } = getTestFixture()
  const margins = [0, -0.2, 0.2, -0.4, -1, 0]
  circuit.add(
    <board width={32} height={14} routingDisabled>
      {(["pill", "rotated_pill"] as const).flatMap((shape, row) =>
        margins.map((solderPasteMargin, column) => (
          <chip
            key={`${shape}-${column}`}
            name={`U${row * margins.length + column + 1}`}
            pcbX={column * 5 - 12.5}
            pcbY={row * 5 - 2.5}
            pcbRotation={column * 45}
            pinLabels={{ 1: "PAD" }}
            footprint={
              <footprint>
                <smtpad
                  shape={shape}
                  ccwRotation={30}
                  width={2}
                  height={1}
                  radius={0.3}
                  solderPasteMargin={solderPasteMargin}
                  coveredWithSolderMask={column === 5}
                  portHints={["pin1"]}
                />
              </footprint>
            }
          />
        )),
      )}
      <pcbnotetext
        text="Pill paste: zero / inset / outset / square / removed / covered"
        pcbY={6}
        fontSize={0.4}
      />
    </board>,
  )
  await circuit.renderUntilSettled()
  const pastes = circuit.db.pcb_solder_paste.list()
  expect(pastes).toHaveLength(8)
  for (const [padIndex, pad] of circuit.db.pcb_smtpad.list().entries()) {
    const column = padIndex % margins.length
    const paste = pastes.find(
      (paste) => paste.pcb_smtpad_id === pad.pcb_smtpad_id,
    )
    if (column >= 4) {
      expect(paste).toBeUndefined()
      continue
    }
    if (paste?.shape !== "pill" && paste?.shape !== "rotated_pill")
      throw new Error("Expected rounded solder paste")
    expect(paste.width).toBeCloseTo([2, 1.6, 2.4, 1.2][column]!)
    expect(paste.height).toBeCloseTo([1, 0.6, 1.4, 0.2][column]!)
    expect(paste.radius).toBeCloseTo([0.3, 0.1, 0.5, 0][column]!)
  }
  const pad = circuit.selectOne(".U2 smtpad")
  if (!(pad instanceof SmtPad)) throw new Error("Expected the second SMT pad")
  const pasteBefore = pastes.find(
    (paste) => paste.pcb_smtpad_id === pad.pcb_smtpad_id,
  )!
  if (pasteBefore.shape !== "pill" && pasteBefore.shape !== "rotated_pill")
    throw new Error("Expected rounded solder paste")
  const { x: pasteXBefore, y: pasteYBefore } = pasteBefore
  pad._moveCircuitJsonElements({ deltaX: 0.5, deltaY: -0.25 })
  const pasteAfter = circuit.db.pcb_solder_paste.get(
    pasteBefore.pcb_solder_paste_id,
  )!
  if (pasteAfter.shape !== "pill" && pasteAfter.shape !== "rotated_pill")
    throw new Error("Expected rounded solder paste after moving")
  expect(pasteAfter.x).toBeCloseTo(pasteXBefore + 0.5)
  expect(pasteAfter.y).toBeCloseTo(pasteYBefore - 0.25)
  await expect(circuit).toMatchPcbSnapshot(import.meta.path, {
    showSolderPaste: true,
  })
})
