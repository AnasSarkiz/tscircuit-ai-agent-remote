export {}

// Read-only capture of the same public EasyEDA endpoints used by the pinned CLI.
const supplierPartNumber = process.argv[2]
if (!supplierPartNumber?.match(/^C[0-9]+$/)) throw new Error("Expected exact LCSC part number")
const response = await fetch("https://easyeda.com/api/components/search", {
  method: "POST",
  headers: {
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    referer: "https://easyeda.com/editor",
    "x-requested-with": "XMLHttpRequest",
  },
  body: `type=3&doctype%5B%5D=2&uid=0819f05c4eef4c71ace90d822a990e87&returnListStyle=classifyarr&wd=${supplierPartNumber}&version=6.4.7`,
})
if (!response.ok) throw new Error(`EasyEDA search HTTP ${response.status}`)
const searchResponse: {
  success: boolean
  result: { lists: { lcsc: Array<{ uuid: string; lcsc: { number: string } }> } }
} = await response.json()
await Bun.write(
  `evidence/imports/${supplierPartNumber}-search.json`,
  JSON.stringify(searchResponse, null, 2),
)
const componentRecord = searchResponse.result.lists.lcsc.find(
  (component) => component.lcsc.number === supplierPartNumber,
)
if (!componentRecord) throw new Error("No exact supplier match")
const componentResponse = await fetch(
  `https://easyeda.com/api/components/${componentRecord.uuid}?version=6.4.7&uuid=${componentRecord.uuid}&datastrid=`,
)
if (!componentResponse.ok) throw new Error(`EasyEDA component HTTP ${componentResponse.status}`)
await Bun.write(
  `evidence/imports/${supplierPartNumber}-raw.json`,
  JSON.stringify(await componentResponse.json(), null, 2),
)
