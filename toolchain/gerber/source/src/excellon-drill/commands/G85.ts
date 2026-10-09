import { z } from "zod"
import { defineExcellonDrillCommand } from "../define-excellon-drill-command"

export const G85 = defineExcellonDrillCommand({
  command_code: "G85",
  schema: z.object({
    command_code: z.literal("G85").default("G85"),
    start_x: z.number(),
    start_y: z.number(),
    x: z.number(),
    y: z.number(),
    width: z.number(), // slot width = tool diameter
  }),
  // Excellon canned slots carry both board-world endpoints in one block.
  stringify: ({ start_x, start_y, x, y }) =>
    `X${start_x.toFixed(4)}Y${start_y.toFixed(4)}G85X${x.toFixed(4)}Y${y.toFixed(4)}`,
})
