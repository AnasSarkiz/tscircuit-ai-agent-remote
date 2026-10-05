import { readFileSync, mkdirSync, writeFileSync } from "node:fs"
import { join } from "node:path"
import { convertCircuitJsonToPcbSvg } from "circuit-to-svg"
import sharp from "sharp"
import { z } from "zod"

// Diagnostic views use the untouched native output. Full strict-schema and
// fabrication gates run separately; rendering never constitutes approval.
const circuitPath = process.argv[2]
const outputDirectory = process.argv[3]
if (!circuitPath || !outputDirectory)
  throw new Error("Provide native Circuit JSON and output directory")
const circuitJson = z
  .array(z.object({ type: z.string() }).passthrough())
  .parse(JSON.parse(readFileSync(circuitPath, "utf8")))
mkdirSync(outputDirectory, { recursive: true })
const common = {
  width: 1000,
  height: 1300,
  shouldDrawErrors: true,
  shouldDrawWarnings: true,
  showErrorsInTextOverlay: false,
  showPinNumbers: false,
}
const views = [
  ...["top", "inner1", "inner2", "bottom"].map((layer) => ({ name: layer, layer })),
  { name: "top-mask", layer: "top", showSolderMask: true },
  { name: "top-paste", layer: "top", showSolderPaste: true },
  { name: "usb-charger", layer: "top", viewport: { minX: -24, minY: -32, maxX: 4, maxY: -18 } },
  {
    name: "amplifier-regulator",
    layer: "top",
    viewport: { minX: -24, minY: -20, maxX: 1, maxY: 5 },
  },
  { name: "microphones", layer: "top", viewport: { minX: 7, minY: -32, maxX: 24, maxY: -6 } },
  {
    name: "display-backlight",
    layer: "top",
    viewport: { minX: -3, minY: -26, maxX: 24, maxY: 20 },
  },
]
for (const { name, ...options } of views) {
  const svg = convertCircuitJsonToPcbSvg(circuitJson, { ...common, ...options })
  writeFileSync(join(outputDirectory, `${name}.svg`), svg)
  await sharp(Buffer.from(svg))
    .png()
    .toFile(join(outputDirectory, `${name}.png`))
}
await sharp({ create: { width: 2000, height: 2600, channels: 4, background: "#ffffff" } })
  .composite(
    ["top", "inner1", "inner2", "bottom"].map((layer, index) => ({
      input: join(outputDirectory, `${layer}.png`),
      left: (index % 2) * 1000,
      top: Math.floor(index / 2) * 1300,
    })),
  )
  .png()
  .toFile(join(outputDirectory, "four-layer-review.png"))
console.log(
  JSON.stringify({
    source_circuit_json: circuitPath,
    views: views.map(({ name }) => name),
    fabrication_approval_inferred: false,
  }),
)
