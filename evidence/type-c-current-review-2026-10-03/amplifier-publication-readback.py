import json, hashlib, urllib.request, urllib.error, datetime
from pathlib import Path
config=json.loads(Path("/Users/anassarkiz/Library/Preferences/tscircuit-nodejs/config.json").read_text())
version="AnasSarkiz/tscircuit-ai-agent-remote@0.0.2-wip-a0-amplifier-review"
def post(endpoint, body):
    request=urllib.request.Request("https://registry-api.tscircuit.com/"+endpoint,data=json.dumps(body).encode(),headers={"Content-Type":"application/json","Authorization":"Bearer "+config["sessionToken"]})
    try:
        with urllib.request.urlopen(request,timeout=20) as response:return json.load(response)
    except urllib.error.HTTPError as error:return {"http_status":error.code}
    except (TimeoutError, urllib.error.URLError) as error:return {"network_error":type(error).__name__}
release=post("package_releases/get",{"package_name_with_version":version})
record={"checked_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source_revision":"50bebdb6c283cf72ab4ab1e28321782e28065cf8","version":version,"publisher_exit_code":1,"reported_successes":665,"reported_failures":13,"ready_to_build":release.get("package_release",{}).get("ready_to_build"),"files":[]}
for file_path in ["src/audio/speaker-amplifier-review.tsx", "bun.lock", "evidence/audio-charge-review-2026-10-03/AO3400A.pdf", "evidence/audio-charge-review-2026-10-03/AO3401A.pdf", "evidence/audio-charge-review-2026-10-03/AS04008PS-4W-R.pdf", "evidence/audio-charge-review-2026-10-03/README.md", "evidence/audio-charge-review-2026-10-03/WORK-IN-PROGRESS.md", "evidence/audio-charge-review-2026-10-03/amplifier-schema-failures.json", "evidence/audio-charge-review-2026-10-03/bq24074.pdf", "imports/SN74LVC245APWR/SN74LVC245APWR.step", "imports/TLV3201AIDBVR/TLV3201AIDBVR.step", "imports/TPS3839G33DBZR/TPS3839G33DBZR.step", "imports/TPS7A2033PDBVR/TPS7A2033PDBVR.step", "references/tps7a20.pdf"]:
    response=post("package_files/get",{"package_name_with_version":version,"file_path":"/"+file_path})
    remote=response.get("package_file",{})
    content=remote.get("content_text")
    import base64
    payload=content.encode() if isinstance(content,str) else base64.b64decode(remote["content_base64"]) if remote.get("content_base64") else None
    sha=hashlib.sha256(payload).hexdigest() if payload is not None else None
    record["files"].append({"path":file_path,"http_status":response.get("http_status"),"network_error":response.get("network_error"),"remote_sha256":sha,"matches":sha==hashlib.sha256(Path(file_path).read_bytes()).hexdigest() if sha else None})
Path("evidence/type-c-current-review-2026-10-03/amplifier-publication-failure-receipt.json").write_text(json.dumps(record,indent=2)+"\n")
print(json.dumps(record,indent=2))
