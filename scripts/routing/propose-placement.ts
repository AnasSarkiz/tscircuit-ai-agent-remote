import { getNativeCourtyardProposal } from "./lib/get-native-courtyard-proposal"

const [nativePath, posePath, outputPath] = Bun.argv.slice(2)
if (!nativePath || !posePath || !outputPath)
  throw new Error("Provide native JSON, pose proposal JSON and output path")
const proposal = getNativeCourtyardProposal({
  nativeInput: await Bun.file(nativePath).json(),
  poseInput: await Bun.file(posePath).json(),
})
await Bun.write(outputPath, JSON.stringify(proposal, null, 2))
console.log(
  JSON.stringify({
    courtyardCount: proposal.outlines.length,
    proposedPartCount: Object.keys(proposal.poses).length,
  }),
)
