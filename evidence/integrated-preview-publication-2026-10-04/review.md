# A1 native private publication outcome

Source revision: `4535f6d97a91e15e9a947b50167c42343de903c4`.
GitHub main was pushed successfully and verified with exact remote readback.
Native release: `0.0.2-wip-a1-integrated-placement-preview`.
The native publisher exited 1: 1,232 reported successes and 118 failures
(110 timeouts, 8 HTTP 413 size-limit rejections). Source files stayed frozen
through publication, with zero source-manifest mismatches.

Exact-version readback exited 0. Among the 118 reported failures, 108 files
arrived byte-identically and 10 are HTTP 404. There are zero mismatched or
unverified cases. The additional source/deliverable checks also match:
all 90 source-manifest files, main.tsx, generated circuit.json, PCB top,
ratsnest, 3D top, 3D bottom and the 13-page schematic PDF. Total 174 files
checked: 164 byte-identical, 10 missing. The package is private and
ready_to_build=false. Publication remains incomplete: B-009.

Eight missing files were rejected with HTTP 413, including the native 22 MB
board.glb. Two timeout files are also missing. Every missing file remains
available locally and in the verified GitHub revision. No custom upload,
archive compression, evidence omission or forced readiness was used.

Missing exact-release files:

- `evidence/audio-charge-review-2026-10-03/amplifier-schema-failures.json`
- `evidence/audio-charge-review-2026-10-03/bq24074.pdf`
- `evidence/blocker-recheck-2026-10-03-1357/strict-schema-failures.json`
- `evidence/haptic-review-2026-10-03/driver-schema-failures.json`
- `evidence/integrated-preview-2026-10-03/board.glb`
- `evidence/type-c-current-review-2026-10-03/schema-failures.json`
- `imports/SN74LVC245APWR/SN74LVC245APWR.step`
- `imports/TPD2EUSB30ADRTR/TPD2EUSB30ADRTR.step`
- `imports/TPS61160DRVR/TPS61160DRVR.obj`
- `references/tps7a20.pdf`

These are outcome notes created after publication enumeration. They are excluded
from the A1 release and will accompany the next real implementation revision;
there is no metadata-only commit/publication retry loop. The background watcher
remains paused. No routing, fabrication approval or physical test is claimed.
