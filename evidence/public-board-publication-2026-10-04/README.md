# Public board publication — 2026-10-04

User authorization: make the existing board GitHub repository and tscircuit package
public, and push the built Circuit JSON. No routing or fabrication approval requested.

The official package update API accepts is_private/is_unlisted/public_dist_enabled;
the inspected upstream endpoint source is preserved. Only this board package was
updated to false/false/true. GitHub repository visibility changed through gh repo edit.
Anonymous GitHub metadata confirms private=false. No credentials were printed or stored.

The native root build completed with routing disabled and network available.
The restricted-network first build added 122 source_part_not_found_warning elements;
that build was rejected for publication and replaced with the successful network build.
4808 elements; zero traces/vias/errors. Every element except source_project_metadata
matches the previously visually inspected connector revision. Its schematic/PCB/GLB
reviews remain applicable because geometry/connectivity are unchanged. Three connector
orientation warnings and previous component metadata warnings remain visible.

Format and root/staged TypeScript checks pass. Canonical tests: 30 pass/one existing
B-010 schema failure/272 assertions. Native five checks are recorded separately.
B-005 microphone polygon paste, B-010 native schema, B-015 assembly BOM fields and
all remaining electrical/mechanical/routing/fabrication gates are unchanged.

.gitignore permits dist/index/circuit.json only. The preparer requires a native root
build and copies that artifact byte-for-byte into the board-only package. The staged
source closure is identical to the validated root runtime source, and staged types pass.
The package retains 75 files, no documents/scripts/evidence/tests/unused components.
package.json private=true is the npm accidental-publication guard; registry visibility
is controlled by its official API and is public. No npm publication is requested.

Both destinations are now **public** and anonymously accessible. Published source
commit **6f8f4a270e76c7455084a1d43ea92833694179f2** and registry release
**0.0.2-wip-a1-public-board**. Native upload exited0, 75 successes/zero failures;
anonymous exact-version readback verifies all 75 hashes with no missing, extra or
unverified files. Public GitHub and registry `dist/index/circuit.json` are identical
(2,298,951 bytes; SHA-256 `0be465e43d862abd74d8fa7b8f397738fcae90f8134c330cf2311bdf54d273ca`).
Registry `is_private=false`, `is_unlisted=false`, `public_dist_enabled=true`.
`ready_to_build=true` and null reported build errors do not establish a completed
cloud build or fabrication readiness. Receipt-only follow-up changes no runtime
input and needs no additional registry release.
