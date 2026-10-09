import { RootCircuit } from "@tscircuit/core"
import { getPlatformConfig } from "@tscircuit/eval"
import { plugin } from "bun"
import { relative } from "node:path"
import { Esp32S3UsbReviewSheet } from "../../src/mcu/esp32-s3-usb-review"

// The existing diagnostic is intentionally unrouted. Set the documented root
// platform control, as scripts/routing/capture-placement.tsx already does.
plugin({
  name: "diagnostic-genuine-asset-paths",
  setup(builder) {
    builder.onLoad({ filter: /\.(obj|step)$/ }, ({ path }) => ({
      contents: `export default ${JSON.stringify(`./${relative(process.cwd(), path)}`)}`,
      loader: "js",
    }))
  },
})
const root = new RootCircuit({ platform: { ...getPlatformConfig(), routingDisabled: true } })
const routingEvents: object[] = []
root.on("autorouting:start", event => routingEvents.push(event))
root.add(<board width={60} height={50} routingDisabled><Esp32S3UsbReviewSheet /></board>)
await root.renderUntilSettled()
const native = root.getCircuitJson()
const copper = native.filter(element => ["pcb_trace", "pcb_via", "pcb_copper_pour"].includes(element.type))
console.log(JSON.stringify({ routingEventCount: routingEvents.length, copperCount: copper.length, rootRoutingDisabled: root.pcbRoutingDisabled, platformRoutingDisabled: root.platform?.routingDisabled }))
if (routingEvents.length || copper.length) throw Error("The diagnostic must not start routing or emit copper")
await Bun.write("evidence/pcb-completion-2026-10-08/diagnostic-native/mcu-usb/circuit.json", JSON.stringify(native, null, 2))
await Bun.write("evidence/pcb-completion-2026-10-08/diagnostic-native/mcu-usb/events.json", JSON.stringify({ routingEvents, copperCount: copper.length, rootRoutingDisabled: root.pcbRoutingDisabled, platformRoutingDisabled: root.platform?.routingDisabled }, null, 2))
