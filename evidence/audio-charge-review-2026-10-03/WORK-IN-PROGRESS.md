# Audio and charge-interface review — 2026-10-03

The exact JST S3B-PH-SM4-TB(LF)(SN) / C265101 three-contact, top-side SMT
connector imported successfully through the supported exact-footprint/model
workflow. It is a candidate battery+/battery−/NTC interface, not a qualified
pack/harness. Nominal PH series 2 A applies with AWG24; actual pack harness
and contact polarity must be reviewed. No imported definitions were changed.

BLOCKING B-012: exact PUI Audio AS04008PS-4W-R / C3311258 speaker is listed
by LCSC but native import reports “Component not found in EasyEDA library
search”. Stage2 qualification/import and integration of this speaker stop.
No generic speaker definition or locally authored substitute was created.
Manufacturer name is PUI Audio, not CUI; earlier research shorthand was wrong.
Continue identifying a genuine suitable/importable alternative and reviewing
the independent MAX98357A amplifier application.

Type-C input entitlement/dead-pack startup needs hardware review. Original
Rd resistors do not establish permission for 500 mA before enumeration.
TUSB320I C80170 (TI primary datasheet) is a possible UFP GPIO detector:
OUT1 high means default/unattached; low means attached1.5/3A advertisement.
OUT2 distinguishes default attached and1.5/3A. Exact TUSB320LAI C132554
exists too, but its different datasheet must be reviewed before selecting.
Controller supply, integrated Rd, startup, charger EN modes, system enable and
brownout/thermal budgets remain unimplemented. Do not reuse an I2C-only/default
firmware decision where dead-pack charging requires hardware behavior.

Gitc82e7de display review is verified on private main. Native private publisher
session69035/tagwip-a0-display-logic-review remains active; its enumerated source
files are frozen. New research files and new imports were created after native
file enumeration and belong to a later milestone. Auto-review initially rejected
this push over checkout scope; source proof of canonical hidden-path exclusions
and relevant board proposal evidence resolved it, retry accepted. No bypass.
