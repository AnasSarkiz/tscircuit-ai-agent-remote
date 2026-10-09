import { expect, test } from "bun:test"
import type { AnyCircuitElement } from "circuit-json"
import {
  convertSoupToExcellonDrillCommands,
  stringifyExcellonDrill,
} from "src/excellon-drill"

test("canned slots emit both endpoints in one Excellon block without an extra round drill", () => {
  const expected = [
    "X-4.3251Y-31.0741G85X-4.3251Y-30.4741",
    "X-4.0251Y-30.7741G85X-4.6251Y-30.7741",
    "X-4.3251Y-30.4741G85X-4.3251Y-31.0741",
    "X-4.6251Y-30.7741G85X-4.0251Y-30.7741",
  ]
  for (const [index, rotation] of [0, 90, 180, 270].entries()) {
    const circuitJson: AnyCircuitElement[] = [
      {
        type: "pcb_hole",
        pcb_hole_id: "pcb_hole_0",
        hole_shape: "rotated_pill",
        hole_width: 0.8,
        hole_height: 1.4,
        x: -4.3251,
        y: -30.7741,
        ccw_rotation: rotation,
      },
    ]
    const commands = convertSoupToExcellonDrillCommands({
      circuitJson,
      is_plated: false,
    })
    const text = stringifyExcellonDrill(commands)
    expect(
      commands.filter((command) => command.command_code === "G85"),
    ).toHaveLength(1)
    expect(
      commands.filter((command) => command.command_code === "drill_at"),
    ).toHaveLength(0)
    expect(text.split("\n").filter((line) => line.includes("G85"))).toEqual([
      expected[index]!,
    ])
  }
})
