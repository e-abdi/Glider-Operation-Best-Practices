---
title: Slocum Maintenance Schedule
description: What to check before every deployment, after every recovery, and on its own schedule — a Slocum G3 maintenance overview organised by timing rather than by component.
---

# Slocum Maintenance Schedule

This page organizes maintenance by **when** it needs doing, not by which
component it touches — the detailed how-to for each item lives on the
relevant [Glider Components](../../glider-components/slocum/index.md) page
or checklist; this is the index that tells you when to go read it.

!!! info "Source"
    Synthesized from facts already established across this site's Slocum
    component pages, the [Post-Recovery Maintenance Checklist](../../recovery/slocum/checklists/post-recovery-maintenance-checklist.md),
    and the [Ballasting Procedure](../../ballasting/slocum/ballasting-procedure.md)
    — see those pages for sourcing and full detail.

---

## Before Every Deployment

| Item | What to confirm | Detail |
|---|---|---|
| Vacuum | ≥ 6 in Hg (shallow) / ≥ 7 in Hg (deep) — never power up without it | [One-Pager](../../lab-test/guides/slocum-one-pager.md) |
| O-rings | Inspect every hull O-ring and sealing surface; replace as needed | [O-Rings](../../glider-components/slocum/o-rings/index.md) |
| Desiccant | Fresh pack installed for this deployment | [O-Rings](../../glider-components/slocum/o-rings/index.md) |
| Sacrificial anodes | Forward/aft continuity < 10 Ω; replace if significantly consumed | [Post-Recovery Checklist](../../recovery/slocum/checklists/post-recovery-maintenance-checklist.md) |
| Battery | Correct type installed and charged; coulomb counter reset if new pack | [Primary](../../glider-components/slocum/batteries/primary/index.md) · [Rechargeable](../../glider-components/slocum/batteries/rechargeable/index.md) |

## After Every Recovery

!!! danger "Rinse after every saltwater exposure"
    Fresh water on the whole glider, the tail fin/rudder, the pressure
    transducer, and the CTD/science sensors — salt left to dry promotes
    corrosion and can inhibit moving parts on the next power-up.

| Item | Action | Detail |
|---|---|---|
| Full rinse | Whole glider, fin, pressure transducer, science sensors | [Post-Recovery Checklist](../../recovery/slocum/checklists/post-recovery-maintenance-checklist.md) |
| Thruster *(if fitted)* | Remove hub (7/64 hex), rinse, re-grease with MoS₂, replace hub | [Thruster](../../glider-components/slocum/thruster/index.md) |
| Digifin / fin | Rinse; check for fouling or a stuck/noisy fin | [Digifin](../../glider-components/slocum/digifin/index.md) |
| External inspection | Hull, anodizing/paint, wet-mate connectors, air bladder, recovery lanyard | [Post-Recovery Checklist](../../recovery/slocum/checklists/post-recovery-maintenance-checklist.md) |
| Leak-detect voltages | Confirm within normal range | [Post-Recovery Checklist](../../recovery/slocum/checklists/post-recovery-maintenance-checklist.md) |

## Periodic / Condition-Based

These don't happen every deployment — they're driven by cycle counts,
symptoms, or a fixed interval.

| Item | Interval / trigger | Detail |
|---|---|---|
| Shallow buoyancy pump | 10,000-cycle service life | [Shallow Pump](../../glider-components/slocum/pumps/shallow-pump/index.md) |
| Deep buoyancy pump | Service when oil-flux troubleshooting indicates wear | [Deep Pump](../../glider-components/slocum/pumps/deep-pump/index.md) |
| O-ring open policy | Primary batteries: every open (i.e. every mission). Rechargeable: commonly once a year | [O-Rings](../../glider-components/slocum/o-rings/index.md) |
| Compass | Degauss a suspect (magnetized) battery pack if calibration won't converge | [Compass](../../glider-components/slocum/compass/index.md) |
| Software updates | Read the release's `readme.txt` before updating | [One-Pager](../../lab-test/guides/slocum-one-pager.md) |

## Storage

- Recharge or otherwise service batteries as planned before shelving.
- Confirm desiccant is installed and the glider is sealed with a proper vacuum.
- Store at **+10 to +25 °C** for optimum battery life.
- If crating, use all straps and secure cylindrical parts so they can't roll.

See the [Post-Recovery Maintenance Checklist](../../recovery/slocum/checklists/post-recovery-maintenance-checklist.md#10-storage-preparation) for the full storage-prep checklist.
