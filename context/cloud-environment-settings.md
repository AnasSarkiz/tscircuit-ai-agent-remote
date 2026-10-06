# Prepared Codex Cloud environment settings

The managed Linux environment is connected and running. The environment-status tool on 2026-10-06 reports current observations, desired/observed phase `running`, specification revision 1, no reported failure, and restricted networking with the package-manager preset. Credential/capability readiness is not established by the empty capability list. Real locked installs, supervised routing and CLI builds run in this workspace; a fresh-container restore has not been tested.

- Repository: AnasSarkiz/tscircuit-ai-agent-remote, main. No other repository required.
- Suggested name: tscircuit-ai-agent-remote.
- Sharing: Only me / private environment (the board source repository is public).
- Install script: `cd /workspace/tscircuit-ai-agent-remote` followed by `bash scripts/cloud/setup.sh`.
- Start skill: repository `board-cloud-start`, with tscircuit skill available in `.agents/skills/tscircuit`.
- Shell initialization: `source scripts/cloud/env.sh`.
- Setup validation: checksum verification, locked install, Linux supervisor smoke test, TypeScript and static tests. Retained board failures stay visible; setup must not start routing.
- Network: existing restricted/package-manager access; no unrestricted network/security reduction or credentials copied from Mac.
- Keep routing out of the install script. The setup report and saved configuration draft are reviewable separately from board validation. Start continuation with context/cloud-start-prompt.txt from the accepted main revision; preserve the current restricted network policy and configured secrets.

Official current environment guide: https://learn.chatgpt.com/docs/environments/cloud-environments

The connection-repair checkpoint setup was tested successfully on 2026-10-06: 397 exact files verified, frozen Bun 1.3.9 install, Python 3.12.14 geometry dependencies and all four supervisor smoke cases passed. Setup launched no board routing. A complete install/start-instruction draft was saved successfully with requires_publish=true; network, secrets and repository membership were preserved. Review and save the draft in Environment settings, then publish it to activate it. A fresh-container restore remains unverified. See evidence/connection-repair-2026-10-06/cloud-setup-receipt.json.
