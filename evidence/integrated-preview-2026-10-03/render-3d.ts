import { getBestCameraPosition } from "circuit-json-to-gltf"
import { renderGLTFToPNGFromGLB } from "poppygl"
import type { CircuitJson } from "circuit-json"

const circuitJson: CircuitJson = await Bun.file("dist/index/circuit.json").json()
const renderCircuitJson = circuitJson
const glb = await Bun.file("dist/index/3d.glb").arrayBuffer()
await Bun.write("evidence/integrated-preview-2026-10-03/board.glb",glb)
const camera = getBestCameraPosition(renderCircuitJson)
const distance = Math.hypot(...camera.camPos.map((position,index) => position-camera.lookAt[index]))
const directionScale = distance/Math.hypot(0.5,1,0.65)
for(const view of ["top","bottom"] as const) {
 const sign=view === "top" ? 1 : -1
 const camPos: [number,number,number]=[camera.lookAt[0]+0.5*directionScale,camera.lookAt[1]+sign*directionScale,camera.lookAt[2]-0.65*directionScale]
 const image = await renderGLTFToPNGFromGLB(glb,{camPos,lookAt:camera.lookAt,fov:camera.fov,width:1200,height:1200,supersampling:2,backgroundColor:"#f1f4f8",grid:false})
 await Bun.write(`evidence/integrated-preview-2026-10-03/3d-${view}.png`,image)
 console.log(`Rendered actual GLB ${view} view`)
}
