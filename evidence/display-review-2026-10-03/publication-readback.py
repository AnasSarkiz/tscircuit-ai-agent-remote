import json, hashlib, urllib.request, urllib.error, datetime
from pathlib import Path
config=json.loads(Path("/Users/anassarkiz/Library/Preferences/tscircuit-nodejs/config.json").read_text())
version="AnasSarkiz/tscircuit-ai-agent-remote@0.0.2-wip-a0-mcu-usb-review"
def post(endpoint, body):
    request=urllib.request.Request("https://registry-api.tscircuit.com/"+endpoint,data=json.dumps(body).encode(),headers={"Content-Type":"application/json","Authorization":"Bearer "+config["sessionToken"]})
    try:
        with urllib.request.urlopen(request,timeout=45) as response:return json.load(response)
    except urllib.error.HTTPError as error:return {"http_status":error.code}
release=post("package_releases/get",{"package_name_with_version":version})
record={"checked_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source_revision":"02950fb70e20bc3add927c36aa2fde9b21dd1db7","version":version,"publisher_exit_code":1,"reported_successes":535,"reported_failures":4,"ready_to_build":release.get("package_release",{}).get("ready_to_build"),"files":[]}
for file_path in ["src/mcu/esp32-s3-usb-review.tsx","imports/SN74LVC1G125DBVR/SN74LVC1G125DBVR.step","imports/SN74LVC245APWR/SN74LVC245APWR.step","imports/TPS63802DLAR/TPS63802DLAR.step","references/tps7a20.pdf"]:
    response=post("package_files/get",{"package_name_with_version":version,"file_path":"/"+file_path})
    remote=response.get("package_file",{})
    content=remote.get("content_text")
    import base64
    payload=content.encode() if isinstance(content,str) else base64.b64decode(remote["content_base64"]) if remote.get("content_base64") else None
    sha=hashlib.sha256(payload).hexdigest() if payload is not None else None
    record["files"].append({"path":file_path,"http_status":response.get("http_status"),"remote_sha256":sha,"matches":sha==hashlib.sha256(Path(file_path).read_bytes()).hexdigest() if sha else None})
Path("evidence/display-review-2026-10-03/publication-failure-receipt.json").write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps(record,indent=2))
