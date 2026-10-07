import { applyToPoint, compose, inverse, rotateDEG, translate } from "transformation-matrix"
import { z } from "zod"

const placementElement = z.object({
  type: z.string(),
  source_component_id: z.string().optional(),
  pcb_component_id: z.string().optional(),
  name: z.string().optional(),
  center: z.object({ x: z.number(), y: z.number() }).optional(),
  rotation: z.number().optional(),
  width: z.number().optional(),
  height: z.number().optional(),
  outline: z.array(z.object({ x: z.number(), y: z.number() })).optional(),
})
const proposal = z.record(
  z.string(),
  z.object({ pcbX: z.number(), pcbY: z.number(), pcbRotation: z.number() }),
)

export function getNativeCourtyardProposal({
  nativeInput,
  poseInput,
}: {
  nativeInput: unknown
  poseInput: unknown
}) {
  const nativeElements = z.array(z.object({ type: z.string() }).passthrough()).parse(nativeInput)
  const elements = placementElement
    .array()
    .parse(
      nativeElements.filter(
        (element) =>
          element.type === "source_component" ||
          element.type === "pcb_component" ||
          (element.type.startsWith("pcb_courtyard_") && !element.type.endsWith("error")),
      ),
    )
  const poses = proposal.parse(poseInput)
  const viaSources = z
    .array(z.object({ source_manually_placed_via_id: z.string() }))
    .parse(nativeElements.filter((element) => element.type === "source_manually_placed_via"))
  const viaSourceIds = new Set(viaSources.map((via) => via.source_manually_placed_via_id))
  type SourceComponentId = string
  const names = new Map<SourceComponentId, string>(
    elements.flatMap((element) =>
      element.type === "source_component" && element.source_component_id && element.name
        ? [[element.source_component_id, element.name]]
        : [],
    ),
  )
  const components = elements.filter(
    (element) =>
      element.type === "pcb_component" &&
      (!element.source_component_id || !viaSourceIds.has(element.source_component_id)),
  )
  const courtyards = elements.filter(
    (element) => element.type.startsWith("pcb_courtyard_") && !element.type.endsWith("error"),
  )
  const outlines = components.flatMap((component) => {
    const reference = component.source_component_id
      ? names.get(component.source_component_id)
      : undefined
    if (!reference || !component.center || component.rotation === undefined) {
      throw new Error(`Incomplete native component geometry: ${component.pcb_component_id}`)
    }
    const pose = poses[reference]
    const oldLocalToPcb = compose(
      translate(component.center.x, component.center.y),
      rotateDEG(component.rotation),
    )
    const newLocalToPcb = pose
      ? compose(translate(pose.pcbX, pose.pcbY), rotateDEG(pose.pcbRotation))
      : oldLocalToPcb
    const oldPcbToNewPcb = compose(newLocalToPcb, inverse(oldLocalToPcb))
    return courtyards
      .filter((courtyard) => courtyard.pcb_component_id === component.pcb_component_id)
      .map((courtyard) => {
        let outline = courtyard.outline
        if (!outline && courtyard.center && courtyard.width && courtyard.height) {
          const { x, y } = courtyard.center
          const halfWidth = courtyard.width / 2
          const halfHeight = courtyard.height / 2
          outline = [
            { x: x - halfWidth, y: y - halfHeight },
            { x: x + halfWidth, y: y - halfHeight },
            { x: x + halfWidth, y: y + halfHeight },
            { x: x - halfWidth, y: y + halfHeight },
          ]
          const courtyardLocalToPcb = compose(
            translate(x, y),
            rotateDEG(courtyard.rotation ?? 0),
            translate(-x, -y),
          )
          outline = outline.map((point) => applyToPoint(courtyardLocalToPcb, point))
        }
        if (!outline) throw new Error(`Unsupported native courtyard for ${reference}`)
        return { reference, outline: outline.map((point) => applyToPoint(oldPcbToNewPcb, point)) }
      })
  })
  return { classification: "Native courtyard proposal; full DRC pending", poses, outlines }
}
