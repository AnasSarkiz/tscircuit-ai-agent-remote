import { ComponentGuides } from "./src/board/ComponentNotes"
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
import { ManualSignalPaths } from "./src/board/ManualSignalPaths"
import { ManualPowerCopper } from "./src/board/ManualPowerCopper"
import { ManualConnectionCopper } from "./src/board/ManualConnectionCopper"
import { viaHoleDiameterMm, viaPadDiameterMm } from "./src/board/viaGeometry"

// A7: frozen 50x65x1.0 mm placement; native routing in progress. NOT FOR FABRICATION.
export default function AiAgentRemote({ placementOnly = false }: { placementOnly?: boolean } = {}) {
  return (
    <board
      routingDisabled={placementOnly}
      routeRemaining={false}
      width={50}
      height={65}
      borderRadius={3}
      thickness={1.0}
      layers={4}
      allowBlindAndBuriedVias={false}
      autorouterEffortLevel="1x"
      autorouterVersion="beta_pipeline9"
      autorouter={{ preset: "auto_local", allowViaInPad: false, traceClearance: 0.2 }}
      pcbStyle={{
        silkscreenFontSize: 0.7,
        viaHoleDiameter: viaHoleDiameterMm,
        viaPadDiameter: viaPadDiameterMm,
      }}
    >
      <BoardNets placementOnly={placementOnly} />
      <BoardRouting placementOnly={placementOnly} />
      <McuUsbSheet placementOnly={placementOnly} />
      <ChargerSheet placementOnly={placementOnly} />
      <RegulatorSheet placementOnly={placementOnly} />
      <DisplaySheet placementOnly={placementOnly} />
      <SpeakerSheet placementOnly={placementOnly} />
      <HapticSheet placementOnly={placementOnly} />
      <MicrophoneClockSheet placementOnly={placementOnly} />
      <HoldSheet placementOnly={placementOnly} />
      <BatteryReadySheet placementOnly={placementOnly} />
      <MicrophonesSheet placementOnly={placementOnly} />
      <ControlsSheet placementOnly={placementOnly} />
      <BacklightSheet placementOnly={placementOnly} />
      <BoardFeatures />
      <ManualSignalPaths placementOnly={placementOnly} />
      <ManualPowerCopper placementOnly={placementOnly} />
      <ManualConnectionCopper placementOnly={placementOnly} />
      <ComponentGuides />
    </board>
  )
}
