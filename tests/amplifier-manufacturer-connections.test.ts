import { describe, expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import { any_circuit_element } from "circuit-json"
import { z } from "zod"

const rawElements = z
  .array(z.object({ type: z.string() }).passthrough())
  .parse(
    JSON.parse(
      readFileSync(
        new URL(
          "../evidence/audio-charge-review-2026-10-03/amplifier-circuit.json",
          import.meta.url,
        ),
        "utf8",
      ),
    ),
  )
const sourceElements = any_circuit_element
  .array()
  .parse(rawElements.filter((element) => element.type.startsWith("source_")))

// ADI MAX98357A TQFN pin drawing; AOS AO3400A/AO3401A SOT-23 G/S/D drawing.
const expectPinNet = ({
  name,
  pinNumber,
  netName,
}: {
  name: string
  pinNumber: number
  netName: string
}) => {
  const sourceComponent = sourceElements.find(
    (element) => element.type === "source_component" && element.name === name,
  )
  if (!sourceComponent || sourceComponent.type !== "source_component") {
    throw new Error(`Missing amplifier component ${name}`)
  }
  const sourcePort = sourceElements.find(
    (element) =>
      element.type === "source_port" &&
      element.source_component_id === sourceComponent.source_component_id &&
      element.pin_number === pinNumber,
  )
  const sourceNet = sourceElements.find(
    (element) => element.type === "source_net" && element.name === netName,
  )
  if (
    !sourcePort ||
    sourcePort.type !== "source_port" ||
    !sourceNet ||
    sourceNet.type !== "source_net"
  ) {
    throw new Error(`Missing ${name}.${pinNumber} or ${netName}`)
  }
  expect(
    sourceElements.some(
      (element) =>
        element.type === "source_trace" &&
        element.connected_source_port_ids.includes(sourcePort.source_port_id) &&
        element.connected_source_net_ids.includes(sourceNet.source_net_id),
    ),
  ).toBe(true)
}

describe("amplifier manufacturer requirements", () => {
  test("power, exposed ground, differential output and left-channel gain use manufacturer pins", () => {
    for (const [name, pinNumber, netName] of [
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
      expectPinNet({ name, pinNumber, netName })
    for (const netName of ["SPEAKER_P", "SPEAKER_N"]) {
      const net = sourceElements.find(
        (element) => element.type === "source_net" && element.name === netName,
      )
      if (!net || net.type !== "source_net") throw new Error(netName)
      const groundedTrace = sourceElements.find(
        (element) =>
          element.type === "source_trace" &&
          element.connected_source_net_ids.includes(net.source_net_id) &&
          element.connected_source_net_ids.some((id) =>
            sourceElements.some(
              (other) =>
                other.type === "source_net" && other.source_net_id === id && other.name === "GND",
            ),
          ),
      )
      expect(groundedTrace).toBeUndefined()
    }
  })
  test("shutdown uses amplifier supply and MOSFET physical gate/source/drain polarity", () => {
    for (const [name, pinNumber, netName] of [
      ["Q1", 1, "AUDIO_NMOS_GATE"],
      ["Q1", 2, "GND"],
      ["Q1", 3, "AUDIO_PMOS_GATE"],
      ["Q2", 1, "AUDIO_PMOS_GATE"],
      ["Q2", 2, "VSYS"],
      ["Q2", 3, "AUDIO_ENABLE_SUPPLY"],
      ["U3", 4, "AMP_SD_MODE"],
      ["R62", 1, "VSYS"],
      ["R62", 2, "AUDIO_PMOS_GATE"],
      ["R61", 1, "AUDIO_NMOS_GATE"],
      ["R61", 2, "GND"],
      ["R64", 1, "AMP_SD_MODE"],
      ["R64", 2, "GND"],
    ] as const)
      expectPinNet({ name, pinNumber, netName })
    function resistanceOhms(name: string) {
      const resistor = sourceElements.find(
        (element) => element.type === "source_component" && element.name === name,
      )
      if (
        !resistor ||
        resistor.type !== "source_component" ||
        !("resistance" in resistor) ||
        typeof resistor.resistance !== "number"
      )
        throw new Error(name)
      return resistor.resistance
    }
    // ESP32 VOH>=0.8*VDD; provisional regulator minimum 3.18204V; +/-1.6% resistor corners.
    const minimumGateVoltage =
      (0.8 * 3.18204 * (resistanceOhms("R61") * 0.984)) /
      (resistanceOhms("R61") * 0.984 + resistanceOhms("R60") * 1.016)
    expect(minimumGateVoltage).toBeGreaterThan(2.5)
    // AOS leakage maximum 5uA at TJ=55C; 1kohm external pulldown bounds SD below B0 minimum 0.08V.
    const offVoltage = 5e-6 * resistanceOhms("R64") * 1.016
    expect(offVoltage).toBeLessThan(0.08)
    // VSYS study minimum 2.8V; left-channel B2 maximum is 1.5V.
    const minimumEnableVoltage =
      (2.8 * (resistanceOhms("R64") * 0.984)) /
      (resistanceOhms("R64") * 0.984 + resistanceOhms("R63") * 1.016 + 0.085)
    expect(minimumEnableVoltage).toBeGreaterThan(1.5)
  })
})
