import { convertCircuitJsonToPcbSvg, convertCircuitJsonToSchematicSvg } from "circuit-to-svg"
import { Resvg } from "@resvg/resvg-js"
import type { CircuitJson } from "circuit-json"
const circuitJson: CircuitJson = await Bun.file("dist/index/circuit.json").json()
const directory="evidence/connector-orientation-review-2026-10-04/after"
for(const ratsnest of [false,true]){
 const svg=convertCircuitJsonToPcbSvg(circuitJson,{width:1400,height:1700,layer:"top",shouldDrawRatsNest:ratsnest,showCourtyards:true,showPcbNotes:true,backgroundColor:"#101720",showSolderMask:true})
 const basename=ratsnest?"pcb-ratsnest":"pcb-top"
 await Bun.write(`${directory}/${basename}.svg`,svg)
 await Bun.write(`${directory}/${basename}.png`,new Resvg(svg).render().asPng())
}
for(const sheet of circuitJson.filter(element=>element.type === "schematic_sheet")){
 const svg=convertCircuitJsonToSchematicSvg(circuitJson,{width:1684,height:1190,schematicSheetId:sheet.schematic_sheet_id})
 await Bun.write(`${directory}/sheet-${String(sheet.sheet_index).padStart(2,"0")}.svg`,svg)
 await Bun.write(`${directory}/sheet-${String(sheet.sheet_index).padStart(2,"0")}.png`,new Resvg(svg).render().asPng())
}
console.log("Rendered top, ratsnest and every native A4 schematic sheet")
