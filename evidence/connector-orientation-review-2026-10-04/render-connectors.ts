import { renderGLTFToPNGFromGLB } from "poppygl"

const phase = Bun.argv[2]
if (phase !== "before" && phase !== "after") throw new Error("Expected before or after")
const directory = `evidence/connector-orientation-review-2026-10-04/${phase}`
const glb = await Bun.file(`${directory}/board.glb`).arrayBuffer()
const views: {
  name: string
  camPos: [number, number, number]
  lookAt: [number, number, number]
}[] = [
  { name: "board-top", camPos: [50, 85, -57], lookAt: [0, 0, 0] },
  { name: "board-opposite", camPos: [-50, 85, 57], lookAt: [0, 0, 0] },
  { name: "usb-bottom-edge", camPos: [0, 13, -52], lookAt: [0, 2, -28] },
  { name: "battery-right-edge", camPos: [-44, 16, 9], lookAt: [-20, 3, 9] },
  { name: "speaker-left-edge", camPos: [44, 16, -8], lookAt: [19, 3, -8] },
  { name: "motor-right-edge", camPos: [-44, 16, -7], lookAt: [-20, 3, -7] },
  { name: "service-right-edge", camPos: [-43, 15, 22], lookAt: [-18, 2, 22] },
  { name: "display-ribbon", camPos: [-5, 40, -4], lookAt: [-5, 2, -6] },
]
for (const view of views) {
  const png = await renderGLTFToPNGFromGLB(glb, {
    camPos: view.camPos,
    lookAt: view.lookAt,
    fov: 50,
    width: 1000,
    height: 850,
    supersampling: 2,
    backgroundColor: "#f1f4f8",
    grid: false,
  })
  await Bun.write(`${directory}/${view.name}.png`, png)
  console.log(`Rendered ${phase}/${view.name}`)
}
