# Official release applicability watch

Read-only follow-up to board revision0573bf4492817ea0263827b6f0431fb7905d4959. Existing publisher session17411 is still running; no files enumerated by that publication were changed. This new evidence was created after enumeration and is not part of the in-progress release.

Official npm metadata now reports core0.0.2067 (64bcfafa49e533543a541b9822415e6210b1525a) and easyeda0.0.369 (dc3fee46760b0abb146607da47b3fa868662edf3). Exact GitHub comparison responses are preserved here. Other watched versions remain unchanged. An initial query mistakenly used the different package easyeda-converter; the corrected releases.json uses the supported easyeda package. No dependency change was made.

Core PR4332 preserves canonical electrical attributes that already exist on imported source ports, and requests optional datasheet information from parts-engine. Explicit user attributes remain authoritative. The reviewed source includes identity checks and a visible warning when enrichment fails. This does not create missing metadata in the board's existing genuine JSX component definitions.

Easyeda PR590 supports caller-supplied pinAttributes and writes them to Circuit JSON and generated TSX. Its README explicitly says fetching and validating datasheet metadata remains the caller's responsibility. No geometry, paste, custom schematic label or B-010 repair appears in this exact release diff.

Latest published CLI0.1.2237 import source is preserved here. It still uses its prior datasheet-fetch, addDatasheetAttributesToCircuitJson and convertCircuitJsonToTscircuit branch, with convertRawEasyToTsx({rawEasy}) when no attributes are returned. It does not pass the new pinAttributes option to that API. This is source inspection, not a newly established end-to-end importer defect.

Supported native CLI0.1.2235 `import C2149796 --jlcpcb` was run in the isolated fresh-import directory, exit0. It produces genuine TPS22919DCKR/C2149796 with ground pin2 and NC pin4 metadata only; supply pin1 remains undeclared. Native log and unmodified generated definition are preserved. No board import was replaced. No fresh fixture build or complete native-schema validation was performed on this observation, and no warning was suppressed. B-007 remains open; neither release resolves B-010 or the current footprint/fabrication blockers.

PR4283 remains open at head7fa3beb2f9c83878d1d65cec4e591f68e8fb4b50; mergeability now reports true, which does not mean merged or published. Its previously inspected late-registration fix remains separate from these new releases. No new routing result is inferred.

The release/applicability update was sent to the human-authorized fix chat “Clarify issue status” (01a0f218-ce92-7671-b666-efccdef3aed2). No upstream implementation, scope or landing approval was granted. Whole-board stages remain1in progress,2blocked,3–6not started,7physical testing pending,8not started.

Primary sources: https://github.com/tscircuit/core/pull/4332 ; https://github.com/tscircuit/easyeda-converter/pull/590 ; https://github.com/tscircuit/core/pull/4283 .

Follow-up05:46UTC: official core0.0.2068/head690320b3a80b7364c0ffc10331456d89f2df78df adds PR4333, preserving supplier imports when a strict legacy parts engine rejects the new optional datasheet request field. Exact source diff and tests inspected; the fallback retains part-identity checks and a visible warning. This addresses compatibility introduced by2067, not our unchanged JSX imports or B-010/paste/body/BOM/publication blockers. No dependency installed, no test pass inferred from upstream source. Other watched versions unchanged. PR4283 remains open at the same head, merged=false; mergeability now false, a changing advisory state rather than publication or resolution. No material new board issue, so no duplicate fix-chat message or user notification.
