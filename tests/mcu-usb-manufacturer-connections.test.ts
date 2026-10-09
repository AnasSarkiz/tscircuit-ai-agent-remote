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
          "../evidence/pcb-completion-2026-10-08/diagnostic-native/mcu-usb/circuit.json",
          import.meta.url,
        ),
        "utf8",
      ),
    ),
  )
const generatedReview = any_circuit_element
  .array()
  .parse(rawElements.filter((element) => element.type.startsWith("source_")))
const moduleComponent = generatedReview.find(
  (element) => element.type === "source_component" && element.name === "U1",
)
if (!moduleComponent || moduleComponent.type !== "source_component") {
  throw new Error("MCU application evidence lacks the module")
}
const moduleSourcePorts = generatedReview.filter(
  (element) =>
    element.type === "source_port" &&
    element.source_component_id === moduleComponent.source_component_id,
)

describe("Espressif module datasheet v1.8 connection requirements", () => {
  test("every emitted native element conforms to the installed Circuit JSON schema", () => {
    const failingElements = rawElements.flatMap((element, index) =>
      any_circuit_element.safeParse(element).success ? [] : [{ index, type: element.type }],
    )
    expect(failingElements).toEqual([])
  })
  test("module supply, reset, USB polarity and boot reach the correct physical pins", () => {
    for (const [pinNumber, netName] of [
      [2, "V3V3"],
      [3, "MCU_EN"],
      [13, "MCU_USB_DN"],
      [14, "MCU_USB_DP"],
      [27, "MCU_BOOT_N"],
    ] as const) {
      const port = moduleSourcePorts.find(
        (element) => element.type === "source_port" && element.pin_number === pinNumber,
      )
      if (!port || port.type !== "source_port") throw new Error(`Missing module pin ${pinNumber}`)
      const net = generatedReview.find(
        (element) => element.type === "source_net" && element.name === netName,
      )
      if (!net || net.type !== "source_net") throw new Error(`Missing net ${netName}`)
      expect(
        generatedReview.some(
          (element) =>
            element.type === "source_trace" &&
            element.connected_source_port_ids.includes(port.source_port_id) &&
            element.connected_source_net_ids.includes(net.source_net_id),
        ),
      ).toBe(true)
    }
  })
  test("octal PSRAM pins 28–30 stay disconnected from external applications", () => {
    const occupiedPortIds = moduleSourcePorts
      .filter(
        (element) =>
          element.type === "source_port" && [28, 29, 30].includes(element.pin_number ?? -1),
      )
      .map((element) => (element.type === "source_port" ? element.source_port_id : ""))
    expect(occupiedPortIds).toHaveLength(3)
    expect(
      generatedReview.filter(
        (element) =>
          element.type === "source_trace" &&
          element.connected_source_port_ids.some((portId) => occupiedPortIds.includes(portId)),
      ),
    ).toHaveLength(0)
  })
  test("all nine exposed ground shapes retain their physical identity and internal connection", () => {
    const groundPorts = moduleSourcePorts.filter(
      (element) => element.type === "source_port" && element.port_hints?.includes("pin41"),
    )
    expect(groundPorts).toHaveLength(9)
    expect(
      moduleComponent.internally_connected_source_port_ids?.some((portIds) =>
        groundPorts.every(
          (element) => element.type === "source_port" && portIds.includes(element.source_port_id),
        ),
      ),
    ).toBe(true)
  })
  test("the diagnostic remains unrouted and contains no emitted errors", () => {
    expect(
      rawElements.filter(
        (element) =>
          element.type === "pcb_trace" ||
          element.type === "pcb_via" ||
          element.type.endsWith("_error"),
      ),
    ).toHaveLength(0)
  })
})
