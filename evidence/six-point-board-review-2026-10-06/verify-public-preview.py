"""Verify the anonymous published native preview and observe existing builds."""
import json,hashlib,datetime,urllib.request
from pathlib import Path
folder=Path(__file__).resolve().parent
release_id='436cf0a3-fcb3-4479-a6b7-7fbbc616cc27'
version='0.0.5-wip-style-vias-power'
native_bytes=(folder/'final-native/circuit.json').read_bytes()
native=json.loads(native_bytes)
url='https://registry-api.tscircuit.com/package_releases/get_preview_circuit_json?package_release_id='+release_id
with urllib.request.urlopen(url,timeout=45) as response:
    status=response.status;preview=json.load(response)
candidates=[]
def visit(value,path='$',component_path=None):
    if isinstance(value,list):
        if value and isinstance(value[0],dict) and 'type' in value[0]:
            candidates.append((path,value,component_path));return
        for i,item in enumerate(value):visit(item,path+'['+str(i)+']',component_path)
    elif isinstance(value,dict):
        component_path=value.get('component_path',value.get('file_path',component_path))
        for key,item in value.items():visit(item,path+'.'+key,component_path)
visit(preview)
matches=[(path,component_path) for path,value,component_path in candidates if value==native]
assert matches,'Published preview does not contain exact validated native object'
page='https://tscircuit.com/AnasSarkiz/tscircuit-ai-agent-remote/releases/'+release_id+'/preview'
with urllib.request.urlopen(page,timeout=45) as response:page_status=response.status
record={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'release_id':release_id,'version':version,'preview_endpoint_url':url,'anonymous_http_status':status,'exact_native_object_equality':True,'matching_native_paths':matches,'local_native_json_sha256':hashlib.sha256(native_bytes).hexdigest(),'native_elements':len(native),'schematic_sheet_count':sum(item['type']=='schematic_sheet' for item in native),'preview_page_url':page,'preview_page_anonymous_http_status':page_status,'browser_thumbnail_or_remote_CI_success_inferred':False,'fabrication_ready':False}
(folder/'final-public-preview-receipt.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record))
