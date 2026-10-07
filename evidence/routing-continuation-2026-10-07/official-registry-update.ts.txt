import { findPackageReleaseId } from "lib/package_release/find-package-release-id"
import { withWinterSpec } from "lib/with-winter-spec"
import { z } from "zod"

const routeSpec = {
  methods: ["POST"],
  auth: "none",
  jsonBody: z.object({
    package_release_id: z.string().uuid().optional(),
    package_name_with_version: z.string().optional(),
    is_locked: z.boolean().optional(),
    is_latest: z.boolean().optional(),
    ready_to_build: z.boolean().optional(),
    license: z.string().optional(),
  }),
  jsonResponse: z.object({
    ok: z.boolean(),
  }),
} as const

export default withWinterSpec(routeSpec)(async (req, ctx) => {
  const { is_locked, is_latest, ready_to_build, license } = req.jsonBody
  const delta = Object.fromEntries(
    Object.entries({ is_locked, is_latest, ready_to_build, license }).filter(
      ([, v]) => v !== undefined,
    ),
  )
  const package_release_id = await findPackageReleaseId(req.jsonBody, ctx)

  if (!package_release_id) {
    return ctx.error(404, {
      error_code: "package_release_not_found",
      message: "Package release not found",
    })
  }

  if (Object.keys(delta).length === 0) {
    return ctx.error(400, {
      error_code: "no_fields_provided",
      message: "No fields provided to update",
    })
  }

  await ctx.db.transaction().execute(async (trx) => {
    if (delta.is_latest !== undefined) {
      if (delta.is_latest) {
        await trx
          .updateTable("main.package_release")
          .set({
            is_latest: false,
          })
          .where("package_release_id", "!=", package_release_id)
          .where("is_latest", "=", true)
          .where("package_id", "=", (qb) =>
            qb
              .selectFrom("main.package_release")
              .where("package_release_id", "=", package_release_id)
              .select("package_id")
              .limit(1),
          )
          .execute()
      }
    }

    await trx
      .updateTable("main.package_release")
      .set(delta)
      .where("package_release_id", "=", package_release_id)
      .execute()
  })

  return ctx.json({
    ok: true,
  })
})
