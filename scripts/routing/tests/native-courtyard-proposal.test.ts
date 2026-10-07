import { expect, test } from "bun:test"
import { getNativeCourtyardProposal } from "../lib/get-native-courtyard-proposal"

const component = [
  { type: "source_component", source_component_id: "source_component_0", name: "J7" },
  {
    type: "pcb_component",
    source_component_id: "source_component_0",
    pcb_component_id: "pcb_component_0",
    center: { x: 4, y: 2 },
    rotation: 0,
  },
]

test("polygon courtyard moves around its component anchor", () => {
  const proposal = getNativeCourtyardProposal({
    nativeInput: [
      ...component,
      {
        type: "pcb_courtyard_polygon",
        pcb_component_id: "pcb_component_0",
        outline: [
          { x: 3, y: 1.5 },
          { x: 5, y: 1.5 },
          { x: 5, y: 2.5 },
        ],
      },
    ],
    poseInput: { J7: { pcbX: 1, pcbY: -3, pcbRotation: 90 } },
  })
  const expected = [
    { x: 1.5, y: -4 },
    { x: 1.5, y: -2 },
    { x: 0.5, y: -2 },
  ]
  proposal.outlines[0].outline.forEach((point, index) => {
    expect(point.x).toBeCloseTo(expected[index].x, 9)
    expect(point.y).toBeCloseTo(expected[index].y, 9)
  })
})

test("rotated rectangle courtyard preserves its own rotation", () => {
  const proposal = getNativeCourtyardProposal({
    nativeInput: [
      ...component,
      {
        type: "pcb_courtyard_rect",
        pcb_component_id: "pcb_component_0",
        center: { x: 4, y: 2 },
        width: 2,
        height: 1,
        rotation: 90,
      },
    ],
    poseInput: { J7: { pcbX: 1, pcbY: -3, pcbRotation: 90 } },
  })
  const expected = [
    { x: 2, y: -2.5 },
    { x: 0, y: -2.5 },
    { x: 0, y: -3.5 },
    { x: 2, y: -3.5 },
  ]
  proposal.outlines[0].outline.forEach((point, index) => {
    expect(point.x).toBeCloseTo(expected[index].x, 9)
    expect(point.y).toBeCloseTo(expected[index].y, 9)
  })
})

test("unsupported native courtyard cannot produce a passing proposal", () => {
  expect(() =>
    getNativeCourtyardProposal({
      nativeInput: [
        ...component,
        { type: "pcb_courtyard_circle", pcb_component_id: "pcb_component_0" },
      ],
      poseInput: {},
    }),
  ).toThrow("Unsupported native courtyard for J7")
})

test("missing native component geometry fails instead of dropping the component", () => {
  expect(() =>
    getNativeCourtyardProposal({
      nativeInput: [component[0], { ...component[1], center: undefined }],
      poseInput: {},
    }),
  ).toThrow("Incomplete native component geometry")
})

test("native via components are identified separately from purchased component courtyards", () => {
  const proposal = getNativeCourtyardProposal({
    nativeInput: [
      ...component,
      {
        type: "source_manually_placed_via",
        source_manually_placed_via_id: "source_manually_placed_via_0",
      },
      {
        type: "pcb_component",
        pcb_component_id: "pcb_component_1",
        source_component_id: "source_manually_placed_via_0",
        center: { x: 8, y: 4 },
        rotation: 0,
      },
    ],
    poseInput: {},
  })
  expect(proposal.outlines).toEqual([])
})
