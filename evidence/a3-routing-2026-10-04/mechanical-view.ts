import * as THREE from "three"
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js"
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js"

// Engineering assembly envelopes, not electronic component definitions.
// Coordinates are PCB x/y and height z, in millimetres; native GLB uses -x,z,y.
const scene = new THREE.Scene()
scene.background = new THREE.Color("#e8edf1")
const camera = new THREE.PerspectiveCamera(35, innerWidth / innerHeight, 0.1, 1000)
camera.position.set(90, 85, -100)
const renderer = new THREE.WebGLRenderer({ antialias: true })
renderer.setSize(innerWidth, innerHeight)
renderer.setPixelRatio(devicePixelRatio)
document.body.append(renderer.domElement)
const controls = new OrbitControls(camera, renderer.domElement)
controls.target.set(0, 0, 0)
scene.add(new THREE.HemisphereLight(0xffffff, 0x607080, 2.5))
const sunlight = new THREE.DirectionalLight(0xffffff, 3)
sunlight.position.set(30, 100, -40)
scene.add(sunlight)
const assembly = new THREE.Group()
scene.add(assembly)
const nativeBoard = new THREE.Group()
assembly.add(nativeBoard)
new GLTFLoader().load("./buydisplay/board.glb", (gltf) => nativeBoard.add(gltf.scene))

function box(envelope: { name: string; x: number; y: number; z: number; width: number; height: number; depth: number; color: string; opacity?: number }) {
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(envelope.width, envelope.depth, envelope.height), new THREE.MeshStandardMaterial({ color: envelope.color, transparent: true, opacity: envelope.opacity ?? .65, depthWrite: false }))
  mesh.position.set(-envelope.x, envelope.z, envelope.y)
  mesh.name = envelope.name
  assembly.add(mesh)
  const edges = new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry), new THREE.LineBasicMaterial({ color: envelope.color }))
  edges.position.copy(mesh.position)
  assembly.add(edges)
  return mesh
}
const display = box({ name: "BuyDisplay ER-TFT022-1 no-touch glass — nominal raised position", x: -.5, y: -5.225, z: 5.25, width: 54.36, height: 40.3, depth: 2.3, color: "#00a4c8", opacity: .35 })
const battery = box({ name: "AKY2945 including conditional 10% swelling", x: 0, y: -8, z: -4.235, width: 52.5, height: 35, depth: 6.27, color: "#ca9900", opacity: .55 })
box({ name: "maximum external enclosure 60x75x15 maximum", x: 0, y: 3.5, z: -.37, width: 60, height: 75, depth: 15, color: "#708090", opacity: .035 })
box({ name: "antenna all-height exclusion", x: -12, y: 35.675, z: -.56, width: 20, height: 8, depth: 15, color: "#ff3030", opacity: .2 })
box({ name: "slim external speaker candidate / not procurement approved", x: 19.5, y: 18, z: -2.6, width: 11, height: 15, depth: 3, color: "#505050" })
box({ name: "external coin motor envelope", x: 19.5, y: 31, z: -2.425, width: 7, height: 7, depth: 2.65, color: "#8855aa" })
for (const [x,y] of [[2,13],[-21.5,-29.5]]) {
  const boss = new THREE.Mesh(new THREE.CylinderGeometry(3,3,6.57,32),new THREE.MeshStandardMaterial({color:"#cccccc",transparent:true,opacity:.7}))
  boss.position.set(-x,-4.085,y)
  assembly.add(boss)
  box({name:"nylon M2 head envelope",x,y,z:1.55,width:4,height:4,depth:1.5,color:"#ffffff"})
}

// Cable routing space only: no fabricated bend-radius or path qualification.
// The actual factory flex outline and COF/stiffened regions require assembly confirmation.
box({name:"FPC fold planning space — not a proved cable path",x:20.55,y:-5.225,z:3.65,width:17.3,height:40.3,depth:3.1,color:"#f27b00",opacity:.09})
const activeArea=box({name:"ER-TFT022-1 active area",x:-2.31,y:-5.225,z:6.415,width:44.64,height:33.48,depth:.025,color:"#064e68",opacity:.9})
box({name:"TALK plastic actuator corridor",x:19,y:35.7,z:2.6,width:4,height:10.6,depth:2,color:"#3870c0",opacity:.4})
for(const x of [-16.4,21]) box({name:"microphone rear acoustic corridor",x,y:-30.7,z:-2,width:1.5,height:6.6,depth:2.4,color:"#1b9d60",opacity:.5})
box({name:"speaker / motor harness corridor",x:27,y:19,z:-2,width:2,height:30,depth:2,color:"#408030",opacity:.4})

document.querySelector<HTMLButtonElement>("#display")?.addEventListener("click",()=>{display.visible=!display.visible;activeArea.visible=display.visible})
document.querySelector<HTMLButtonElement>("#battery")?.addEventListener("click",()=>battery.visible=!battery.visible)
document.querySelector<HTMLButtonElement>("#top")?.addEventListener("click",()=>{camera.position.set(0,125,.001);controls.update()})
document.querySelector<HTMLButtonElement>("#side")?.addEventListener("click",()=>{camera.position.set(120,0,0);controls.update()})
document.querySelector<HTMLButtonElement>("#bottom")?.addEventListener("click",()=>{camera.position.set(0,-125,.001);controls.update()})
window.addEventListener("resize",()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight)})
renderer.setAnimationLoop(()=>{controls.update();renderer.render(scene,camera)})
