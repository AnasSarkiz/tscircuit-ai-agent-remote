import { ICS_43434 } from "../imports/ICS_43434/ICS_43434"

// Isolated geometry/connectivity review; not the handheld board or fabrication output.
export default function MicrophoneLocalCorrectionReview() {
  return (
    <board width="10mm" height="10mm" routingDisabled>
      <schematicsheet
        name="microphone-local-correction-review"
        displayName="C5656610 user-authorized acoustic opening review"
        sheetIndex={1}
        sheetSize="A4"
      >
        <net name="GND" isGroundNet />
        <net name="MIC_VDD" isPowerNet />
        <ICS_43434 name="MIC1" layer="top" />
        <trace from="MIC1.pin3" to="net.GND" />
        <trace from="MIC1.pin5" to="net.MIC_VDD" />
      </schematicsheet>
    </board>
  )
}
