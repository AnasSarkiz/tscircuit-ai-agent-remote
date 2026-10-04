import { readFileSync, writeFileSync } from "node:fs"
import { createHash } from "node:crypto"
import { any_circuit_element } from "circuit-json"
import { z } from "zod"
const sourcePath="dist/index/circuit.json"
const bytes=readFileSync(sourcePath)
const elements=z.array(z.object({type:z.string()}).passthrough()).parse(JSON.parse(bytes.toString()))
const counts: Record<string,number>={}
const schemaFailures=[]
for(const element of elements){
 counts[element.type]=(counts[element.type]??0)+1
 const parsed=any_circuit_element.safeParse(element)
 if(!parsed.success) schemaFailures.push({type:element.type,issues:parsed.error.issues.map(issue=>({path:issue.path,code:issue.code}))})
}
const sourceComponents=z.array(z.object({source_component_id:z.string(),name:z.string()})).parse(elements.filter(e=>e.type==='source_component'))
function getComponentName(sourceComponentId: unknown): string | undefined {
 return sourceComponents.find(component=>component.source_component_id===sourceComponentId)?.name
}
interface NativeBounds { type: string; name: string | undefined; left: number; right: number; bottom: number; top: number }
const bounds: NativeBounds[]=[]
for(const element of elements){
 if(element.type==='pcb_component'||element.type==='pcb_courtyard_rect'){
  const rect=z.object({center:z.object({x:z.number(),y:z.number()}),width:z.number(),height:z.number()}).parse(element)
  bounds.push({type:element.type,name:getComponentName(element.source_component_id),left:rect.center.x-rect.width/2,right:rect.center.x+rect.width/2,bottom:rect.center.y-rect.height/2,top:rect.center.y+rect.height/2})
 } else if(element.type==='pcb_courtyard_outline'){
  const outline=z.array(z.object({x:z.number(),y:z.number()})).parse(element.outline)
  const component=elements.find(e=>e.type==='pcb_component'&&e.pcb_component_id===element.pcb_component_id)
  bounds.push({type:element.type,name:getComponentName(component?.source_component_id),left:Math.min(...outline.map(p=>p.x)),right:Math.max(...outline.map(p=>p.x)),bottom:Math.min(...outline.map(p=>p.y)),top:Math.max(...outline.map(p=>p.y))})
 }
}
const mounts=[{x:-21.5,y:6.7},{x:-21.5,y:-29.5}].map(mount=>{
 const nearby=bounds.map(rect=>({...rect,keepoutGapMillimeters:Math.hypot(Math.max(rect.left-mount.x,0,mount.x-rect.right),Math.max(rect.bottom-mount.y,0,mount.y-rect.top))-3})).sort((a,b)=>a.keepoutGapMillimeters-b.keepoutGapMillimeters)
 return {...mount,holeDiameterMillimeters:2.2,keepoutDiameterMillimeters:6,straightEdgeCentreDistanceMillimeters:Math.min(25-Math.abs(mount.x),32.5-Math.abs(mount.y)),npthEdgeDistanceMillimeters:Math.min(25-Math.abs(mount.x),32.5-Math.abs(mount.y))-1.1,nearestNativeBounds:nearby.slice(0,8),displayKeepoutGapMillimeters:Math.hypot(Math.max(-18.1-mount.x,0,mount.x-18.1),Math.max(-26.9-mount.y,0,mount.y-24.9))-3,batteryKeepoutGapMillimeters:Math.hypot(Math.max(-17.5-mount.x,0,mount.x-17.5),Math.max(-27.25-mount.y,0,mount.y-25.25))-3,antennaKeepoutGapMillimeters:Math.hypot(Math.max(-21-mount.x,0,mount.x+3),Math.max(28.76-mount.y,0,mount.y-36.25))-3}
})
const record={sha256:createHash('sha256').update(bytes).digest('hex'),counts,schemaFailureCount:schemaFailures.length,schemaFailureTypes:schemaFailures.reduce<Record<string,number>>((acc,e)=>{acc[e.type]=(acc[e.type]??0)+1;return acc},{}),mounts,nativeErrors:elements.filter(e=>e.type.includes('error')),notes:['Bounding-box mounting clearance is conservative; no mechanical Z or enclosure fit approval','Display36.2x51.8 and pack35x52.5 trial centre(0,-1); actual pack procurement/harness remains pending','Antenna body bounds are manufacturer mechanical-study nominal shifted to current U1 origin; actual enclosure metal keepout must be reviewed','All output bytes remain native; schema failures retained without rewriting']}
writeFileSync('evidence/routing-intake-2026-10-04/native-analysis.json',JSON.stringify(record,null,2)+'\n')
writeFileSync('evidence/routing-intake-2026-10-04/schema-failures-summary.json',JSON.stringify(schemaFailures,null,2)+'\n')
console.log(JSON.stringify({counts,schemaFailureCount:schemaFailures.length,mounts},null,2))
