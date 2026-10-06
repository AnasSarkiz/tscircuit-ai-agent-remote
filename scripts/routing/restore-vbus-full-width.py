"""Restore full .5 mm VBUS trunks using the corrected strip outline generator.

Original native source snapshots remain unchanged. The rejected .35 mm neck
experiment is removed; source endpoints, layers and nominal widths are retained.
"""
import json,runpy,sys
from pathlib import Path
b=runpy.run_path(str(Path(__file__).with_name('plan-connection-bridges.py')))
source=Path(sys.argv[1]);original=Path(sys.argv[2]);current=json.loads(source.read_text());before=json.loads(original.read_text())
selected=current['pours'][78:82]
if [(r['net'],r['layer'],r['nominal_width_mm']) for r in selected]!=[
    ('VBUS','bottom',.5),('VBUS','bottom',.3),('VBUS','top',.3),('VBUS','top',.5)]:
    raise ValueError('Expected the explicit rejected via-neck experiment')
restored=[]
for region in before['pours'][78:80]:
    if region['net']!='VBUS' or region['nominal_width_mm']!=.5:raise ValueError('Expected original full-width trunks')
    restored.extend(b['region_records']('VBUS',{'parts':[(region['layer'],region['path_mm'])],
        'width':.5,'drawn_width_mm':region['drawn_width_mm']}))
current['pours'][78:82]=restored
index=next(i for i,r in enumerate(current['pad_necks']) if r['terminal']=='.C1 > .pin1')
current['pad_necks'][index]=next(r for r in before['pad_necks'] if r['terminal']=='.C1 > .pin1')
source.write_text(json.dumps(current,indent=2)+'\n')
print(json.dumps({'restored_full_width_regions':len(restored),'nominal_width_mm':.5,
    'total_remaining_C1_narrow_length_mm':current['pad_necks'][index]['total_narrow_length_mm'],
    'fresh_native_qualification_required':True}))
