import json,math
from pathlib import Path
# TI TIDA-01232 Eq7/8: IPC-2221 empirical screening, not a physical thermal test.
def width_mm(current_a, layer):
    copper_mm=layer["copper_mm"]
    rise_c=20
    k=0.024 if layer["internal"] else 0.048
    area_mil2=(current_a/(k*rise_c**0.44))**(1/0.725)
    return area_mil2/(copper_mm/0.0254)*0.0254
rows=[]
for current in [.08,.10,.30,.5,1,1.5,2,3]:
    external=width_mm(current,{"copper_mm":.035,"internal":False})
    internal=width_mm(current,{"copper_mm":.0152,"internal":True})
    rows.append({'current_a':current,'external_35um_min_nominal_mm':external,'inner_15p2um_min_nominal_mm':internal,'external_width_before_minus20percent_width_tolerance_mm':external/.8,'inner_width_before_minus20percent_width_tolerance_mm':internal/.8})
via_radius_outer_mm=.15+.025
via_radius_inner_mm=.15
via_area_mm2=math.pi*(via_radius_outer_mm**2-via_radius_inner_mm**2)
receipt={'method':'IPC-2221 empirical static screening from TI TIDA-01232 Eq7/8','temperature_rise_c':20,'external_copper_mm':.035,'inner_copper_mm':.0152,'provisional_stack':'JLC04161H-7628','rows':rows,'via_example':{'finished_hole_mm':.30,'assumed_barrel_copper_mm':.025,'barrel_cross_section_mm2':via_area_mm2,'equivalent_external_35um_trace_width_mm':via_area_mm2/.035,'thermal_capacity_result':'UNQUALIFIED: cross-section equivalence is not a via current rating; manufacturer guaranteed barrel thickness, length, temperature rise and current sharing required'},'limitations':['No measured copper exists yet','Copper thickness tolerance and neck-downs not included in nominal formula','Actual rail currents, peak duration, enclosure temperature and adjacent copper remain unqualified','Use IPC-2152/validated thermal model and prototype measurements for final thermal qualification; formula alone does not establish safety']}
Path('evidence/routing-intake-2026-10-04/power-width-study.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
