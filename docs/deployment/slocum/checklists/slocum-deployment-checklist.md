---
title: Slocum Deployment Checklist
description: Slocum glider deployment checklist covering pre-deployment, on-deck operations, in-water checks, and first-day monitoring.
---

# Slocum Deployment Checklist

[Print this page :material-printer:](#){ .print-button onclick="window.print(); return false;" }

---

**Deployment mission:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; **Glider S/N:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_

**Engineer:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; **Date:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## 1. Pre-Deployment

- [ ] Archive deployment on SFMC
- [ ] Cache files
- [ ] Test remote comms &emsp;<small>*Cell / Iridium Go / Iridium handset*</small>
- [ ] Remote team confirms local testing done
- [ ] Remote team relays glider turnaround plan and ETA
- [ ] IMS movements confirmed

**MicroRider** *(if fitted)*

- [ ] MR — Check probe capacitance/resistance with multimeter/Gigaohm-meter
- [ ] MR — Check `SETUP.CFG` (serial numbers, cal constants, file names: `D_*.P`)
- [ ] MR — Bench test with **test probes**; check P-file creation and logfile for errors &emsp;<small>`odas5ir -f setup.cfg -c all`</small>
- [ ] MR — Check/set date and time
- [ ] MR — *(optional)* Bench test with **mission probes**; check P-file and logfile; reinstall test probes after
- [ ] MR — Check probe ports (greased O-ring, ferrule OK)
- [ ] MR — Check all screws, bolts, and connectors are firm/tight

**Final pre-deployment**

- [ ] *(optional)* Run a simulation; check all files and data
- [ ] Download all relevant glider/sensor files and build the final Expedition folder; send to office/SharePoint &emsp;<small>`*.ma, *.mi`, config files (science and flight), MicroRider `SETUP.CFG`</small>

---

## 2. On Deck

- [ ] Note deployment time &emsp;<small>*Ensure remote team has unplugged Freewave*</small>
- [ ] Stop `initial.mi` &emsp;<small>`Ctrl-C` × 2</small>
- [ ] Increase time in GliderDOS &emsp;<small>`put u_max_time_in_gliderdos 3600`</small>
- [ ] *(optional)* Pull engineering config files &emsp;<small>`zs config/autoexec.mi` &ensp; `zs config/sbdlist.dat`</small>
- [ ] *(optional)* Pull science config files &emsp;<small>`szs /config/proglets.dat` &ensp; `szs config/tbdlist.dat`</small>
- [ ] Confirm vanilla mission and `.ma` files are present &emsp;<small>*(optionally type `send off` or `send on`)*</small>
- [ ] Send new `goto` and any new files &emsp;<small>`dockzr *.*`</small>

**MicroRider** *(if fitted)*

- [ ] MR — Install mission probes &emsp;<small>*confirm probes installed by remote team*</small>
- [ ] MR — On-deck calibration; fill ChanStats checklist; check for broken probes &emsp;<small>`u4stalk`, then `odas5ir -f setup.cfg -c all`</small>

**Status checks**

- [ ] Run `status.mi` &emsp;<small>`run status.mi`</small>
- [ ] Confirm `status.mi` completes normally — no aborts, or any aborts understood and resolved
- [ ] Confirm GPS location; send SBD/TBD; check age of GPS fix
- [ ] Plot engineering and science data &emsp;<small>`send *.sbd *.tbd`</small>
- [ ] Confirm engineering data in DataVisualizer
- [ ] Confirm science data in DataVisualizer &emsp;<small>*battery · vacuum · time · GPS position · leak detectors*</small>
- [ ] Confirm devices show no unusually high number of warnings or oddities
- [ ] Communicate to remote team: glider is OK / not OK to deploy &emsp;<small>*From this point the **pilot team** is responsible for control of the glider*</small>

---

## 3. In Water

- [ ] Remote team confirms glider is deployed and is on/off buoy
- [ ] Run `status.mi` &emsp;<small>`run status.mi`</small>
- [ ] Confirm surface dialog engineering data &emsp;<small>*battery · vacuum · time · GPS position · leak detectors*</small>
- [ ] Confirm no aborts
- [ ] Zero ocean pressure &emsp;<small>`zero_ocean_pressure`</small>

**MicroRider** *(if fitted)*

- [ ] MR — Surface calibration; fill ChanStats checklist; check for broken probes &emsp;<small>`u4stalk` using `ctrl-F`, then `odas5ir -f setup.cfg -c all`</small>
- [ ] MR — Send calibration data to Rockland support &emsp;<small>*copy calibration text from terminal*</small>

**Initial dive sequence**

- [ ] Run `ini0.mi` (on buoy preferred) &emsp;<small>`run ini0.mi`</small>
- [ ] Send MDB &emsp;<small>`send *.mbd -num=1`</small>
- [ ] Send all SBD and TBD (should be `ini0` and `status` only) &emsp;<small>`send *.sbd *.tbd`</small>
- [ ] Exit reset and catch glider on connection &emsp;<small>`exit reset`</small>
- [ ] Confirm ballast — dive/climb profile should be a clean V-shape &emsp;<small>*if not, use drive calculator*</small>
- [ ] If not V: inform field crew of weights to add/remove and repeat `ini0`
- [ ] If ballast OK: notify crew to remove buoy
- [ ] Once glider is free: sequence mission &emsp;<small>`Sequence mission.mi(5)` *(or expedition-specific mission name)*</small>
- [ ] Confirm first vanilla mission dive depth is 30 m
- [ ] Confirm script is running &emsp;<small>`SFMC-g3s-ma-first-num=3.xml`</small>

**MicroRider** *(if fitted — after first dive)*

- [ ] MR — Surface calibration after first dive; fill ChanStats checklist
- [ ] MR — Check MicroRider memory: confirm increasing data files and growing log size &emsp;<small>`dir \DATA\D*.P` &ensp; `dir \DATA\logfile.txt`</small>
- [ ] MR — Mid-profile channel analysis from `.tbd` data; fill ChanStats checklist (mid-profile) &emsp;<small>*reference: TN_048, ChanStat*</small>
- [ ] MR — Send data to Rockland support &emsp;<small>*calibration text + `.tbd`/`.sbd` converted data (`.dat` ASCII) + logfile*</small>

**Depth ramp-up**

- [ ] Adjust dive depth and altitude incrementally &emsp;<small>*typical sequence: 100 → 300 → 600 → 990 m (edit `yo35.ma`)*</small>
- [ ] Adjust autoballast values as appropriate
- [ ] *(optional)* Toggle current correction in surface dialog &emsp;<small>`!put u_use_current_correction 0`</small>
- [ ] Notify field crew that glider is on mission and diving to full depth

---

## 4. Remainder of Day 1

- [ ] Email BODC with deployment time and location
- [ ] *(optional)* Increase number of half yos
- [ ] Increase surface interval / no-comms count once navigation, data retrieval, and nominal operation are confirmed
- [ ] Adjust engineering data density as desired &emsp;<small>edit `sbdlist.dat` (restart mission)</small>
- [ ] Adjust science data density as desired &emsp;<small>edit `tbdlist.dat` (send to science)</small>
- [ ] Compare actual results against campaign plan; verify with lead pilot that all requirements are being met
- [ ] Subscribe to abort SMS/calls &emsp;<small>*GliderLab*</small>
- [ ] Set SFMC email subscriptions &emsp;<small>*glider page → Options → Configure Glider Event Subscriptions*</small>
- [ ] Adjust altimeter minimum depth &emsp;<small>e.g. `!put u_alt_min_depth 40` to enable altimeter at 40 m and deeper</small>

**MicroRider** *(if fitted)*

- [ ] MR — Repeat MicroRider channel checks periodically (2–3× per deployment day)

---

## 5. Day 2 and Beyond

- [ ] Complete daily pilot log and post to C2 &emsp;<small>`SLC-CL-PLT05 Pilot log checklist.xlsx`</small>
- [ ] Confirm deployment-specific criteria are being satisfied: energy budget · science requirements · navigation requirements

**MicroRider** *(if fitted)*

- [ ] MR — Repeat probe capacitance check (MR1) once per week
- [ ] MR — Repeat TBD data channel analysis (MR2) once per day
- [ ] MR — Repeat mid-profile channel stats (MR3) when in doubt about probe health

---

## Sign-Off

| Phase | Completed by | Time (UTC) | Notes |
|---|---|---|---|
| Pre-Deployment | | | |
| On Deck | | | |
| In Water — first dive | | | |
| Depth ramp-up complete | | | |

---

*Slocum Deployment Checklist — v1.2 · Adapted from NOC/Voice of the Ocean Slocum deployment checklist*
