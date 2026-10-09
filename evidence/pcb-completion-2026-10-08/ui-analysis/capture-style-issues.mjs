import { chromium } from '/workspace/tscircuit-ai-agent-remote/.tools/browser/node_modules/playwright-core/index.mjs'
import { spawn } from 'node:child_process'
import { createHash } from 'node:crypto'
import { openSync, readFileSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'

// Preserve the inherited proxy and TLS checks. The local preview is loopback;
// the configured public proxy CAs are trusted in the task's NSS database.
process.env.PLAYWRIGHT_DISABLE_FORCED_CHROMIUM_PROXIED_LOOPBACK = '1'
const output = '/tmp/current-qualified-board-style'
const native = readFileSync(`${output}/style-input/circuit.json`)
const receipt = {
  native_sha256: createHash('sha256').update(native).digest('hex'),
  command: 'tsci dev native circuit.json -p 3049',
  tls_verification_enabled: true,
  public_proxy_ca_trust: '/home/agent/.pki/nssdb; existing OpenAI-nebula-dns public CA',
  events: [],
  ui_schematic_style_passed: false,
}
const cli = spawn('bun', [resolve('node_modules/.bin/tsci'), 'dev', 'circuit.json', '-p', '3049'], {
  cwd: resolve(`${output}/style-input`),
  env: { ...process.env, RUNFRAME_STANDALONE_FILE_PATH: resolve('node_modules/@tscircuit/runframe/dist/standalone.min.js') },
  stdio: ['ignore', openSync(`${output}/ui-server.log`, 'w'), openSync(`${output}/ui-server-errors.log`, 'w')],
})
let browser, page
try {
  const deadline = Date.now() + 30_000
  while (true) {
    try {
      const response = await fetch('http://127.0.0.1:3049', { signal: AbortSignal.timeout(1000) })
      if (response.ok) break
    } catch {}
    if (Date.now() > deadline) throw Error('CLI native preview did not start')
    await new Promise(resolve => setTimeout(resolve, 250))
  }
  browser = await chromium.launch({
    executablePath: '/usr/bin/chromium', headless: true, args: ['--no-sandbox'],
    env: { ...process.env },
    proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY, bypass: '127.0.0.1,localhost' } : undefined,
  })
  page = await browser.newPage({ viewport: { width: 1500, height: 1100 } })
  page.on('pageerror', error => receipt.events.push({ kind: 'pageerror', message: error.message }))
  page.on('requestfailed', request => {
    if (request.url().includes('jscdn.tscircuit.com')) receipt.events.push({ kind: 'requestfailed', url: request.url(), error: request.failure() })
  })
  await page.goto('http://127.0.0.1:3049', { waitUntil: 'domcontentloaded' })
  let viewer
  const viewerDeadline = Date.now() + 20_000
  while (!viewer && Date.now() < viewerDeadline) {
    for (const frame of page.frames()) {
      if (await frame.getByText('Schematic', { exact: true }).count()) { viewer = frame; break }
    }
    if (!viewer) await page.waitForTimeout(250)
  }
  if (!viewer) throw Error('Schematic tab missing from preview frames')
  await viewer.getByText('Schematic', { exact: true }).first().click({ timeout: 10_000 })
  await page.mouse.click(1400, 950, { button: 'right' })
  await viewer.getByText('Run Style Analysis', { exact: true }).click({ timeout: 10_000 })
  receipt.run_style_analysis_clicked = true
  await viewer.getByText('Style Analysis', { exact: true }).first().waitFor({ timeout: 15_000 })
  await page.waitForTimeout(5000)
  receipt.body_text = await page.locator('body').innerText()
  receipt.frame_texts = await Promise.all(page.frames().map(async frame => ({ url: frame.url(), text: await frame.locator('body').innerText() })))
  const sources = (await Promise.all(page.frames().map(frame => frame.locator('img').evaluateAll(images => images.map(image => image.getAttribute('src')))))).flat().filter(src => src?.startsWith('data:image/svg+xml'))
  sources.forEach((src, index) => { const comma = src.indexOf(','); const bytes = src.slice(0, comma).includes('base64') ? Buffer.from(src.slice(comma + 1), 'base64') : Buffer.from(decodeURIComponent(src.slice(comma + 1))); writeFileSync(`${output}/style-issue-${index}.svg`, bytes) })
  receipt.captured_svg_count = sources.length

  await page.screenshot({ path: `${output}/ui-style-analysis.png`, fullPage: true })
  // Retain only visible UI text and screenshot; page HTML can contain credentials.
} catch (error) {
  receipt.error = error.message
  if (page) {
    receipt.body_text = await page.locator('body').innerText()
    await page.screenshot({ path: `${output}/ui-style-analysis.png`, fullPage: true })
  }
} finally {
  if (browser) await browser.close()
  cli.kill('SIGTERM')
  const text = [receipt.body_text, ...(receipt.frame_texts ?? []).map(frame => frame.text)].join('\n');
  const count = text.match(/(\d+) style issues? found/);
  receipt.issue_count = count ? Number(count[1]) : null;
  receipt.ui_schematic_style_passed = receipt.run_style_analysis_clicked === true && receipt.issue_count === 0 && !receipt.error;
  writeFileSync(`${output}/ui-style-analysis-receipt.json`, `${JSON.stringify(receipt, null, 2)}\n`)
  console.log(JSON.stringify({ native_sha256: receipt.native_sha256, events: receipt.events, error: receipt.error, run_style_analysis_clicked: receipt.run_style_analysis_clicked }))
}
