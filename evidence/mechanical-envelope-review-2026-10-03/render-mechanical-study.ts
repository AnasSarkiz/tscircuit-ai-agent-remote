import { mkdir } from "node:fs/promises"
import { Resvg } from "@resvg/resvg-js"
import { applyToPoint, compose, scale, toSVG, translate } from "transformation-matrix"

const outputDirectory = "evidence/mechanical-envelope-review-2026-10-03"
await mkdir(outputDirectory, { recursive: true })

// Dimension study only. These rectangles are mechanical envelopes, not
// electronic component definitions or a replacement PCB placement.
const displayBodyWidthMillimeters = 33.7
const displayBodyHeightMillimeters = 42.94
const moduleBodyCenterYMillimeters = 22
const moduleBodyHeightMillimeters = 25.5
const antennaHeightMillimeters = 7.49
const antennaBottomYMillimeters = moduleBodyCenterYMillimeters + moduleBodyHeightMillimeters / 2 - antennaHeightMillimeters
const recommendedClearanceMillimeters = 15
const nativeModuleBodyGraphicCenterYMillimeters = (16.5449631 - 8.9940511) / 2
const moduleInstanceYMillimeters = moduleBodyCenterYMillimeters - nativeModuleBodyGraphicCenterYMillimeters
const nativePin1TopYMillimeters = 9.0449527 + 0.8999982 / 2
const requiredLandTopYMillimeters = moduleInstanceYMillimeters + nativePin1TopYMillimeters

function renderPanel(params: { boardHeightMillimeters: number; screenOriginX: number }) {
  const { boardHeightMillimeters, screenOriginX } = params
  const pcbToSvgMatrix = compose(translate(screenOriginX, 61), scale(1, -1))
  const displayBottomYMillimeters = -boardHeightMillimeters / 2 + 1
  const displayTopYMillimeters = displayBottomYMillimeters + displayBodyHeightMillimeters
  const nominalAntennaDisplayGapMillimeters = antennaBottomYMillimeters - displayTopYMillimeters
  const landTopMarginMillimeters = boardHeightMillimeters / 2 - requiredLandTopYMillimeters
  const labels: Array<{ x: number; y: number; text: string; color?: string }> = [
    { x: 0, y: 36, text: "ESP32 body / antenna" },
    { x: 0, y: 31, text: "Antenna" },
    { x: 0, y: 18, text: "Module shield" },
    { x: 0, y: displayBottomYMillimeters + 20, text: "LCD body" },
    { x: 0, y: displayBottomYMillimeters + 16, text: "33.7 × 42.94 mm" },
    { x: 0, y: 44, text: "15 mm RF clearance study" },
  ]
  const geometry = `<g transform="${toSVG(pcbToSvgMatrix)}">
    <rect x="-25" y="${-boardHeightMillimeters / 2}" width="50" height="${boardHeightMillimeters}" rx="2" fill="#ecf6ef" stroke="#23683a" stroke-width="0.35" />
    <rect x="-24" y="${antennaBottomYMillimeters - recommendedClearanceMillimeters}" width="48" height="${antennaHeightMillimeters + 30}" fill="#fff0c4" fill-opacity="0.45" stroke="#b87912" stroke-dasharray="1 1" stroke-width="0.3" />
    <rect x="${-displayBodyWidthMillimeters / 2}" y="${displayBottomYMillimeters}" width="${displayBodyWidthMillimeters}" height="${displayBodyHeightMillimeters}" fill="#c8e6f4" fill-opacity="0.85" stroke="#257492" stroke-width="0.3" />
    <rect x="-9" y="${moduleBodyCenterYMillimeters - moduleBodyHeightMillimeters / 2}" width="18" height="${moduleBodyHeightMillimeters}" fill="#bfc2ca" fill-opacity="0.7" stroke="#4d5262" stroke-width="0.3" />
    <rect x="-9" y="${antennaBottomYMillimeters}" width="18" height="${antennaHeightMillimeters}" fill="#e3b752" stroke="#805510" stroke-width="0.3" />
    <line x1="-23" y1="${requiredLandTopYMillimeters}" x2="23" y2="${requiredLandTopYMillimeters}" stroke="#b73131" stroke-dasharray="1 1" stroke-width="0.3" />
  </g>`
  const texts = labels.map((label) => {
    const point = applyToPoint(pcbToSvgMatrix, { x: label.x, y: label.y })
    return `<text x="${point.x}" y="${point.y}" text-anchor="middle" fill="${label.color ?? "#22304b"}" font-size="1.7">${label.text}</text>`
  }).join("")
  return {
    svg: `${geometry}${texts}<text x="${screenOriginX}" y="6" text-anchor="middle" font-size="2.7" font-weight="bold">50 × ${boardHeightMillimeters} mm PCB trial</text>
      <text x="${screenOriginX}" y="97" text-anchor="middle" font-size="2" fill="${nominalAntennaDisplayGapMillimeters >= 15 && landTopMarginMillimeters >= 0 ? "#23683a" : "#b73131"}">LCD–antenna gap: ${nominalAntennaDisplayGapMillimeters.toFixed(2)} mm</text>
      <text x="${screenOriginX}" y="101" text-anchor="middle" font-size="1.8">Top-pad support margin: ${landTopMarginMillimeters.toFixed(2)} mm</text>`,
    boardHeightMillimeters,
    moduleInstanceYMillimeters,
    displayBottomYMillimeters,
    displayTopYMillimeters,
    nominalAntennaDisplayGapMillimeters,
    landTopMarginMillimeters,
  }
}

const panels = [renderPanel({ boardHeightMillimeters: 50, screenOriginX: 39 }), renderPanel({ boardHeightMillimeters: 65, screenOriginX: 111 })]
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1100" viewBox="0 0 150 110"><rect width="150" height="110" fill="white"/><g font-family="Arial, sans-serif">${panels.map((panel) => panel.svg).join("")}<text x="75" y="104" text-anchor="middle" font-size="1.6">Red dashed line: upper edge of the first native solder land. PCB is green; LCD is blue.</text><text x="75" y="108" text-anchor="middle" font-size="1.7">Nominal study only — raised LCD, antenna substrate clearance and top-button location remain unqualified.</text></g></svg>`
await Bun.write(`${outputDirectory}/envelope-study.svg`, svg)
await Bun.write(`${outputDirectory}/envelope-study.png`, new Resvg(svg).render().asPng())
await Bun.write(`${outputDirectory}/nominal-dimensions.json`, JSON.stringify({
  status: "unqualified nominal envelope study; no native PCB placement or component definitions generated",
  manufacturerClearanceMillimeters: recommendedClearanceMillimeters,
  moduleBodyCenterYMillimeters,
  nativeModuleBodyGraphicCenterYMillimeters,
  requiredLandTopYMillimeters,
  antennaBottomYMillimeters,
  panels: panels.map(({ svg, ...dimensions }) => dimensions),
}, null, 2))
