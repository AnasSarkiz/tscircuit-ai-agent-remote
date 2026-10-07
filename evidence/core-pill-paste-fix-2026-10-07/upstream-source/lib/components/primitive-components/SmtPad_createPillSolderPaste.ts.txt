import type { PcbSmtPadPill, PcbSmtPadRotatedPill } from "circuit-json"
import type { SmtPad } from "./SmtPad"

/**
 * Copy the emitted pad's board-world point and CCW orientation in mm (+X right,
 * +Y top, right-handed +Z above). The pad already includes placement and layer
 * reflection; paste must use that same geometry rather than transform it again.
 */
export function SmtPad_createPillSolderPaste(
  smtPad: SmtPad,
  pcb_smtpad: PcbSmtPadPill | PcbSmtPadRotatedPill,
) {
  const { coveredWithSolderMask, solderPasteMargin } = smtPad._parsedProps
  if (coveredWithSolderMask) return

  const width =
    solderPasteMargin === undefined
      ? pcb_smtpad.width * 0.7
      : Math.max(pcb_smtpad.width + 2 * solderPasteMargin, 0)
  const height =
    solderPasteMargin === undefined
      ? pcb_smtpad.height * 0.7
      : Math.max(pcb_smtpad.height + 2 * solderPasteMargin, 0)
  if (width === 0 || height === 0) return

  const radius = Math.min(
    width / 2,
    height / 2,
    solderPasteMargin === undefined
      ? pcb_smtpad.radius * 0.7
      : Math.max(pcb_smtpad.radius + solderPasteMargin, 0),
  )
  smtPad.root!.db.pcb_solder_paste.insert({
    ...(pcb_smtpad.shape === "rotated_pill"
      ? {
          shape: "rotated_pill" as const,
          ccw_rotation: pcb_smtpad.ccw_rotation,
        }
      : { shape: "pill" as const }),
    width,
    height,
    radius,
    x: pcb_smtpad.x,
    y: pcb_smtpad.y,
    layer: pcb_smtpad.layer,
    pcb_smtpad_id: pcb_smtpad.pcb_smtpad_id,
    pcb_component_id: pcb_smtpad.pcb_component_id,
    pcb_group_id: pcb_smtpad.pcb_group_id,
    subcircuit_id: pcb_smtpad.subcircuit_id,
  })
}
