---
title: Slocum Deployment Checklist
description: Slocum glider deployment checklist covering startup, systems checks, pre-launch prep, launch, and in-water test dives.
---

# Slocum Deployment Checklist

[Print this page :material-printer:](#){ .print-button onclick="window.print(); return false;" }

---

**Deployment mission:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; **Glider S/N:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_

**Engineer:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; **Date:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

!!! info "Source"
    Paraphrased from a NorGliders / University of Bergen (UiB) field-pilot
    deployment logsheet (*SL05 — G3 Deployment Field Pilot*). Expected sensor
    ranges are UiB operating norms — confirm against your own glider's
    baseline.

---

## 1. Startup

- [ ] Contacts clean and greased; go plug inserted
- [ ] `^c` &emsp;<small>*gain control of the glider*</small>
- [ ] `callback 30`
- [ ] `lab_mode on`
- [ ] `report clearall`
- [ ] `where` &emsp;<small>*record `m_veh_temp`, `m_vacuum`, `m_battery`*</small>
- [ ] Confirm BMS currents are non-zero &emsp;<small>*`m_bms_aft_current`, `m_bms_ebay_current`, `m_bms_pitch_current`*</small>
- [ ] `boot app` → `consci` → `boot app` → `quit` &emsp;<small>*cycle both processors up*</small>
- [ ] `simul?` and `dir config` — confirm `simul.sim` is **not** present in `\config`

## 2. Motor Check

- [ ] `use` &emsp;<small>*review device list*</small>
- [ ] `wiggle on`, `report ++ m_battpos m_fin m_de_oil_vol` — leave 5 min
- [ ] `use` again — record any oddities, warnings, or errors, and confirm motors moved their full ranges &emsp;<small>`m_de_oil_vol` −415 : 415 cc · `m_battpos` −0.9 : 0.9 in · `m_fin` −0.45 : 0.45 rad</small>
- [ ] `wiggle off`
- [ ] `ballast`
- [ ] `report clearall`
- [ ] `lab_mode off`

## 3. GPS Check

- [ ] `put c_gps_on 3` — confirm a fix (`where`, or the `V`→`A` flag in the data stream; a fresh almanac can take several minutes)
- [ ] `put c_gps_on 1`
- [ ] `sync_time`

## 4. Mission Settings & Onboard Status

- [ ] Test-dive mission file staged (e.g. `yo14.ma`: `num_half_cycles_to_do` 2 · `d_target_depth` 10–20 m · `d_bpump_value` 500–600 cc · `d_target_altitude` > 15 m · pitch mode 3, `±0.4538`)
- [ ] `surfac21.ma` `when_secs` set (e.g. 1200 s)
- [ ] `goto_l10.ma` staged — initial waypoint lat/lon recorded and given to the skipper
- [ ] `run status.mi` completes **normally** &emsp;<small>*a `surface_2` timeout on `m_raw_altitude` while on the bench is expected and OK*</small>
- [ ] GPS fix acquired; Iridium connects after the mission
- [ ] `callback 30` → `use` → `send *.*` → data processes successfully
- [ ] `callback 0 0` — confirm **modem** connection in SFMC
- [ ] `callback 1 0` — confirm **RUDICS** connection in SFMC
- [ ] `where` — `m_vacuum` **> 9 in Hg**; `get m_de_oil_vol` **> 415 cc**; `get m_battpos` **> 0.9 in**
- [ ] Air bladder filled and pitch battery all the way forward

!!! danger "Do not deploy until Iridium connections are verified."

**MicroRider** *(if fitted)* — mounted securely, MCIL-8-FS cable connected,
sensors installed with serial numbers/orientation recorded, bench-calibrated
(`odas5ir -c all`) and 60 s bench-tested with a review of the resulting
statistics.

## 5. Prepare for Launch

- [ ] Wings attached securely, Phillips screw fastened
- [ ] CTD, DO, and other sensor covers removed
- [ ] Floats attached and line organized *(if used)*
- [ ] Trolley front ring and securing strap removed
- [ ] OK received from the skipper
- [ ] Release system prepared

!!! danger "Before the glider goes in the water, confirm all three:"
    - [ ] **Not** in `lab_mode` (`lab_mode off`)
    - [ ] **Not** in simulation — `simul.sim?` gets no reply
    - [ ] Set to `boot app` (`boot app`) — keep sending a keystroke to the glider to stop it from booting a mission early

- [ ] `callback 10`, then **launch the glider**

## 6. In Water

- [ ] Glider sitting correctly in the water
- [ ] `where` — record leak-detect voltages &emsp;<small>`m_leakdetect_voltage_forward` > 2.4 · `m_digifin_leakdetect_reading` > 1018 · `m_vacuum` > 9</small>
- [ ] `run status.mi` — GPS fix acquired, mission completes normally
- [ ] `callback 0 0` — confirm modem connection; `callback 0 1` — confirm RUDICS connection

## 7. Science Check

- [ ] `loadmission sci_on.mi` — all sensors reporting reasonable values, no oddities
- [ ] `loadmission sci_off.mi`

## 8. Test Dives

- [ ] **Test dive 1** — depth 10–15 m, ~10 min (`when_secs` ≈ 1200s) — `run <mission>.mi` completes normally; record surfacing behaviour, max depth, dive/climb pitch angle, roll, science data
- [ ] Floats removed, if fitted
- [ ] **Test dive 2** — depth 30–50 m, ~20 min (`when_secs` ≈ 1800s) — edit `yo14.ma` / `surfac21.ma` for the deeper dive before running
- [ ] Depth increased incrementally on subsequent dives once the glider is flying cleanly

---

## Sign-Off

| Phase | Completed by | Time (UTC) | Notes |
|---|---|---|---|
| Startup & systems check | | | |
| Prepared for launch | | | |
| In water — first dive | | | |
| Test dive 2 complete | | | |

---

**Notes:**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
