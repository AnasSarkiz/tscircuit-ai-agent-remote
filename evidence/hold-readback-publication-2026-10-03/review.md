# Hold-readback publication exact receipt

Native supported `tsci push --private --version-tag wip-a0-hold-readback-review` session17411 ended exit1. GitHub source0573bf4492817ea0263827b6f0431fb7905d4959 was previously pushed and exact main verified. The actual private registry release is0.0.2-wip-a0-hold-readback-review. No enumerated source/artifact bytes changed during publication or readback.

The CLI reports1081successes and20failures. Exact authenticated readback proves13reported failed files have matching local/remote byte hashes, seven haveHTTP404, and none are mismatched or unverified. This verifies reported failures, not every reported successful file. Package remains private=true and ready_to_build=false. This revision is not fully published and is not fabrication-ready.

Six missing files match the persistent HTTP413 failures: evidence/audio-charge-review-2026-10-03/amplifier-schema-failures.json and bq24074.pdf; evidence/haptic-review-2026-10-03/driver-schema-failures.json; evidence/type-c-current-review-2026-10-03/schema-failures.json; imports/SN74LVC245APWR/SN74LVC245APWR.step; references/tps7a20.pdf. The seventh missing file at this exact version is imports/TLV3201AIDBVR/TLV3201AIDBVR.tsx (C105188), reported as a timeout. Historical release-specific missing-file conclusions remain separate.

Native log was checked before saving: no Request Body line, no unusually long payload line. Credentials stay in the existing configuration and are read in memory only; no credential output is saved. Readback uses native registry read endpoints and exact release identity. No custom upload, evidence omission, compressed substitute, forced readiness, schema patch or early routing was used.

B-009 result was sent to authorized chat01a0f218-ce92-7671-b666-efccdef3aed2, “Clarify issue status”. Local read-only watch and publication receipts were created after publisher enumeration and are outside this release. They are pending inclusion in a future validated implementation revision; this review does not create a new board version or claim a complete remote update.
