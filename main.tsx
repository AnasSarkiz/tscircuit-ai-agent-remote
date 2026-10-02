// The PCB build is blocked until the required imported encoder is qualified.
// No fabricated schematic, placement, copper or export is returned by this scaffold.
export default function AiAgentRemote() {
  throw new Error(
    "A0 BLOCKED: C370970 EC11E15244G1 imported terminal holes are 1.30 mm and mounting slots are 3.20 mm long; ALPS specifies 1.00-1.10 mm holes and 2.60-2.70 mm slots. See VALIDATION.md. No complete board or routes exist.",
  )
}
