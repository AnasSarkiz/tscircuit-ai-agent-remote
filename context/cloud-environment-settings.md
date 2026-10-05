# Prepared Codex Cloud environment settings

Environment creation is pending GitHub connector access to this exact board repository. No environment ID, published environment or cloud execution is claimed.

- Repository: AnasSarkiz/tscircuit-ai-agent-remote, main. No other repository required.
- Suggested name: tscircuit-ai-agent-remote.
- Sharing: Only me / private environment (the board source repository is public).
- Install script: `bash scripts/cloud/setup.sh`.
- Start skill: repository `board-cloud-start`, with tscircuit skill available in `.agents/skills/tscircuit`.
- Shell initialization: `source scripts/cloud/env.sh`.
- Setup validation: checksum verification, locked install, Linux supervisor smoke test, TypeScript and static tests. Retained board failures stay visible; setup must not start routing.
- Network: existing restricted/package-manager access; no unrestricted network/security reduction or credentials copied from Mac.
- Do not publish/save an environment as successful until its real setup report is reviewed. Start continuation with context/cloud-start-prompt.txt from the migrated main revision.

Official current environment guide: https://learn.chatgpt.com/docs/environments/cloud-environments
