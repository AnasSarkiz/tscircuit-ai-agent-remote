"""Add real copper to an authored strip while retaining its nominal requirement."""
import json,runpy,sys
from pathlib import Path
b=runpy.run_path(str(Path(__file__).with_name('plan-connection-bridges.py')))
source=Path(sys.argv[1]);index=int(sys.argv[2]);drawn_width=float(sys.argv[3]);content=json.loads(source.read_text());region=content['pours'][index]
if drawn_width<=region['drawn_width_mm']:raise ValueError('This operation only widens the actual source copper')
replacement=b['region_records'](region['net'],{'parts':[(region['layer'],region['path_mm'])],
    'width':region['nominal_width_mm'],'drawn_width_mm':drawn_width})
if len(replacement)!=1:raise ValueError('Expected one complete source strip')
content['pours'][index]={**region,**replacement[0],
    'outline_reserve_basis':'Additional real copper at a measured native width deficit; nominal width unchanged; fresh native clearance, width and continuity audits required'}
source.write_text(json.dumps(content,indent=2)+'\n')
print(json.dumps({'source_region_index':index,'nominal_width_mm':region['nominal_width_mm'],'old_drawn_width_mm':region['drawn_width_mm'],'new_drawn_width_mm':drawn_width}))
