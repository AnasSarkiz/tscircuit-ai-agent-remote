"""Read only the existing automatic cloud builds; never request a rebuild."""
import json,datetime,urllib.request,urllib.parse
from pathlib import Path
folder=Path(__file__).resolve().parent
release_id='436cf0a3-fcb3-4479-a6b7-7fbbc616cc27'
url='https://registry-api.tscircuit.com/package_builds/list?'+urllib.parse.urlencode({'package_release_id':release_id})
with urllib.request.urlopen(url,timeout=45) as response:result=json.load(response)
record={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'release_id':release_id,'read_only':True,'endpoint':url,'response':result}
(folder/'cloud-build-list-observation.json').write_text(json.dumps(record,indent=2)+'\n')
builds=result.get('package_builds',[])
print(json.dumps({'response_keys':list(result),'build_ids':[item.get('package_build_id') for item in builds],'count':len(builds)}))
if builds:
    selected=max(builds,key=lambda build:build.get('created_at',''))
    assert selected['package_release_id']==release_id
    url='https://registry-api.tscircuit.com/package_builds/get?'+urllib.parse.urlencode({'package_build_id':selected['package_build_id']})
    with urllib.request.urlopen(url,timeout=45) as response:current=json.load(response)
    record={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'release_id':release_id,'existing_build_id':selected['package_build_id'],'read_only':True,'response':current}
    (folder/'cloud-build-observation.json').write_text(json.dumps(record,indent=2)+'\n')
    build=current['package_build']
    print(json.dumps({key:build.get(key) for key in ['package_build_id','build_in_progress','user_code_job_started_at','user_code_job_completed_at','user_code_job_error','circuit_json_build_error']}))
