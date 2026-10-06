import { chromium } from '../../.tools/browser/node_modules/playwright-core/index.mjs'
import { spawn } from 'node:child_process'
import { writeFileSync, openSync } from 'node:fs'
import { resolve } from 'node:path'
// Preserve the inherited proxy for remote requests; Chromium's forced
// loopback proxying must be disabled only for this local CLI preview.
process.env.PLAYWRIGHT_DISABLE_FORCED_CHROMIUM_PROXIED_LOOPBACK = '1'
const output = 'evidence/six-point-board-review-2026-10-06'
const cli = spawn('bun', [resolve('node_modules/.bin/tsci'),'dev','circuit.json','-p','3041'], {cwd:resolve(`${output}/style-input`),env:{...process.env,RUNFRAME_STANDALONE_FILE_PATH:resolve('node_modules/@tscircuit/runframe/dist/standalone.min.js')},stdio:['ignore',openSync(`${output}/ui-server.log`,'w'),openSync(`${output}/ui-server-errors.log`,'w')],detached:true})
const receipt={command:'tsci dev native circuit.json -p 3041',events:[]}
let browser, page
try {
 const deadline=Date.now()+45000
 while(true){try {const response=await fetch('http://127.0.0.1:3041',{signal:AbortSignal.timeout(1000)});if(response.ok)break}catch{}if(Date.now()>deadline)throw Error('CLI preview did not start');await new Promise(r=>setTimeout(r,250))}
 browser=await chromium.launch({executablePath:'/usr/bin/chromium',headless:true,args:['--no-sandbox'],proxy:process.env.HTTPS_PROXY?{server:process.env.HTTPS_PROXY,bypass:'127.0.0.1,localhost'}:undefined})
 page=await browser.newPage({viewport:{width:1500,height:1100}})
 page.on('pageerror',error=>receipt.events.push({kind:'pageerror',message:error.message}))
 page.on('requestfailed',request=>{if(request.url().includes('jscdn.tscircuit.com'))receipt.events.push({kind:'requestfailed',url:request.url(),error:request.failure()})})
 await page.goto('http://127.0.0.1:3041',{waitUntil:'domcontentloaded'})
 let viewer
 const viewerDeadline=Date.now()+25000
 while(!viewer && Date.now()<viewerDeadline){for(const frame of page.frames()){if(await frame.getByText('Schematic',{exact:true}).count()){viewer=frame;break}}if(!viewer)await page.waitForTimeout(250)}
 if(!viewer)throw Error('Schematic tab missing from all preview frames')
 await viewer.getByText('Schematic',{exact:true}).first().click({timeout:10000})
 // The viewer's style analysis is in its own right-click menu.
 await page.mouse.click(1400,950,{button:'right'})
 await viewer.getByText('Run Style Analysis',{exact:true}).click({timeout:10000})
 receipt.run_style_analysis_clicked=true
 await viewer.getByText('Style Analysis',{exact:true}).first().waitFor({timeout:15000})
 await page.waitForTimeout(3000)
 receipt.body_text=await page.locator('body').innerText();receipt.frame_texts=await Promise.all(page.frames().map(async f=>({url:f.url(),text:await f.locator('body').innerText()})))
 await page.screenshot({path:`${output}/ui-style-analysis.png`,fullPage:true})
 writeFileSync(`${output}/ui-style-analysis.html`,await page.content())
} catch(error){receipt.error=error.message;if(page){receipt.frames=page.frames().map(f=>f.url());receipt.body_text=await page.locator('body').innerText();receipt.frame_texts=await Promise.all(page.frames().map(async f=>({url:f.url(),text:await f.locator('body').innerText()})));await page.screenshot({path:`${output}/ui-style-analysis.png`,fullPage:true});writeFileSync(`${output}/ui-style-analysis.html`,await page.content())}}
finally{
 if(browser)await browser.close()
 try{process.kill(-cli.pid,'SIGTERM')}catch{}
 writeFileSync(`${output}/ui-style-analysis-receipt.json`,JSON.stringify(receipt,null,2)+'\n')
 console.log(JSON.stringify(receipt))
}
