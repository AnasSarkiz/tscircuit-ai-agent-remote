import { describe, expect, test } from "bun:test"
import { readFileSync } from "node:fs"

const encoderImport = readFileSync(
  new URL("../imports/EC11E15244G1/EC11E15244G1.tsx", import.meta.url),
  "utf8",
)
const regulatorImport = readFileSync(
  new URL("../imports/TPS63802DLAR/TPS63802DLAR.tsx", import.meta.url),
  "utf8",
)
const regulatorPinLabels = regulatorImport.split("const pinLabels = {")[1]?.split("} as const")[0]
if (!regulatorPinLabels) throw new Error("Imported regulator pin labels could not be inspected")
const regulatorPinNumbers = Array.from(regulatorPinLabels.matchAll(/pin(\d+):/g), (match) =>
  Number(match[1]),
)
const terminalHoleDiametersMm = Array.from(
  encoderImport.matchAll(/holeDiameter="([0-9.]+)mm"/g),
  (match) => Number(match[1]),
)
const mountingSlotLengthsMm = Array.from(
  encoderImport.matchAll(/holeWidth="([0-9.]+)mm"/g),
  (match) => Number(match[1]),
)

// Independent requirements from TI SLVSEU9D section 7, page 4.
describe("C2845237 TPS63802DLAR pin identity qualification", () => {
  test("retains all ten physical pin numbers", () => {
    expect(regulatorPinNumbers).toEqual(Array.from({ length: 10 }, (_, index) => index + 1))
  })
  test("retains the exact manufacturer function on every pin", () => {
    const manufacturerFunctions = [
      "EN",
      "MODE",
      "AGND",
      "FB",
      "PG",
      "VOUT",
      "L2",
      "GND",
      "L1",
      "VIN",
    ]
    for (const [index, manufacturerFunction] of manufacturerFunctions.entries()) {
      expect(regulatorPinLabels).toContain(`pin${index + 1}: ["${manufacturerFunction}"]`)
    }
  })
})

// Independent geometry limits from ALPS EC11E15244G1 mounting drawing;
// current official EC11E catalogue (Update 2510), page 2, drawing 2.
describe("C370970 EC11E15244G1 mechanical import qualification", () => {
  test("five terminal holes meet the 1.00-1.10 mm manufacturer range", () => {
    expect(terminalHoleDiametersMm).toHaveLength(5)
    for (const diameterMm of terminalHoleDiametersMm) {
      expect(diameterMm).toBeGreaterThanOrEqual(1)
      expect(diameterMm).toBeLessThanOrEqual(1.1)
    }
  })
  test("both mounting slots meet the 2.60-2.70 mm manufacturer length range", () => {
    expect(mountingSlotLengthsMm).toHaveLength(2)
    for (const lengthMm of mountingSlotLengthsMm) {
      expect(lengthMm).toBeGreaterThanOrEqual(2.6)
      expect(lengthMm).toBeLessThanOrEqual(2.7)
    }
  })
})
