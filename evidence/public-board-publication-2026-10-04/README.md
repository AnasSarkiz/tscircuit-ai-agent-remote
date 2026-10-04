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

Target 0.0.2-wip-a1-public-board. Source commit, remote publisher exit, anonymous full
readback and the GitHub circuit JSON hash will be recorded after publication.
