import { EC11E15244G1 } from "../imports/EC11E15244G1/EC11E15244G1"

// Schematic-only component review; not a board design or fabrication artifact.
export default function EncoderChipBoxReview() {
  return (
    <board width="25mm" height="25mm" routingDisabled>
      <schematicsheet
        name="encoder-symbol-review"
        displayName="C370970 native chip-box review"
        sheetIndex={1}
        sheetSize="A4"
      >
        <EC11E15244G1 name="ENC1" />
      </schematicsheet>
    </board>
  )
}
