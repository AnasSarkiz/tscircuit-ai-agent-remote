import { compose, rotateDEG, translate } from "transformation-matrix"

const poses = JSON.parse(await Bun.stdin.text())
const matrices = Object.fromEntries(
  Object.entries(poses).map(([name, pose]) => [
    name,
    compose(rotateDEG(-pose.rotation), translate(-pose.x, -pose.y)),
  ]),
)
process.stdout.write(JSON.stringify(matrices))
