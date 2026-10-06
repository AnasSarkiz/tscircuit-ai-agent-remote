import { readdirSync } from "node:fs"
import sharp from "sharp"
const root = "evidence/six-point-board-review-2026-10-06/final-schematics"
const files = readdirSync(root).filter(name => name.endsWith(".png")).sort()
for (const [name, list] of [["circuits-1-7", files.slice(0, 7)], ["circuits-8-13", files.slice(7, 13)], ["guides-14-20", files.slice(13, 20)], ["guides-21-26", files.slice(20)]]) {
  const inputs = []
  for (const [index, file] of list.entries()) {
    inputs.push({ input: await sharp(`${root}/${file}`).resize(800, 500).png().toBuffer(), left: (index % 2) * 800, top: Math.floor(index / 2) * 500 })
  }
  await sharp({ create: { width: 1600, height: Math.ceil(list.length / 2) * 500, channels: 4, background: "white" } }).composite(inputs).png().toFile(`${root}/${name}-contact.png`)
}
