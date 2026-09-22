# DEV4-06-R3｜Final Regression Evidence & Release Gate

## Decision

**RC_CANDIDATE_READY**

- Tested version: `v0.4.5-dev.4-R2`
- Tested remote commit: `6f8462d89545948bffd35b520d793858565efd72`
- Automated gate: **20 PASS / 0 FAIL**
- Manual device regression: **10 PASS / 0 FAIL**
- Manual acceptance confirmed by user: **2026-09-22**

R3 records evidence only. It does not modify the tested application, APP_VERSION, data formats, Supabase schema, Stable branch, `main`, or formal PUBLIC.

## Automated Gate

Run from the repository root:

```bash
node tools/dev4-06-r3-release-gate.mjs
```

Validated areas:

1. Root and isolated Preview JavaScript syntax.
2. Root and Preview static duplicate IDs.
3. Root and Preview literal DOM references.
4. Root and Preview duplicate function declarations.
5. Root and Preview Service Worker syntax.
6. Root and Preview manifest JSON.
7. Root and Preview APP_VERSION consistency.
8. Canonical Meetup validation and cross-module selector synchronization.
9. `全部歷史` non-destructive current Meetup behavior.
10. Stale / deleted `activeMeetupId` cleanup contract.
11. Preview Cloud, IndexedDB, localStorage, and cache isolation.
12. Supabase schema and patch immutability.
13. Git diff integrity.

## Manual Device Evidence

The user confirmed the DEV4-06-R2 test build as **OK** after using the immutable R2 test link. The accepted 10-item matrix covers:

- Ranking → Awards → Share synchronization.
- Awards → Ranking → Share synchronization.
- Share → Ranking → Awards synchronization.
- `全部歷史` without clearing the active Meetup.
- Immediate return to the current Meetup.
- Source Meetup carry-over from Live, Awards, Post-game Review, and Unified History.
- Valid context recovery after reload.
- Invalid / deleted context cleanup and fallback.
- Root / Preview runtime-visible regression behavior.
- Preview storage, cloud, and cache isolation.

## Integrity Hashes

| Artifact | SHA-256 |
| --- | --- |
| `index.html` | `2cfc9990947716acce1a0a23a8e70756fd75b2858371695b1f73c73118dc99c0` |
| `preview/v0.4.5-dev.4/index.html` | `623a2985095deb3199670bbb638c00df66ce429057c9e03270f4d76018f391ea` |
| `manifest.webmanifest` | `0253987b2d9e8a9fbf3a206e7311b9921305ccbe95d4426248f23905c34341fe` |
| `preview/v0.4.5-dev.4/manifest.webmanifest` | `6dfe5c1a71b9fee5a105cb75b06dc10a469601c56e965362963c1c190e07777d` |
| `sw.js` | `97d2139a81de41091cde9f71de7e76b9814381076e635113240031b32095ebac` |
| `preview/v0.4.5-dev.4/sw.js` | `e05f94924de74a7b0aa1e1fce9e537ea92bb8ce8810349f45fcd4ba00095e0e6` |

## Release Gate Guardrails

- Unified History remains the single score/history source.
- No second Player / History / Analytics store.
- No Session / Backup / Roster metadata format change.
- No Supabase schema or patch change.
- PUBLIC-only players remain read-only.
- Preview remains isolated from Stable and formal PUBLIC.
- Promotion is limited to the next governed `v0.4.5-RC.1` stage.

## Gate Outcome

All required automated and manual checks passed. There are no P0, P1, or P2 blockers recorded for DEV4-06. The tested R2 artifact is eligible to enter `v0.4.5-RC.1｜Release Candidate Integration & Freeze Gate` without additional dev.4 feature changes.
