# Multica local patch: comment-session resume

This project currently depends on a local Multica daemon patch that enables controlled session continuity for issue comment follow-ups.

Patch file:

- `0001-daemon-resume-comment-sessions.patch`

What it does:

- Adds `MULTICA_RESUME_COMMENT_SESSIONS=1` daemon opt-in.
- When Multica Cloud omits `prior_session_id` for issue comment follow-ups, the local daemon infers the provider session from `prior_work_dir`.
- Verified with a clean Multica issue experiment: same issue comment follow-up resumed Claude session and recalled visible prior context after the automatic Round 1 comment was deleted.

Local runtime notes:

- Patched binary was built from `../multica` with portable Go 1.26.3.
- Installed local binary path: `%USERPROFILE%\.multica\bin\multica.exe`.
- Original release binary backup: `%USERPROFILE%\.multica\bin\multica.exe.bak-0.3.2`.
- Required daemon env: `MULTICA_RESUME_COMMENT_SESSIONS=1`.

Do not treat this as an upstream Multica release until the patch is merged upstream or replaced by an official option.
