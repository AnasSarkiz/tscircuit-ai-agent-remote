import { any_circuit_element } from "circuit-json"
import { createHash } from "node:crypto"
const elements: Array<{type:string;[key:string]:unknown}> = await Bun.file("dist/index/circuit.json").json()
const strictFailures=elements.flatMap((element,index)=>{
 const result=any_circuit_element.safeParse(element)
 return result.success?[]:[{index,type:element.type,issues:result.error.issues.map(issue=>({path:issue.path,code:issue.code,message:issue.message}))}]
})
const components=elements.filter(element=>element.type === "source_component")
const summary={milestone:"A1 integrated placement preview",parent_commit:"98a3f7ece77d3b15d92cd21fcf333ff5c951a2e4",dimensions_mm:[50,65],thickness_mm:1.6,layers:4,physical_component_count:130,imported_electronic_components:122,native_copper_test_pads:8,schematic_sheets:elements.filter(element=>element.type === "schematic_sheet").length,pcb_traces:elements.filter(element=>element.type === "pcb_trace").length,pcb_vias:elements.filter(element=>element.type === "pcb_via").length,native_errors:elements.filter(element=>element.type.includes("error")),strict_schema_failure_count:strictFailures.length,fabrication_ready:false,routing_enabled:false,circuit_json_sha256:createHash("sha256").update(new Uint8Array(await Bun.file("dist/index/circuit.json").arrayBuffer())).digest("hex")}
await Bun.write("evidence/integrated-preview-2026-10-03/preview-summary.json",JSON.stringify(summary,null,2))
await Bun.write("evidence/integrated-preview-2026-10-03/strict-schema-failures-summary.json",JSON.stringify(strictFailures,null,2))
const lines=["# A1 integrated preview inventory","","Derived directly from the native full-board Circuit JSON. **Not an assembler BOM release.** Native fabrication CSV/MPN qualification remains B-015.","","122 genuine imported electronic parts plus 8 native copper pads. Stock/rating/footprint qualification remains provisional.","","| Ref | Manufacturer part number | Exact JLC code |","|---|---|---|"]
for(const component of components){
 const codes=component.supplier_part_numbers
 let code="Native copper feature"
 if(typeof codes === "object" && codes !== null && "jlcpcb" in codes && Array.isArray(codes.jlcpcb)) code=codes.jlcpcb.join(", ")
 lines.push(`| ${component.name} | ${component.manufacturer_part_number ?? "Native test pad"} | ${code} |`)
}
await Bun.write("BOM-preview.md",lines.join("\n")+"\n")
console.log(JSON.stringify(summary,null,2))
