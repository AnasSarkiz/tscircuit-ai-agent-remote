import { ICS_43434 } from "./fresh-import/imports/ICS_43434/ICS_43434"

// Diagnostic component-only fixture; not the handheld design or fabrication output.
export default function MicrophoneImportReview() {
  return (
    <board width="10mm" height="10mm" routingDisabled>
      <schematicsheet
        name="microphone-import-review"
        displayName="C5656610 published-import geometry review"
        sheetIndex={1}
        sheetSize="A4"
      >
        <ICS_43434 name="MIC1" layer="top" />
      </schematicsheet>
    </board>
  )
}
