import { expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import { any_circuit_element } from "circuit-json"
import { z } from "zod"

// Reapply manufacturer pin requirements to the current whole-board source,
// rather than relying only on the historical single-sheet fixtures. This
// checks logical assignments; physical copper and full schema gates are separate.
// Sources: Espressif ESP32-S3-WROOM-1 v1.8, TI BQ24074 SLUS810,
// TI TPS63802 SLVSEU9D, ADI MAX98357A, TDK ICS-43434 DS-000069,
// TI TPS3808 and the preserved manufacturer review evidence in this repository.
const rawElements = z
  .array(z.object({ type: z.string() }).passthrough())
  .parse(JSON.parse(readFileSync(new URL("../dist/index/circuit.json", import.meta.url), "utf8")))
const sourceElements = any_circuit_element
  .array()
  .parse(rawElements.filter((element) => element.type.startsWith("source_")))

function getPort(connection: { reference: string; pinNumber: number }) {
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
  if (!port || port.type !== "source_port")
    throw new Error(`Missing ${connection.reference}.pin${connection.pinNumber}`)
  return port
}

function expectPinNet(connection: { reference: string; pinNumber: number; netName: string }) {
  const port = getPort(connection)
  const net = sourceElements.find(
    (element) => element.type === "source_net" && element.name === connection.netName,
  )
  if (!net || net.type !== "source_net") throw new Error(`Missing ${connection.netName}`)
  expect(
    sourceElements.some(
      (element) =>
        element.type === "source_trace" &&
        element.connected_source_port_ids.includes(port.source_port_id) &&
        element.connected_source_net_ids.includes(net.source_net_id),
    ),
  ).toBe(true)
}

test("current MCU USB, supply, reset and boot use Espressif physical pins", () => {
  for (const [pinNumber, netName] of [
    [2, "V3V3"],
    [3, "MCU_EN"],
    [13, "MCU_USB_DN"],
    [14, "MCU_USB_DP"],
    [27, "MCU_BOOT_N"],
  ] as const)
    expectPinNet({ reference: "U1", pinNumber, netName })
  for (const pinNumber of [28, 29, 30]) {
    const port = getPort({ reference: "U1", pinNumber })
    expect(
      sourceElements.filter(
        (element) =>
          element.type === "source_trace" &&
          element.connected_source_port_ids.includes(port.source_port_id),
      ),
    ).toHaveLength(0)
  }
})

test("current charger and battery supervisor retain manufacturer power and control pins", () => {
  for (const [reference, pinNumber, netName] of [
    ["U16", 1, "PACK_NTC"],
    ["U16", 2, "PACK_BAT"],
    ["U16", 3, "PACK_BAT"],
    ["U16", 4, "GND"],
    ["U16", 5, "GND"],
    ["U16", 6, "GND"],
    ["U16", 7, "CHARGE_PGOOD_N"],
    ["U16", 8, "GND"],
    ["U16", 9, "CHARGE_STATUS_N"],
    ["U16", 10, "VSYS"],
    ["U16", 11, "VSYS"],
    ["U16", 12, "CHARGER_ILIM"],
    ["U16", 13, "VBUS"],
    ["U16", 16, "CHARGER_ISET"],
    ["U16", 17, "GND"],
    ["U25", 1, "BUCK_ENABLE"],
    ["U25", 2, "GND"],
    ["U25", 3, "VSYS"],
    ["U25", 5, "PACK_BAT"],
    ["U25", 6, "VSYS"],
    ["J3", 2, "PACK_NTC"],
  ] as const)
    expectPinNet({ reference, pinNumber, netName })
  // No defaulted polarity, fabricated harness qualification or NC wiring.
  for (const [reference, pinNumber] of [
    ["J3", 1],
    ["J3", 3],
    ["U16", 14],
    ["U16", 15],
    ["U25", 4],
  ] as const) {
    const port = getPort({ reference, pinNumber })
    expect(
      sourceElements.filter(
        (element) =>
          element.type === "source_trace" &&
          element.connected_source_port_ids.includes(port.source_port_id),
      ),
    ).toHaveLength(0)
  }
})

test("current regulator retains TI power, ground, feedback and switching pin identities", () => {
  for (const [pinNumber, netName] of [
    [1, "BUCK_ENABLE"],
    [2, "GND"],
    [4, "REG_FB"],
    [5, "REG_PG"],
    [6, "V3V3"],
    [10, "VSYS"],
  ] as const) {
    expectPinNet({ reference: "U2", pinNumber, netName })
  }
  // These ground and switch pins are assigned through pin-to-pin traces.
  for (const [fromPin, toReference, toPin] of [
    [3, "U2", 2],
    [8, "U2", 3],
    [7, "L1", 2],
    [9, "L1", 1],
  ] as const) {
    const fromPort = getPort({ reference: "U2", pinNumber: fromPin })
    const toPort = getPort({ reference: toReference, pinNumber: toPin })
    expect(
      sourceElements.some(
        (element) =>
          element.type === "source_trace" &&
          element.connected_source_port_ids.includes(fromPort.source_port_id) &&
          element.connected_source_port_ids.includes(toPort.source_port_id),
      ),
    ).toBe(true)
  }
})

test("current amplifier supply and differential speaker outputs retain manufacturer pin assignments", () => {
  for (const [reference, pinNumber, netName] of [
    ["U3", 2, "VSYS"],
    ["U3", 7, "VSYS"],
    ["U3", 8, "VSYS"],
    ["U3", 3, "GND"],
    ["U3", 11, "GND"],
    ["U3", 15, "GND"],
    ["U3", 17, "GND"],
    ["U3", 9, "SPEAKER_P"],
    ["U3", 10, "SPEAKER_N"],
    ["J4", 1, "SPEAKER_P"],
    ["J4", 2, "SPEAKER_N"],
    ["U3", 1, "AMP_DIN"],
    ["U3", 14, "AMP_LRCLK"],
    ["U3", 16, "AMP_BCLK"],
  ] as const)
    expectPinNet({ reference, pinNumber, netName })
})

test("current dual microphone power, data, clocks and channel select retain TDK pins", () => {
  for (const reference of ["U4", "U5"]) {
    for (const [pinNumber, netName] of [
      [1, "MIC_WS"],
      [3, "GND"],
      [4, "MIC_BCLK"],
      [5, "VMIC"],
      [6, "MIC_SD"],
    ] as const)
      expectPinNet({ reference, pinNumber, netName })
    expectPinNet({ reference, pinNumber: 2, netName: reference === "U4" ? "GND" : "VMIC" })
  }
})
