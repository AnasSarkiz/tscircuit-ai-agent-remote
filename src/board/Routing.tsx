import { fanoutTracePath } from "@tscircuit/props"
import regulatorPaths from "../../routes/a3/regulator.json"

const routingTolerances = {
  minTraceWidth: 0.2,
  minTraceToPadEdgeClearance: 0.2,
  minTraceToHoleEdgeClearance: 0.25,
  minPadEdgeToPadEdgeClearance: 0.1,
  minBoardEdgeClearance: 0.25,
  minViaEdgeToPadEdgeClearance: 0.2,
  minViaHoleDiameter: 0.3,
  minViaPadDiameter: 0.7,
} as const

// Native phases. Their original events/paths must be preserved before edits.
export function BoardRouting({ placementOnly = false }: { placementOnly?: boolean } = {}) {
  return (
    <>
      {!placementOnly && (
        <>
          <copperpour
            name="L2_GND"
            layer="inner1"
            connectsTo="net.GND"
            unbroken
            clearance={0.2}
            boardEdgeMargin={0.25}
            cutoutMargin={0.25}
            useThermalReliefs={false}
          />

          <autoroutingphase
            name="regulator-switching"
            phaseIndex={0}
            pcbTracePaths={fanoutTracePath.array().parse(regulatorPaths)}
            autorouter={{ preset: "auto_local", allowViaInPad: false, traceClearance: 0.2 }}
            {...routingTolerances}
          />
        </>
      )}

      <differentialpair
        name="USB_MCU"
        positiveConnection=".U1 > .pin14"
        negativeConnection=".U1 > .pin13"
        maxLengthSkew={0.5}
        targetDifferentialImpedance={90}
        pcbTraceGap={0.1999}
        maxUncoupledLength={5}
      />
      <differentialpair
        name="SPEAKER_OUTPUT"
        positiveConnection=".J4 > .pin1"
        negativeConnection=".J4 > .pin2"
        maxLengthSkew={2}
        pcbTraceGap={0.2}
        maxUncoupledLength={5}
      />
    </>
  )
}
