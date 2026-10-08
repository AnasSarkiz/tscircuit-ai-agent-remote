import { readFileSync, writeFileSync } from "node:fs"
import { convertCircuitJsonToPcbSvg } from "circuit-to-svg"
import sharp from "sharp"
const circuitJson=JSON.parse(readFileSync("dist/index/circuit.json","utf8"))
const output="evidence/microphone-local-bypass-2026-10-08/rendered/local-bypass"
const svg=convertCircuitJsonToPcbSvg(circuitJson,{width:1400,height:1300,layer:"top",viewport:{minX:14.5,minY:-32.5,maxX:22,maxY:-25.5},shouldDrawErrors:true,shouldDrawWarnings:true,showErrorsInTextOverlay:false,showPinNumbers:true})
writeFileSync(output+".svg",svg)
await sharp(Buffer.from(svg)).png().toFile(output+".png")
