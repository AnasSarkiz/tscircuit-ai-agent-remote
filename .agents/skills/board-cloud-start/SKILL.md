---
name: board-cloud-start
description: Initialize the existing handheld AI remote cloud checkpoint safely before routing work.
---

Read root AGENTS.md and CLOUD_HANDOFF.md first. Continue this board in the repository root. Run `bash scripts/cloud/setup.sh`, then `source scripts/cloud/env.sh` in each task shell. Setup installs exact locked dependencies and geometry tools; it must not launch routing. Verify checkpoint hashes before source changes. Run TypeScript and static tests; retained board failures are open engineering gates, never environment-install success. Never weaken tests.

After setup, run heavy native routing/build operations through `python3 scripts/cloud/run_with_budget.py --seconds 900 --log <new-log-path> -- <real-command>`. One operation only; no local Mac heavy work. Preserve solver inputs/events/full JSON and phase paths. Resource-stopped trials are not accepted caches. Resume the latest accepted checkpoint in the handoff and repair verified physical connections; the old U2 proposal is no longer the starting action. Battery outer contacts and contact-dependent display fanout stay deferred. GitHub main and matching public tscircuit WIP publication are authorized; verify public source and native bytes. No watcher resume, other-chat messaging, orders or fabrication-ready claim.

Require all four supervisor smoke cases to pass once after a fresh Linux setup, and again if the supervisor changes. `setup.sh` runs `python3 scripts/cloud/smoke_test.py`; preserve its outcome. This is environment protection, not board validation. A passing unchanged session does not need another smoke run before every heavy command.
