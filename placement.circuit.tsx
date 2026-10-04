import AiAgentRemote from "./main"

// Same board/components/connections; no saved route replay, explicit copper paths or pour.
export default function PlacementReview() {
  return <AiAgentRemote placementOnly />
}
