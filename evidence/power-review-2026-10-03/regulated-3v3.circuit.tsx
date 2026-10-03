import { Regulated3v3ReviewSheet } from "../../src/power/regulated-3v3"

// Component application review only; not the handheld or a fabrication export.
export default function Regulated3v3Review() {
  return (
    <board width="24mm" height="24mm" routingDisabled>
      <Regulated3v3ReviewSheet />
    </board>
  )
}
