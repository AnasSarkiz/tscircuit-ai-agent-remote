import { fanoutTracePath } from "@tscircuit/props"
import { z } from "zod"

export const viaHoleDiameterMm = 0.3
export const viaPadDiameterMm = 0.45

// Authored dimensional changes to replay inputs, not new solver output.
// Preserve every original saved route, position, layer and wire width on disk.
export function parseReplayWithRequestedVias(replayInput: unknown) {
  return z
    .array(fanoutTracePath)
    .parse(replayInput)
    .map((path) => ({
      ...path,
      route: path.route.map((point) =>
        point.route_type === "via"
          ? { ...point, via_diameter: viaPadDiameterMm, via_hole_diameter: viaHoleDiameterMm }
          : point,
      ),
    }))
}
