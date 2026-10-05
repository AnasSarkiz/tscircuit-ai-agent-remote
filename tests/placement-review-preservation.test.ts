import { describe, expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import { z } from "zod"

// Compare untouched native outputs. Full strict schema failures remain separate gates.
const nativeElements = z.array(z.object({ type: z.string() }).passthrough())
const canonical = nativeElements.parse(
  JSON.parse(readFileSync(new URL("../dist/index/circuit.json", import.meta.url), "utf8")),
)
const placement = nativeElements.parse(
  JSON.parse(readFileSync(new URL("../dist/placement/circuit.json", import.meta.url), "utf8")),
)
const before = nativeElements.parse(
  JSON.parse(
    readFileSync(
      new URL("../evidence/a4-placement-gate-2026-10-04/before-circuit.json", import.meta.url),
      "utf8",
    ),
  ),
)

function electricalPartitions(elements: typeof canonical) {
  const components = z
    .array(z.object({ source_component_id: z.string(), name: z.string() }))
    .parse(elements.filter((element) => element.type === "source_component"))
  const componentsById = Object.fromEntries(
    components.map((component) => [component.source_component_id, component]),
  )
  const ports = z
    .array(
      z.object({ source_port_id: z.string(), source_component_id: z.string(), name: z.string() }),
    )
    .parse(elements.filter((element) => element.type === "source_port"))
    .filter((port) => componentsById[port.source_component_id])
  const nets = z
    .array(z.object({ source_net_id: z.string(), name: z.string() }))
    .parse(elements.filter((element) => element.type === "source_net"))
  const parents: Record<string, string> = {}
  function root(identifier: string): string {
    parents[identifier] ??= identifier
    if (parents[identifier] !== identifier) parents[identifier] = root(parents[identifier])
    return parents[identifier]
  }
  function join(identifiers: string[]) {
    for (const identifier of identifiers.slice(1)) parents[root(identifier)] = root(identifiers[0])
  }
  for (const element of elements) {
    if (element.type === "source_trace") {
      const trace = z
        .object({
          connected_source_port_ids: z.array(z.string()),
          connected_source_net_ids: z.array(z.string()),
        })
        .parse(element)
      join([...trace.connected_source_port_ids, ...trace.connected_source_net_ids])
    } else if (element.type === "source_component_internal_connection") {
      join(z.object({ source_port_ids: z.array(z.string()) }).parse(element).source_port_ids)
    }
  }
  const groups: Record<string, string[]> = {}
  for (const port of ports)
    (groups[root(port.source_port_id)] ??= []).push(
      `${componentsById[port.source_component_id].name}.${port.name}`,
    )
  for (const net of nets) (groups[root(net.source_net_id)] ??= []).push(`net.${net.name}`)
  return Object.values(groups)
    .map((group) => group.sort())
    .sort((first, second) => first.join("|").localeCompare(second.join("|")))
}

describe("Native placement review preserves the board", () => {
  test("the inspection output has no copper routes, vias or pours", () => {
    expect(
      placement.filter((element) =>
        ["pcb_trace", "pcb_via", "pcb_copper_pour"].includes(element.type),
      ),
    ).toEqual([])
  })

  test("all electrical connections and physical placement features match the canonical board", () => {
    const electronics = canonical.filter((element) => element.type === "source_component")
    const electronicIds = new Set(electronics.map((element) => element.source_component_id))
    const pcbIds = new Set(
      canonical
        .filter(
          (element) =>
            element.type === "pcb_component" && electronicIds.has(element.source_component_id),
        )
        .map((element) => element.pcb_component_id),
    )
    const physicalElectronics = canonical.filter((element) => {
      if (element.type === "source_port") return electronicIds.has(element.source_component_id)
      if (element.type === "pcb_component") return electronicIds.has(element.source_component_id)
      if (element.type === "pcb_port") return pcbIds.has(element.pcb_component_id)
      return true
    })
    for (const type of [
      "source_component",
      "source_port",
      "source_net",
      "pcb_component",
      "pcb_smtpad",
      "pcb_plated_hole",
      "pcb_hole",
      "pcb_keepout",
      "pcb_port",
    ]) {
      expect(placement.filter((element) => element.type === type)).toEqual(
        physicalElectronics.filter((element) => element.type === type),
      )
    }
    // Native routing adds duplicate source traces and board-via ports. Compare
    // the complete electrical partition of the actual electronics and nets.
    expect(electricalPartitions(placement)).toEqual(electricalPartitions(canonical))
  })

  test("the original switching paths and USB geometry survive the qualified stackup width change", () => {
    const canonicalCopper = canonical.filter((element) =>
      ["pcb_trace", "pcb_via"].includes(element.type),
    )
    const beforeCopper = before.filter((element) => ["pcb_trace", "pcb_via"].includes(element.type))
    expect(beforeCopper).toHaveLength(4)
    const wireRoute = z.array(
      z.object({
        route_type: z.literal("wire"),
        x: z.number(),
        y: z.number(),
        width: z.number(),
        layer: z.string(),
        start_pcb_port_id: z.string().optional(),
        end_pcb_port_id: z.string().optional(),
      }),
    )
    for (const trace of beforeCopper) {
      const original = wireRoute.parse(trace.route)
      // These two USB routes were changed from 0.2906 to 0.2979 mm for the
      // accepted 1.0 mm stackup; their positions and terminal topology stay fixed.
      const expected = ["source_trace_6", "source_trace_7"].includes(String(trace.source_trace_id))
        ? original.map((point) => ({ ...point, width: 0.2979 }))
        : original
      const matchingRoutes = canonicalCopper.flatMap((element) => {
        const parsed = wireRoute.safeParse(element.route)
        return parsed.success ? [parsed.data] : []
      })
      expect(matchingRoutes).toContainEqual(expected)
    }
  })
})
