import { readFileSync, writeFileSync } from "node:fs"
import { convertCircuitJsonToPcbSvg, convertCircuitJsonToSchematicSvg } from "circuit-to-svg"
import { Resvg } from "@resvg/resvg-js"
import type { AnyCircuitElement } from "circuit-json"
const directory = "evidence/a6-bom-routing-2026-10-04"
const json = JSON.parse(readFileSync("dist/index/circuit.json", "utf8")) as AnyCircuitElement[]
function save(name: string, svg: string) {
  writeFileSync(`${directory}/${name}.svg`, svg)
  writeFileSync(`${directory}/${name}.png`, new Resvg(svg).render().asPng())
}
for (const layer of ["top", "inner1", "inner2", "bottom"] as const) save(`copper-${layer}`, convertCircuitJsonToPcbSvg(json, {layer, width: 1200, height: 1560, shouldDrawErrors: true, showCourtyards: true, showSolderMask: false, shouldDrawRatsNest: false}))
save("paste-top", convertCircuitJsonToPcbSvg(json, {layer:"top", width:1200,height:1560,showSolderPaste:true,showSolderMask:false,shouldDrawRatsNest:false}))
for (const sheet of json.filter(x=>x.type === "schematic_sheet")) if (sheet.type === "schematic_sheet") save(`sheet-${sheet.name}`, convertCircuitJsonToSchematicSvg(json,{schematicSheetId:sheet.schematic_sheet_id}))
for (const [name,viewport] of Object.entries({amplifier:{minX:-24,minY:-4,maxX:-3,maxY:11},backlight:{minX:1,minY:16,maxX:16,maxY:26},charger:{minX:-18,minY:-32,maxX:-1,maxY:-20},usb:{minX:-5,minY:-32,maxX:5,maxY:-21}})) save(`detail-${name}`, convertCircuitJsonToPcbSvg(json,{layer:"top",viewport,width:1400,height:1000,showSolderMask:false,shouldDrawRatsNest:false,showPinNumbers:true,shouldDrawErrors:true,showCourtyards:true}))
