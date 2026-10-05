# Native routing orchestration only: retain inputs/events, preserve real output paths,
# and remove only the failing trial assignment so independent work can continue.
import json,re,subprocess
from pathlib import Path
base=Path('evidence/a7-routing-2026-10-05')
routing=Path('src/board/Routing.tsx');nets=Path('src/board/nets.tsx')
base_routing=routing.read_text();base_nets=nets.read_text()
names=['VSYS','V3V3','VBUS','PACK_BAT','CHARGER_ISET','CHARGE_PGOOD_N','CHARGE_STATUS_N','BUCK_ENABLE','MCU_EN','MCU_BOOT_N','MCU_RESET_N','MCU_MIC_BCLK','MCU_MIC_WS','MCU_MIC_SD','MIC_INPUT','VMIC','MIC_BCLK_INPUT','MIC_WS_INPUT','MIC_BCLK','MIC_WS','MIC_SD','MIC_SD_BUFFERED','MIC_SD_REF','AMP_SD_MODE','MCU_AUDIO_ENABLE','MCU_AUDIO_LRCLK','AUDIO_NMOS_GATE','AUDIO_PMOS_GATE','AUDIO_ENABLE_SUPPLY','AMP_LRCLK','SPEAKER_P','SPEAKER_N','VMOTOR','HAPTIC_NMOS_GATE','HAPTIC_N','HOLD_HARDWARE','MCU_LCD_CS_N','MCU_LCD_SCLK','MCU_LCD_SDA','MCU_LCD_DC','MCU_LCD_RESET_N','MCU_BACKLIGHT_PWM','BACKLIGHT_GATE']
# Paired speaker members occupy one phase, as native differential-pair API requires.
plans=[{'name':n.lower().replace('_','-'),'nets':[n],'index':100+i} for i,n in enumerate(names) if n!='SPEAKER_N']
for p in plans:
 if p['nets']==['SPEAKER_P']:p['nets'].append('SPEAKER_N')
plans=[p for p in plans if p["nets"][0] not in ["VSYS","V3V3","VBUS","PACK_BAT"]]
accepted={};pending=plans.copy();failures=[]
for attempt in range(401,401+len(plans)+1):
 if not pending:break
 new_routing=base_routing;imports='';blocks=''
 for p in plans:
  if p['name'] not in accepted and p not in pending:continue
  cache=p['name'] in accepted
  if cache:imports+=f'import p{p["index"]} from "../../routes/a7/{p["name"]}.json"\n'
  blocks+=f'''          <autoroutingphase name="{p['name']}" phaseIndex={{{p['index']}}}
            {'pcbTracePaths={fanoutTracePath.array().parse(p'+str(p['index'])+')}' if cache else ''}
            autorouter={{{{ preset: "auto_local", allowViaInPad: false, traceClearance: 0.2 }}}}
            {{...routingTolerances}} />\n'''
 new_routing=imports+new_routing.replace('          <autoroutingphase\n            name="hold-readback"',blocks+'          <autoroutingphase\n            name="hold-readback"')
 new_nets=base_nets
 for p in plans:
  if p['name'] not in accepted and p not in pending:continue
  for n in p['nets']:
   if f'<net name="{n}"' in new_nets:new_nets=new_nets.replace(f'<net name="{n}"',f'<net name="{n}" routingPhaseIndex={{{p["index"]}}}')
   else:new_nets=new_nets.replace('    <>',f'    <>\n      <net name="{n}" routingPhaseIndex={{{p["index"]}}} />')
 routing.write_text(new_routing);nets.write_text(new_nets)
 folder=base/f'native-expanded-{attempt:02d}';log=base/f'native-expanded-{attempt:02d}.log'
 print(json.dumps({'attempt':attempt,'pending':len(pending),'saved':len(accepted)}),flush=True)
 with log.open('w') as out:
  try: result=subprocess.run(['bun',str(base/'capture-native.tsx'),str(folder),'45000'],stdout=out,stderr=subprocess.STDOUT,timeout=120)
  except subprocess.TimeoutExpired:
   (folder/'external-timeout.json').write_text(json.dumps({'status':'INCOMPLETE NATIVE RENDER','reason':'External observation budget; raw native events preserved; full final JSON unavailable'},indent=2)+'\n')
 if not (folder/'circuit.json').exists():
  starts=[json.loads(f.read_text()) for f in folder.glob('start-*.json')]
  failed=[x for x in starts if x.get('phaseName') in [p['name'] for p in pending]]
  if not failed:raise RuntimeError(f'Capture stalled before a requested phase: {log}')
  failed=max(failed,key=lambda x:x.get('phaseOrdinal',0))['phaseName'];failures.append({'phase':failed,'directory':str(folder),'unfinished':True});pending=[p for p in pending if p['name']!=failed];print(json.dumps({'deferred_unfinished_trial':failed}),flush=True);continue
 events=json.loads((folder/'end-event-index.json').read_text())
 for e in events:
  if e['phase'] not in [p['name'] for p in pending]:continue
  event=json.loads((folder/e['file']).read_text());paths=event.get('pcbTracePaths')
  if not paths:raise RuntimeError(f'No genuine paths for completed phase {e}')
  Path(f'routes/a7/{e["phase"]}.json').write_text(json.dumps(paths,indent=2)+'\n');accepted[e['phase']]={'directory':str(folder),'event':e['file'],'paths':len(paths)}
 pending=[p for p in pending if p['name'] not in accepted]
 board=json.loads((folder/'circuit.json').read_text());errors=[x for x in board if x['type']=='pcb_autorouting_error']
 if errors or (folder/'interruption.json').exists():
  starts=[json.loads(f.read_text()) for f in folder.glob('start-*.json')]
  failed=[s for s in starts if s.get('phaseName') in [p['name'] for p in pending]]
  if not failed:raise RuntimeError('Failed native phase not identified')
  failed=max(failed,key=lambda x:x.get('phaseOrdinal',0))['phaseName'];failures.append({'phase':failed,'directory':str(folder),'errors':errors,'interrupted':(folder/'interruption.json').exists()});pending=[p for p in pending if p['name']!=failed]
  print(json.dumps({'deferred_failed_trial':failed,'saved':len(accepted)}),flush=True)
 elif pending:raise RuntimeError('Native pipeline skipped a requested phase')
 (base/'expanded-progress-401.json').write_text(json.dumps({'accepted_native_paths':accepted,'failed_trials':failures,'pending':pending},indent=2)+'\n')
 if (base/'pause-native-trials').exists():
  print(json.dumps({'paused_for_dependency_update':True,'remaining_trials':len(pending)}),flush=True)
  break
# Rebuild the source without any failed trial phase. Preserve every failed artifact.
new_routing=base_routing;imports='';blocks='';new_nets=base_nets
for p in plans:
 if p['name'] not in accepted:continue
 imports+=f'import p{p["index"]} from "../../routes/a7/{p["name"]}.json"\n'
 blocks+=f'''          <autoroutingphase name="{p['name']}" phaseIndex={{{p['index']}}}
            pcbTracePaths={{fanoutTracePath.array().parse(p{p['index']})}}
            autorouter={{{{ preset: "auto_local", allowViaInPad: false, traceClearance: 0.2 }}}}
            {{...routingTolerances}} />\n'''
 for n in p['nets']:
  if f'<net name="{n}"' in new_nets:new_nets=new_nets.replace(f'<net name="{n}"',f'<net name="{n}" routingPhaseIndex={{{p["index"]}}}')
  else:new_nets=new_nets.replace('    <>',f'    <>\n      <net name="{n}" routingPhaseIndex={{{p["index"]}}} />')
routing.write_text(imports+base_routing.replace('          <autoroutingphase\n            name="hold-readback"',blocks+'          <autoroutingphase\n            name="hold-readback"'));nets.write_text(new_nets)
print(json.dumps({'complete_native_trials':True,'saved_phases':len(accepted),'failed_trials':len(failures)}),flush=True)
