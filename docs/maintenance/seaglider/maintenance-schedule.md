---
title: Seaglider Maintenance Schedule
description: What to check before every deployment, after every recovery, and on its own schedule — a Seaglider maintenance overview organised by timing rather than by component.
---

# Seaglider Maintenance Schedule

This page organizes maintenance by **when** it needs doing, not by which
component it touches — the detailed how-to for each item lives on the
relevant [Glider Components](../../glider-components/seaglider/index.md)
page or checklist; this is the index that tells you when to go read it.

!!! note "Shorter than the Slocum page, for now"
    Fewer Seaglider component pages exist on this site so far (Batteries,
    Altimeter, VBD) — this schedule will grow as more are added. See the
    [Glider Components](../../glider-components/seaglider/index.md) section
    for what currently exists.

!!! info "Source"
    Synthesized from facts already established across this site's Seaglider
    pages — see those pages for sourcing and full detail.

---

## Before Every Deployment

| Item | What to confirm | Detail |
|---|---|---|
| Self-test | Run the interactive self-test; field team and pilot both review the capture before sign-off | [Deployment Checklist](../../deployment/seaglider/checklists/seaglider-deployment-checklist.md) |
| Buoyancy engine variant | Confirm whether this glider has an Enhanced Buoyancy Engine before touching `$T_BOOST`/`$D_BOOST` — non-Enhanced engines require `$T_BOOST,0` and `$D_BOOST` ≤ 5 m | [VBD](../../glider-components/seaglider/vbds/index.md) |
| Battery | Correct type installed; check derating and storage history | [Batteries](../../glider-components/seaglider/batteries/index.md) |
| Sensor protective covers | Removed before launch (refit on recovery) | [Recovery Checklist](../../recovery/seaglider/checklists/seaglider-recovery-checklist.md) |

## After Every Recovery

| Item | Action | Detail |
|---|---|---|
| Rinse | Whole glider and all sensors, fresh water | [Recovery Checklist](../../recovery/seaglider/checklists/seaglider-recovery-checklist.md) |
| Travel mode | Set via `hw/misc/travel` before packing for transport | [Recovery Checklist](../../recovery/seaglider/checklists/seaglider-recovery-checklist.md) |
| Rudder and wings | Removed for transport | [Recovery Checklist](../../recovery/seaglider/checklists/seaglider-recovery-checklist.md) |
| Visible damage | Inspect and photograph as-recovered condition before anything else is touched | [Recovery Checklist](../../recovery/seaglider/checklists/seaglider-recovery-checklist.md) |
| Basestation | Move mission data into its mission directory; complete the dive log | [Recovery Checklist](../../recovery/seaglider/checklists/seaglider-recovery-checklist.md) |

## Periodic / Condition-Based

| Item | Interval / trigger | Detail |
|---|---|---|
| Compact flash root directory | ≈1365 dives (4096-file limit) — run `usage` / `del` via `pdoscmds.bat` from around dive 1000 onward | [Dive Cycle & Control Files](../../piloting/seaglider/dive-cycle-and-control-files.md) |
| Compass | Degauss a suspect (magnetized) battery pack if calibration won't converge | [Compass Calibration](../../piloting/seaglider/compass-calibration.md) |

## Storage

- Store batteries in original packaging, dry and ventilated, ideally ≤ 23 °C, segregated by state of charge — see [Batteries](../../glider-components/seaglider/batteries/index.md).
- Set the glider to **travel mode** before extended storage or shipping.
