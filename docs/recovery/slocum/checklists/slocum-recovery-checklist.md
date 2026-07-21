---
title: Slocum Recovery Checklist
description: Printable recovery checklist for the Slocum G3 glider, covering both the remote-pilot and field-team sides of a nose recovery.
---

# Slocum Recovery Checklist

[Print this page :material-printer:](#){ .print-button onclick="window.print(); return false;" }

---

**Mission:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; **Glider S/N:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_

**Pilot / Engineer:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; **Date:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

!!! info "Source"
    Paraphrased from NorGliders / University of Bergen (UiB) field
    procedure notes (SL04, SL11, SL12). See the
    [Field Recovery Procedure](../field-recovery-procedure.md) and
    [Remote Pilot Recovery Procedure](../remote-pilot-recovery-procedure.md)
    for the full explanation of each step.

---

## 1. Pre-Recovery Coordination

- [ ] Field team arrival time, recovery time, and schedule-change likelihood discussed with the remote pilot
- [ ] Communication method and position-update frequency agreed
- [ ] Glider configuration confirmed &emsp;<small>*call-in interval, strobe*</small>

## 2. Remote Pilot — Set to Drift

- [ ] Glider caught on the surface; surfacing interval shortened
- [ ] XML script disabled in SFMC
- [ ] `u_max_time_in_gliderdos` set for the expected drift duration
- [ ] `put c_de_oil_vol 420` — max buoyancy
- [ ] `strobe on` *(unless broad daylight)*
- [ ] Field team receiving regular GPS position updates

## 3. Field Team — Organize the Deck

- [ ] Grapple on 20 m line, boathook, glider cart staged
- [ ] Transport case opened, latches flattened
- [ ] Communication with remote pilot confirmed for glider position

## 4. Deploy Nose Recovery Line

- [ ] Remote pilot sends `put c_recovery_on 1` when field team is ~10 min out or has visual contact
- [ ] Nose release confirmed &emsp;<small>*can take up to 10 min to unravel*</small>
- [ ] If not released after 10 min: retry command, boat-hook tap, or shallow dive test (see Remote Pilot procedure troubleshooting)

## 5. Recovery

- [ ] Vessel approached glider from downwind
- [ ] Line grappled/hooked and hauled in; overhand knot tied and attached to A-frame/crane
- [ ] Glider lifted nose-first out of the water
- [ ] Glider lowered onto cart, nose into ring-mount, strap secured
- [ ] Wings removed
- [ ] *(If nose system failed)* Backup workboat recovery used — see Field Recovery Procedure

## 6. Shutdown (Remote Pilot)

- [ ] Glider positioned with clear view of sky; pilot notified
- [ ] `put c_air_pump 0` — air bladder deflated
- [ ] `put c_de_oil_vol -420` — ballast pump retracted; `get m_de_oil_vol` confirms −420
- [ ] `exit` — glider shut down
- [ ] UTC shutdown time recorded and passed to field team

## 7. Stowing (Field Team)

- [ ] **Within 30 minutes of shutdown:** green plug removed, red plug installed
- [ ] Glider placed in transport case, cart legs seated correctly
- [ ] Both ratchet straps fastened, lid replaced

---

## Sign-Off

| Phase | Completed by | Time (UTC) | Notes |
|---|---|---|---|
| Set to drift | | | |
| Nose recovery deployed | | | |
| Glider aboard | | | |
| Shutdown complete | | | |
| Stowed | | | |

---

**Notes:**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
