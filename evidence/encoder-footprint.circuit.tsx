import { EC11E15244G1 } from "../imports/EC11E15244G1/EC11E15244G1"

// Isolated component geometry review; not the handheld board or fabrication package.
export default function EncoderFootprintReview() {
  return (
    <board width="25mm" height="25mm" routingDisabled>
      <schematicsheet
        name="encoder-footprint-review"
        displayName="C370970 corrected footprint review"
        sheetIndex={1}
        sheetSize="A4"
      >
        <EC11E15244G1 name="ENC1" />
      </schematicsheet>
    </board>
  )
}
