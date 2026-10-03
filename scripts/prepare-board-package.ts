import { createHash } from "node:crypto"
import { existsSync, mkdirSync, readFileSync, rmSync, statSync, writeFileSync } from "node:fs"
import { dirname, extname, join, relative, resolve } from "node:path"
import ts from "typescript"

const projectDir = resolve(import.meta.dir, "..")
const packageDir = join(projectDir, ".publish/board")
const sourcePaths = new Set<string>()
const externalModules = new Set<string>()

function resolveLocalModule(importerPath: string, moduleName: string): string {
  const candidate = resolve(dirname(importerPath), moduleName)
  const candidates = [
    candidate,
    `${candidate}.tsx`,
    `${candidate}.ts`,
    join(candidate, "index.tsx"),
  ]
  const modulePath = candidates.find((path) => existsSync(path) && statSync(path).isFile())
  if (!modulePath) throw new Error(`Missing module ${moduleName} imported by ${importerPath}`)
  const relativePath = relative(projectDir, modulePath)
  if (relativePath.startsWith("..") || relativePath.startsWith("/")) {
    throw new Error(`Module escapes board directory: ${modulePath}`)
  }
  return modulePath
}

function collectSource(sourcePath: string): void {
  if (sourcePaths.has(sourcePath)) return
  sourcePaths.add(sourcePath)
  if (![".ts", ".tsx"].includes(extname(sourcePath))) return
  const sourceFile = ts.createSourceFile(
    sourcePath,
    readFileSync(sourcePath, "utf8"),
    ts.ScriptTarget.Latest,
  )
  function visit(node: ts.Node): void {
    if (ts.isImportDeclaration(node) || ts.isExportDeclaration(node)) {
      const moduleSpecifier = node.moduleSpecifier
      if (moduleSpecifier && ts.isStringLiteral(moduleSpecifier)) {
        const moduleName = moduleSpecifier.text
        if (moduleName.startsWith(".")) collectSource(resolveLocalModule(sourcePath, moduleName))
        else externalModules.add(moduleName)
      }
    }
    if (ts.isCallExpression(node) && node.expression.kind === ts.SyntaxKind.ImportKeyword) {
      throw new Error(`Dynamic import needs explicit packaging review: ${sourcePath}`)
    }
    ts.forEachChild(node, visit)
  }
  visit(sourceFile)
}

collectSource(join(projectDir, "index.circuit.tsx"))
for (const moduleName of externalModules) {
  if (!["tscircuit", "@tscircuit/props"].includes(moduleName)) {
    throw new Error(`Unreviewed external module: ${moduleName}`)
  }
}

rmSync(packageDir, { recursive: true, force: true })
mkdirSync(packageDir, { recursive: true })
for (const sourcePath of sourcePaths) {
  const targetPath = join(packageDir, relative(projectDir, sourcePath))
  mkdirSync(dirname(targetPath), { recursive: true })
  writeFileSync(targetPath, readFileSync(sourcePath))
}

const originalPackage = JSON.parse(readFileSync(join(projectDir, "package.json"), "utf8"))
const runtimePackage = {
  name: originalPackage.name,
  version: originalPackage.version,
  description: "A1 complete unrouted handheld AI remote prototype; not fabrication ready",
  main: "index.circuit.tsx",
  author: originalPackage.author,
  private: true,
  scripts: {
    dev: "tsci dev",
    build: "tsci build index.circuit.tsx --routing-disabled",
    typecheck: "tsc --noEmit",
  },
  devDependencies: {
    "@tscircuit/cli": originalPackage.devDependencies["@tscircuit/cli"],
    "@tscircuit/core": originalPackage.devDependencies["@tscircuit/core"],
    "@tscircuit/props": originalPackage.overrides["@tscircuit/props"],
    "@types/bun": originalPackage.devDependencies["@types/bun"],
    tscircuit: originalPackage.devDependencies.tscircuit,
    typescript: originalPackage.devDependencies.typescript,
  },
  overrides: originalPackage.overrides,
}
writeFileSync(join(packageDir, "package.json"), `${JSON.stringify(runtimePackage, null, 2)}\n`)
for (const filePath of ["tsconfig.json", "tscircuit.config.json", "bun.lock"]) {
  writeFileSync(join(packageDir, filePath), readFileSync(join(projectDir, filePath)))
}
const manifest = [...sourcePaths].sort().map((sourcePath) => ({
  path: relative(projectDir, sourcePath),
  bytes: readFileSync(sourcePath).length,
  sha256: createHash("sha256").update(readFileSync(sourcePath)).digest("hex"),
}))
writeFileSync(
  join(projectDir, ".publish/source-manifest.json"),
  `${JSON.stringify({ entry: "index.circuit.tsx", externalModules: [...externalModules].sort(), files: manifest }, null, 2)}\n`,
)
console.log(`Prepared ${manifest.length} board source/model files in ${packageDir}`)
