import { BoardRouting } from "./src/board/Routing"
import { BoardNets } from "./src/board/nets"
import { McuUsbSheet } from "./src/board/McuUsbSheet"
import { ChargerSheet } from "./src/board/ChargerSheet"
import { RegulatorSheet } from "./src/board/RegulatorSheet"
import { DisplaySheet } from "./src/board/DisplaySheet"
import { SpeakerSheet } from "./src/board/SpeakerSheet"
import { HapticSheet } from "./src/board/HapticSheet"
import { MicrophoneClockSheet } from "./src/board/MicrophoneClockSheet"
import { HoldSheet } from "./src/board/HoldSheet"
import { BatteryReadySheet } from "./src/board/BatteryReadySheet"
import { MicrophonesSheet } from "./src/board/MicrophonesSheet"
import { ControlsSheet } from "./src/board/ControlsSheet"
import { BacklightSheet } from "./src/board/BacklightSheet"
import { BoardFeatures } from "./src/board/BoardFeatures"

// A4: 82.7% provisional BuyDisplay coverage trial and partial native copper; remaining routing is incomplete. NOT FOR FABRICATION.
export default function AiAgentRemote({ placementOnly = false }: { placementOnly?: boolean } = {}) {
  return (
    <board
      routingDisabled={placementOnly}
      routeRemaining={false}
      width={50}
      height={65}
      borderRadius={3}
      thickness={0.8}
      layers={4}
      autorouter={{ preset: "auto_local", allowViaInPad: false, traceClearance: 0.2 }}
      pcbStyle={{ silkscreenFontSize: 0.7 }}
    >
      <BoardNets />
      <BoardRouting placementOnly={placementOnly} />
      <McuUsbSheet placementOnly={placementOnly} />
      <ChargerSheet />
      <RegulatorSheet />
      <DisplaySheet />
      <SpeakerSheet />
      <HapticSheet />
      <MicrophoneClockSheet />
      <HoldSheet />
      <BatteryReadySheet />
      <MicrophonesSheet />
      <ControlsSheet />
      <BacklightSheet />
      <BoardFeatures />
    </board>
  )
}
