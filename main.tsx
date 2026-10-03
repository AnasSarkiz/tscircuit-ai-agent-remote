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

// A1: complete, deliberately unrouted placement preview. PROTOTYPE, NOT FOR FABRICATION.
export default function AiAgentRemote() {
  return (
    <board
      width={50}
      height={65}
      borderRadius={3}
      thickness={1.6}
      layers={4}
      routingDisabled
      pcbStyle={{ silkscreenFontSize: 0.7 }}
    >
      <BoardNets />
      <McuUsbSheet />
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
