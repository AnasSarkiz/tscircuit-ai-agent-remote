# Independent search for the replacement display — 2026-10-07

The user instructed the agent to find the display information directly rather
than asking them to supply another PDF. The manufacturer's own catalog search,
robots.txt and sitemap.xml were requested through the inherited proxy with TLS
verification enabled; all returned Cloudflare HTTP 403. Google and Bing searches
were denied by the configured CONNECT proxy. Those outcomes are preserved.

GitHub's code index is accessible through the configured route.
Searching it produced 19 references to ER-TFT023-1, including third-party pin
tables and older hardware designs. These include mirrors of the same designs;
19 hits do not mean 19 independent sources. Later searches explicitly exclude
this board repository to avoid treating our own published review as evidence.

## Findings from accessible references

- DavidAustin/python-eda at commit
  `03aa9317c3206c7518efebec9e77f66bed94ffea` contains a 50-pin ER-TFT023-1 table.
  All 50 roles agree with the old ER-TFT026-1 primary pin table for the current
  SPI configuration, after normalizing names. New secondary pin 33 is named NC
  where the old primary table calls it SDO; this board already leaves it open.
  This suggests reuse of the current SPI/backlight circuitry, but it does not
  verify the replacement's voltage, current limits or physical contact mapping.
- adamgreig/linetime at commit
  `66cabfca1a41a9574b209027391a7ded56ba2b5b` lists ER-TFT023-1 and an ER-CON50HT-1
  connector in its BOM, and uses `ili9342_init` in firmware. The user-supplied
  product URL spells the controller ILI9432. ILI9342 is therefore a useful lead,
  not a manufacturer-confirmed correction to the current listing.
- That older design's XML actually uses an ER-TFT024-3 library symbol and links
  a different panel's datasheet. Its generic symbol cannot qualify the exact
  ER-TFT023-1 power limits or mechanical drawing.
- The aherbez/audiotest and aherbez/game2 symbol references point to
  `https://www.buydisplay.com/download/manual/ER-TFT023-1_Datasheet.pdf`.
  This confirms the existing candidate path as a third-party reference, but
  neither repository tree contains the PDF. The DavidAustin and linetime trees
  also contain no exact panel datasheet. Corrected GitHub issue searches found
  no ER-TFT023 discussion with an attached drawing.

The external pin table is archived only as review evidence. It is not a
permitted JLCPCB component import and was not used to create a board component.
`secondary-interface-audit.json` records the 50-row comparison and its limits.

## Connector and mechanical status

The older references support a 50-pin connector search, including the existing
upper-contact C262650/AFC07-S50ECA-00 and conditional lower-contact candidate
C11063/AFC07-S50FCC-00. Their previously dated official stock observations remain
in the preceding replacement review. No new stock allocation is claimed here.
The replacement's exact contact face, flex length, exit, folded path, insertion
orientation and body dimensions remain unverified. The two genuine imports have
opposite local pin-1 sides, so their identities cannot simply be swapped while
retaining the old provisional mapping.

No manufacturer drawing was recovered. No contact-dependent net or routing
change is accepted. The user authorized a replacement review, not speculative
pin assignments or extra components. The full board remains not ready to order.

## Browser access and automatic approval review

The configured system CA bundle verifies the supplier's TLS chain successfully
with OpenSSL. Its issuer is the already configured public environment proxy CA,
SHA-256 fingerprint
`C71B4D1E9D7775C538C688AB10CEA9CE417D7312E89838F9D15FF73256CD7FC3`.
The initial diagnosis that this CA was absent from Chromium's actual
`/home/agent/.pki/nssdb` was incorrect. Comparing certificate fingerprints, rather
than nicknames, shows it already existed as `OpenAI-nebula-dns`. Supplying
XDG_DATA_HOME did not resolve Chromium's certificate error. No private keys,
credential values or user browser credentials were inspected.

Automatic approval review initially rejected the proposed certutil import
before execution because that persistent trust change had not been explicitly
authorized. The user then replied **"Approve this CA import"**. The exact approved
command completed with exit 0; it did not add a distinct CA, since the same
certificate was already present. The original rejection receipt is retained as
a historical observation, not a current pending approval.

The actual browser fault is NSS initialization error **SEC_ERROR_READ_ONLY
(-8126)** against its real database under the filesystem sandbox. An approved
browser execution with access to that database restored normal certificate
verification. No TLS checks were disabled and no rejected action was executed
through an indirect workaround. The requested product then returned HTTP 403
with a real Cloudflare challenge. Its page specifically reports the required
`challenges.cloudflare.com` verification service as blocked; an independent
request to that host returns CONNECT 403 Forbidden. The product contains no
accessible PDF links at this checkpoint. This is a concrete remaining network
prerequisite, not an unverified missing-certificate assumption.

The environment draft adds `www.google.com`, `www.bing.com` and
`challenges.cloudflare.com` while preserving the previous 14 domains, for 17
explicit hosts. Draft saving is confirmed, with
requires_publish=true; it does not apply the running policy. The user must
review/save settings and publish the environment to activate those hosts.
The saved start instructions include the corrected browser diagnosis. Applying
these hosts permits another normal website attempt; it does not prove the
origin will serve its drawing or that a replacement fits.

## Actual schematic UI analysis after restoring browser TLS

The same browser repair unblocked the previously requested UI style analysis.
The native input hash exactly matches the accepted board. The normal **Run Style
Analysis** UI executed across all schematic sheets and reported **14 issues**:
two inner-label collisions (U12/U3), one inverted power rail (R42), three
decoupling-group spacing issues, and eight spread-out rail paths. The exact
component/pin/message records, screenshot and compressed original HTML are in
`ui-analysis/`. This UI result does not agree with the earlier CLI result of
zero issues. Both observations remain explicit; UI style has not passed.
These are schematic findings, not additional measured PCB shorts or proof of
electrical DRC success. No layout change or new native build is claimed here.

## Preservation and next step

The accepted board/package remains 0.0.8-wip-speaker-routing with native SHA-256
`35c5fb2bfc870daf11b5f5e30847f1e5a86fd886ebb8ef11fc3cf6e88e77e63d`.
Only review metadata changes. No PCB source, import, model, solver path or native
copper changes; no passing fabrication, ordering or physical-test claim.

Browser trust approval has been applied; do not request it again or repeatedly
import the existing CA. After network settings are applied, retry the supplier
page and search indexes with normal TLS verification and the inherited proxy.
Final exact-model GitHub code/repository/PDF-filename searches are also retained;
they add no manufacturer drawing. Continue retrieving the actual drawing before
selecting contact face or implementing the replacement. The independent
schematic issues require source-layout review and revalidation in a subsequent
implementation; they must not be hidden or converted into a passing UI check.
