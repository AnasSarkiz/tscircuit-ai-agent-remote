import { expect, test } from "bun:test"
import { readFileSync } from "node:fs"
import { any_circuit_element } from "circuit-json"

// Validate the complete immutable generated fixture once during loading, as
// the manufacturer fixtures do. This is a schema check, not a timing benchmark.
const validation = any_circuit_element
  .array()
  .safeParse(
    JSON.parse(readFileSync(new URL("../dist/index/circuit.json", import.meta.url), "utf8")),
  )

test("the complete current native output conforms to the installed schema", () => {
  expect(validation.success).toBe(true)
  if (!validation.success) throw validation.error
  expect(validation.data.length).toBeGreaterThan(0)
})
