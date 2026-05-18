# Issue Lifecycle

States: `created` → `assigned` → `running` → `needs_review` → `accepted` | `rework`

## State Definitions

| State | Meaning |
|-------|---------|
| `created` | Issue filed, not yet picked up |
| `assigned` | Worker claimed, not started |
| `running` | Actively working |
| `needs_review` | Output delivered, awaiting QC |
| `accepted` | QC passed, work done |
| `rework` | QC failed, must fix and resubmit |

## Transitions

- `created` → `assigned`: Worker picks up issue
- `assigned` → `running`: Work begins
- `running` → `needs_review`: Worker posts result comment
- `needs_review` → `accepted`: QC approves
- `needs_review` → `rework`: QC fails, routed back
- `rework` → `needs_review`: Worker resubmits

## Worker Reporting Requirement

At `needs_review`, worker **must** post result via:
```
multica issue comment add <issue-id> --content "..."
```
Terminal output does NOT reach the user.