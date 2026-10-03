import { readFileSync } from "node:fs"
import { Resvg } from "@resvg/resvg-js"
import { applyToPoint, compose, scale, toSVG, translate } from "transformation-matrix"
import { z } from "zod"

const folder = "evidence/top-control-mechanical-review-2026-10-03"
const rawElementsSchema = z.array(z.object({ type: z.string() }).passthrough())
const componentSchema = z.object({
  type: z.literal("pcb_component"), source_component_id: z.string(), pcb_component_id: z.string(),
  center: z.object({ x: z.number(), y: z.number() }), rotation: z.number(),
})
const sourceComponentSchema = z.object({
  type: z.literal("source_component"), name: z.string(), source_component_id: z.string(),
})
const padSchema = z.object({
  type: z.literal("pcb_smtpad"), pcb_component_id: z.string(), shape: z.literal("rect"),
  x: z.number(), y: z.number(), width: z.number(), height: z.number(),
})
type Bounds = { left: number; right: number; bottom: number; top: number }

function getPadBounds(params: { filePath: string; name: string; targetX: number; targetY: number }) {
  const elements = rawElementsSchema.parse(JSON.parse(readFileSync(params.filePath, "utf8")))
  const source = sourceComponentSchema.parse(elements.find(
    (element) => element.type === "source_component" && element.name === params.name,
  ))
  const component = componentSchema.parse(elements.find(
    (element) => element.type === "pcb_component" && element.source_component_id === source.source_component_id,
  ))
  if (component.rotation !== 0) throw new Error("This study requires an unrotated native fixture")
  const pads = elements.filter((element) => element.type === "pcb_smtpad" &&
    element.pcb_component_id === component.pcb_component_id).map((element) => padSchema.parse(element))
  if (!pads.length) throw new Error("No native pads")
  const nativeToTrial = compose(translate(params.targetX, params.targetY), translate(-component.center.x, -component.center.y))
  const corners = pads.flatMap((pad) => [
    applyToPoint(nativeToTrial, { x: pad.x - pad.width / 2, y: pad.y - pad.height / 2 }),
    applyToPoint(nativeToTrial, { x: pad.x + pad.width / 2, y: pad.y + pad.height / 2 }),
  ])
  return { count: pads.length, bounds: {
    left: Math.min(...corners.map((point) => point.x)), right: Math.max(...corners.map((point) => point.x)),
    bottom: Math.min(...corners.map((point) => point.y)), top: Math.max(...corners.map((point) => point.y)),
  } }
}

function rectangularDistance(first: Bounds, second: Bounds) {
  return Math.hypot(Math.max(first.left - second.right, second.left - first.right, 0),
    Math.max(first.bottom - second.top, second.bottom - first.top, 0))
}

function renderPanel(params: { moduleX: number; canvasX: number }) {
  const pcbToSvg = compose(translate(params.canvasX, 69), scale(1, -1))
  const moduleOriginY = 22 - 3.775456
  const antenna = { left: params.moduleX - 9, right: params.moduleX + 9, bottom: 27.26, top: 34.75 }
  const display = { left: -16.85, right: 16.85, bottom: -31.5, top: 11.44 }
  const switchBody = { left: 19.5, right: 22.5, bottom: 29.5, top: 31.5 }
  const switchPads = getPadBounds({ filePath: "evidence/hold-control-alternate-review-2026-10-03/circuit.json", name: "SW4", targetX: 21, targetY: 30.5 })
  const modulePads = getPadBounds({ filePath: "evidence/mcu-usb-review-2026-10-03/circuit.json", name: "U1", targetX: params.moduleX, targetY: moduleOriginY })
  const switchEnvelope = { left: Math.min(switchBody.left, switchPads.bounds.left), right: Math.max(switchBody.right, switchPads.bounds.right),
    bottom: Math.min(switchBody.bottom, switchPads.bounds.bottom), top: Math.max(switchBody.top, switchPads.bounds.top) }
  const controlGap = rectangularDistance(antenna, switchEnvelope)
  const modulePadMargin = Math.min(modulePads.bounds.left + 25, 25 - modulePads.bounds.right,
    modulePads.bounds.bottom + 32.5, 32.5 - modulePads.bounds.top)
  const switchPadMargin = Math.min(switchPads.bounds.left + 25, 25 - switchPads.bounds.right,
    switchPads.bounds.bottom + 32.5, 32.5 - switchPads.bounds.top)
  const report = { modulePhysicalCenter: { x: params.moduleX, y: 22 }, moduleNativeOrigin: { x: params.moduleX, y: moduleOriginY },
    switchCenter: { x: 21, y: 30.5 }, antenna, display, switchBody, switchPads, modulePads,
    nominalAntennaToControlGapMillimeters: controlGap, nominalAntennaToDisplayGapMillimeters: rectangularDistance(antenna, display),
    modulePadEdgeMarginMillimeters: modulePadMargin, switchPadEdgeMarginMillimeters: switchPadMargin,
    nominalControlClearanceAtLeast15Millimeters: controlGap >= 15 }
  const geometry = `<g transform="${toSVG(pcbToSvg)}">
    <rect x="-25" y="-32.5" width="50" height="65" fill="#edf6ee" stroke="#23683a" stroke-width=".3"/>
    <rect x="${params.moduleX - 24}" y="12.26" width="48" height="37.49" fill="#fff0c4" fill-opacity=".5" stroke="#b87912" stroke-dasharray="1 1" stroke-width=".3"/>
    <rect x="-16.85" y="-31.5" width="33.7" height="42.94" fill="#c8e6f4" fill-opacity=".8" stroke="#257492" stroke-width=".3"/>
    <rect x="${params.moduleX - 9}" y="9.25" width="18" height="25.5" fill="#bfc2ca" fill-opacity=".65" stroke="#4d5262" stroke-width=".3"/>
    <rect x="${antenna.left}" y="27.26" width="18" height="7.49" fill="#e3b752" stroke="#805510" stroke-width=".3"/>
    <rect x="${switchPads.bounds.left}" y="${switchPads.bounds.bottom}" width="${switchPads.bounds.right - switchPads.bounds.left}" height="${switchPads.bounds.top - switchPads.bounds.bottom}" fill="none" stroke="#bd332d" stroke-width=".25"/>
    <rect x="19.5" y="29.5" width="3" height="2" fill="#e0dae8" stroke="#7c4791" stroke-width=".3"/>
  </g>`
  const labels = [{ x: 0, y: -7, text: "LCD body — raised fit pending" },
    { x: params.moduleX, y: 31, text: "antenna" }, { x: 21, y: 35.5, text: "hold switch candidate" }].map((label) => {
    const point = applyToPoint(pcbToSvg, label)
    return `<text x="${point.x}" y="${point.y}" text-anchor="middle" font-size="1.5">${label.text}</text>`
  }).join("")
  return { report, svg: `<text x="${params.canvasX}" y="7" text-anchor="middle" font-size="2.6" font-weight="bold">Module x=${params.moduleX} mm</text>${geometry}${labels}
    <text x="${params.canvasX}" y="109" text-anchor="middle" font-size="2" fill="${controlGap >= 15 ? "#23683a" : "#b73131"}">Control–antenna: ${controlGap.toFixed(2)} mm nominal</text>
    <text x="${params.canvasX}" y="113" text-anchor="middle" font-size="1.7">LCD–antenna: 15.82 mm nominal</text>` }
}

const panels = [renderPanel({ moduleX: 0, canvasX: 46 }), renderPanel({ moduleX: -8, canvasX: 123 })]
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1700" height="1250" viewBox="0 0 170 125"><rect width="170" height="125" fill="white"/><g font-family="Arial, sans-serif" fill="#22304b">${panels.map((panel) => panel.svg).join("")}
  <text x="85" y="119" text-anchor="middle" font-size="1.8">50 × 65 mm trial; actual imported pad envelopes. No approved PCB placement or enclosure.</text>
  <text x="85" y="123" text-anchor="middle" font-size="1.7">Top-edge actuation, raised LCD, antenna substrate, tolerances, pack and speaker remain unqualified.</text></g></svg>`
await Bun.write(`${folder}/top-control-study.svg`, svg)
await Bun.write(`${folder}/top-control-study.png`, new Resvg(svg).render().asPng())
await Bun.write(`${folder}/nominal-dimensions.json`, JSON.stringify({
  status: "read-only mechanical study, not component definitions or native placement approval",
  boardWidthMillimeters: 50, boardHeightMillimeters: 65, requiredNominalRfGapMillimeters: 15,
  trials: panels.map((panel) => panel.report),
}, null, 2) + "\n")
