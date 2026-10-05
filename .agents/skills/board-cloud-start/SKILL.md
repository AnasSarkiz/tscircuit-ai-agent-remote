---
name: board-cloud-start
description: Initialize the existing handheld AI remote cloud checkpoint safely before routing work.
---

Read root AGENTS.md and CLOUD_HANDOFF.md first. Continue this board in the repository root. Run `bash scripts/cloud/setup.sh`, then `source scripts/cloud/env.sh` in each task shell. Setup installs exact locked dependencies and geometry tools; it must not launch routing. Verify checkpoint hashes before source changes. Run TypeScript and static tests; retained board failures are open engineering gates, never environment-install success. Never weaken tests.

After setup, run heavy native routing/build operations through `python3 scripts/cloud/run_with_budget.py --seconds 900 --log <new-log-path> -- <real-command>`. One operation only; no local Mac heavy work. Preserve solver inputs/events/full JSON and phase paths. Resource-stopped trials are not accepted caches. Follow handoff first actions, including unbuilt U2 via clearance correction and actual replay/geometry verification. Battery outer contacts and contact-dependent display fanout stay deferred. No watcher resume, other-chat messaging, registry retry, orders or fabrication-ready claim.
