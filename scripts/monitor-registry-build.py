"""Observe a public tscircuit cloud build without requesting duplicate builds."""

import argparse
import datetime
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path


def read_build(build_id):
    query = urllib.parse.urlencode({'package_build_id': build_id, 'include_logs': 'true'})
    request = urllib.request.Request('https://registry-api.tscircuit.com/package_builds/get?' + query)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)['package_build']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build-id', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seconds', type=int, default=300)
    args = parser.parse_args()
    if args.seconds <= 0:
        parser.error('--seconds must be positive')
    deadline = time.monotonic() + args.seconds
    previous_status = None
    observations = []
    while True:
        build = read_build(args.build_id)
        status = {
            'build_in_progress': build['build_in_progress'],
            'started_at': build.get('user_code_job_started_at'),
            'completed_at': build.get('user_code_job_completed_at'),
            'error': build.get('user_code_job_error'),
            'website_url': build.get('package_build_website_url'),
        }
        observations.append({
            'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'status': status,
        })
        complete = status['completed_at'] is not None or status['error'] is not None
        record = {
            'build_id': args.build_id,
            'observations': observations,
            'latest_build': build,
            'completed': complete,
            'succeeded': complete and status['error'] is None,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(record, indent=2) + '\n')
        if status != previous_status:
            print(json.dumps(status), flush=True)
            previous_status = status
        if complete:
            return 0 if record['succeeded'] else 1
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            print('Observation deadline reached; cloud build has no completed result.', flush=True)
            return 2
        time.sleep(min(20, remaining))


if __name__ == '__main__':
    raise SystemExit(main())
