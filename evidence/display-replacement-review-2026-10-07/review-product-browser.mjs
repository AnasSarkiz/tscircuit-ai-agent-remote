import { chromium } from '../../.tools/browser/node_modules/playwright-core/index.mjs'
import { writeFileSync } from 'node:fs'

const output = 'evidence/display-replacement-review-2026-10-07'
const url = 'https://www.buydisplay.com/spi-2-3-inch-tft-lcd-touch-screen-display-320x240-ili9432-controller'
const receipt = { url, checked_at_utc: new Date().toISOString(), tls_verification_enabled: true }
let browser
try {
  browser = await chromium.launch({
    executablePath: '/usr/bin/chromium',
    headless: true,
    args: ['--no-sandbox'],
    env: { ...process.env },
    proxy: process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined,
  })
  const page = await browser.newPage()
  const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20_000 })
  receipt.http_status = response?.status()
  receipt.title = await page.title()
  receipt.body_text = await page.locator('body').innerText()
  writeFileSync(`${output}/browser-product-page.html`, await page.content())
  await page.screenshot({ path: `${output}/browser-product-page.png`, fullPage: true })
} catch (error) {
  receipt.error = error.message
} finally {
  if (browser) await browser.close()
  writeFileSync(`${output}/browser-product-receipt.json`, `${JSON.stringify(receipt, null, 2)}\n`)
  console.log(JSON.stringify(receipt))
}
