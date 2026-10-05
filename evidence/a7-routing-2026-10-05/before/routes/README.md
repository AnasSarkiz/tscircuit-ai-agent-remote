# Saved routes

No copper routes exist in revision A0. Requirements and component qualification have not passed.

The user requests persisted native routes and relocation of offending segments for DRC/shorts. This is recorded as a required future routing deliverable. Do not manufacture an empty cache or treat this directory as route evidence.

The pinned props support `pcbRouteCache: { pcbTraces, cacheKey }`. Before using it, verify the canonical cache-key generation and endpoint identity semantics in the pinned core/CLI, persist a valid routed result, rebuild from the saved routes, and run shorts plus geometric/connectivity checks. Change the saved source routes through the supported API; never patch a fabrication artifact to hide a violation. Revalidate the resulting copper and regenerate the entire fabrication package.

Source/API review2026-10-03 found the pinned supported per-phase autorouting:end.pcbTracePaths export and <autoroutingphase pcbTracePaths> replay API. Its canonical generator preserves unique connection selectors and wire/via geometry; unrepresentable junction/endpoints produce an unavailable reason rather than partial paths. Save original complete routing events and final JSON alongside versioned replay paths and source/dependency/placement/phase hashes, then verify replay before relocation. Every relevant phase must be retained; a stage's paths do not necessarily describe the complete board. Legacy pcbRouteCache key/multi-net replay remains unqualified. Detailed verified source locations and round-trip requirements: evidence/saved-route-api-review-2026-10-03/qualification.md. No copper, replay-tested routes or empty placeholder cache is created by this study.
