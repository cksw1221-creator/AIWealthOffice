# Multica Environment Report

Generated: 2026-05-18T15:24:15.780300+00:00
CLI path: `C:\Users\ChenKun\.multica\bin\multica.exe`
CLI version: `{'arch': 'amd64', 'commit': 'e6cf5a6e', 'date': '2026-05-18T10:36:33Z', 'go': 'go1.26.1', 'os': 'windows', 'version': '0.3.2'}`
Auth status: Server:  https://api.multica.ai
User:    陈坤 (cksw1221@gmail.com)
Token:   [REDACTED]
Workspace ID: `not detected from table output`

## Capability Matrix

| Capability | OK | Output | Summary |
| --- | --- | --- | --- |
| version | yes | json | object with 6 field(s) |
| auth_status | yes | table | Server:  https://api.multica.ai<br>User:    陈坤 (cksw1221@gmail.com)<br>Token:   [REDACTED] |
| workspace_list | yes | table | ID                                    NAME<br>cfb8ddd6-061c-4538-8bbe-9c277fcc93ec  AIWealthOffice |
| runtime_list | yes | json | 2 item(s) |
| agent_list | yes | json | 3 item(s) |
| issue_list | yes | json | 3 item(s) in issues |
| issue_create | yes | json | available in adapter; skipped to avoid creating a probe issue |
| issue_get | yes | json | object with 20 field(s) |
| issue_runs | yes | json | 2 item(s) |
| issue_run_messages | yes | json | 0 item(s) |

## Runtimes

- Codex (ChenKunDesktop)
- Claude (ChenKunDesktop)

## Agents

- Coder-A-MulticaAdapter
- Coder-B-TaskProtocol
- Coder-C-QuantMVP

## Redaction

- Token-like fields and bearer values are redacted before writing outputs.
- Probe does not read `.env`, key, or PEM files.
