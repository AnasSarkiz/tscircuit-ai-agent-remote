import { createHash } from "node:crypto"
import { readFileSync, writeFileSync } from "node:fs"
import { convertCircuitJsonToBomRows, convertBomRowsToCsv } from "../bom-export-review-2026-10-03/runtime/node_modules/circuit-json-to-bom-csv/dist/index.js"

// Resolve the official exporter against dated exact supplier identities.
// This exports supplier package labels, not newly authored PCB footprints.
const circuitPath = process.argv[2]
const outputDirectory = process.argv[3]
if (!circuitPath || !outputDirectory) throw new Error("Provide native Circuit JSON and output directory")
const nativeBytes = readFileSync(circuitPath)
const circuitJson = JSON.parse(nativeBytes.toString("utf8"))
const supplierReceipt = JSON.parse(readFileSync("evidence/pcb-completion-2026-10-08/official-stock/receipt.json", "utf8"))
const supplierParts = new Map(supplierReceipt.results.map(receipt => {
  if (!receipt.exact_mpn_match || receipt.stock_record?.componentCode !== receipt.part_number || !receipt.stock_record.componentSpecificationEn?.trim()) {
    throw new Error(`Unqualified supplier identity/package ${receipt.part_number}`)
  }
  return [receipt.part_number, { mfr: receipt.model, package: receipt.stock_record.componentSpecificationEn, manufacturer: receipt.manufacturer }]
}))
const resolvedParts = []
const bomRows = await convertCircuitJsonToBomRows({
  circuitJson,
  resolvePart: async ({ source_component }) => {
    if (source_component.ftype === "simple_test_point") return null
    const jlcpcbParts = source_component.supplier_part_numbers?.jlcpcb
    if (jlcpcbParts?.length !== 1) throw new Error(`Missing exact supplier for ${source_component.name}`)
    const supplierPart = supplierParts.get(jlcpcbParts[0])
    if (!supplierPart || supplierPart.mfr !== source_component.manufacturer_part_number || !supplierPart.package?.trim()) {
      throw new Error(`Supplier identity/package mismatch for ${source_component.name}`)
    }
    resolvedParts.push({ designator: source_component.name, jlcpcb_part: jlcpcbParts[0], mpn: supplierPart.mfr, supplier_package: supplierPart.package })
    return {
      footprint: supplierPart.package,
      supplier_part_number_columns: { "JLCPCB Part #": jlcpcbParts[0] },
      // The dated exact official record supplies the manufacturer and MPN.
      manufacturer_mpn_pairs: [{ manufacturer: supplierPart.manufacturer, mpn: supplierPart.mfr }],
    }
  },
})
const blankDescriptions = bomRows.filter(row => !row.comment.trim())
const supplierCodesAsPackages = bomRows.filter(row => /^C[0-9]+$/.test(row.footprint))
if (bomRows.length !== 125 || resolvedParts.length !== 125 || blankDescriptions.length || supplierCodesAsPackages.length) {
  throw new Error("Resolved BOM does not cover the exact purchased population")
}
writeFileSync(`${outputDirectory}/NOT-FOR-FABRICATION-resolved-bom.csv`, convertBomRowsToCsv(bomRows))
const receipt = {
  source_circuit_json: circuitPath,
  native_sha256: createHash("sha256").update(nativeBytes).digest("hex"),
  converter: "circuit-json-to-bom-csv@0.0.19",
  method: "Official resolvePart callback; exact native MPN and JLC identity matched to recorded supplier package. No CSV repair or imported footprint edit.",
  bom_rows: bomRows.length,
  blank_description_count: blankDescriptions.length,
  supplier_code_as_package_count: supplierCodesAsPackages.length,
  supplier_identity_count: new Set(resolvedParts.map(part => part.jlcpcb_part)).size,
  manufacturer_company_names_available: true,
  current_stock_verified: false,
  stock_receipt_source: "official-stock/receipt.json",
  current_dated_inventory_recorded: true,
  current_buyability_covers_identities: supplierReceipt.covered_parts,
  fabrication_ready: false,
  resolved_parts: resolvedParts,
}
writeFileSync(`${outputDirectory}/resolved-bom-receipt.json`, JSON.stringify(receipt, null, 2) + "\n")
console.log(JSON.stringify({ bom_rows: receipt.bom_rows, blank_description_count: receipt.blank_description_count, supplier_code_as_package_count: receipt.supplier_code_as_package_count, supplier_identity_count: receipt.supplier_identity_count, fabrication_ready: false }))
