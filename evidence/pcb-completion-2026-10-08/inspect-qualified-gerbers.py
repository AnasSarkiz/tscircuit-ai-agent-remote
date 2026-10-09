import sys,json,dataclasses
from pathlib import Path
sys.path.insert(0,str(Path('.gerber-runtime').resolve()))
from pygerber.gerberx3.api.v2 import GerberFile,OnParserErrorEnum
from gerber.excellon import loads,DrillSlot
root=Path('evidence/pcb-completion-2026-10-08/NOT-FOR-FABRICATION-qualified-gerbers')
results=[]
for path in sorted(root.glob('*.gbr')):
    parsed=GerberFile.from_file(path).parse(on_parser_error=OnParserErrorEnum.Raise)
    info={k:float(v) for k,v in dataclasses.asdict(parsed.get_info()).items()}
    if path.name in ['F_Cu.gbr','In1_Cu.gbr','In2_Cu.gbr','B_Cu.gbr','Edge_Cuts.gbr']:
        parsed.render_raster(root/(path.stem+'.png'),dpmm=12)
    results.append({'file':path.name,'strict_parse':True,'bounds':info})
drills=[]
for path in sorted(root.glob('*.drl')):
    parsed=loads(path.read_text())
    slots=[h for h in parsed.hits if isinstance(h,DrillSlot)]
    vias=[h for h in parsed.hits if not isinstance(h,DrillSlot) and abs(h.tool.diameter-.3)<1e-8]
    drills.append({'file':path.name,'hits':len(parsed.hits),'slots':len(slots),'round_0_3mm':len(vias),'diameters_mm':sorted({h.tool.diameter for h in parsed.hits})})
assert len(results)==12
assert drills[0]['slots']==4 and drills[0]['round_0_3mm']==320
assert drills[1]['hits']==8  # Six genuine component holes plus two 2.2 mm mounting holes
result={'gerber_parser':'PyGerber 2.4.3, Raise on parser errors','drill_parser':'PCB-tools 0.1.6','gerbers':results,'drills':drills,'fabrication_ready':False}
(root.parent/'independent-qualified-export-inspection.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
