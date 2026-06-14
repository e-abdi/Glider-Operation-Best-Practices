---
title: Slocum Piloting Checklist
description: Daily Slocum pilot log — the values and checks a pilot records each piloting day (from the glider dialog and SFMC).
---

# Slocum Piloting Checklist

[Print this page :material-printer:](#){ .print-button onclick="window.print(); return false;" }

A daily pilot log. Work down the list each piloting day, recording the value from
the indicated source and flagging anything outside its normal range.

---

**Pilot:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; **Glider S/N:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; **Date (UTC):** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_

---

!!! tip "First piloting day of a deployment"
    Confirm **Science** and **Navigation** against the campaign plan, and create a
    new *important* log entry with a fresh campaign summary for reference.

---

## Status & Identity

<small>*Source: glider dialog unless noted.*</small>

- [ ] **Date**
- [ ] **Last surface reason**
- [ ] **Current mission**
- [ ] **Mission time** &emsp;<small>*paste the seconds timestamp; glider aborts for overtime every **45 days***</small>
- [ ] **GPS location**
- [ ] **Next surfacing is in** &emsp;<small>*estimated from glider history*</small>

---

## Navigation

- [ ] **Performance of navigation last leg** &emsp;<small>*are we headed to the desired waypoint?*</small>
- [ ] **Navigation to / why** &emsp;<small>*which waypoint are we going to, and potentially why*</small>

!!! note
    If the waypoint is **not** part of the campaign plan, update the campaign plan.

---

## Devices & Altimeter

- [ ] **Devices** &emsp;<small>*from SFMC — are any devices in error?*</small>
- [ ] **Altimeter** &emsp;<small>*is it seeing bottom, and at what depth is it turning on?*</small>
- [ ] **Number of yos and depth** &emsp;<small>*from SFMC*</small>

!!! note
    If the in-water navigation has changed from the campaign plan, update the plan.

---

## Science

- [ ] **Science** &emsp;<small>*is science data coming back when and how expected for the sensors below — or changed?*</small>
- [ ] **CTD** &emsp;<small>*compare against campaign plan*</small>
- [ ] **Sensor 1** \_\_\_\_\_\_\_\_\_\_ &emsp;<small>*name the sensor and compare against campaign plan*</small>
- [ ] **Sensor 2** \_\_\_\_\_\_\_\_\_\_ &emsp;<small>*name the sensor and compare against campaign plan*</small>
- [ ] **Sensor 3** \_\_\_\_\_\_\_\_\_\_ &emsp;<small>*name the sensor and compare against campaign plan*</small>
- [ ] **Sensor 4** \_\_\_\_\_\_\_\_\_\_ &emsp;<small>*name the sensor and compare against campaign plan*</small>

!!! note
    - If science sampling needed to be changed, update the campaign plan.
    - At least once a week, confirm the sampling of **all** science sensors against the Science Campaign plan.

---

## Mission Script & Power Modes

- [ ] **Script** &emsp;<small>*copy from terminal*</small>
- [ ] **Current correction** &emsp;<small>*on or off, from dialog*</small>
- [ ] **Lower power mode** &emsp;<small>*off, or the value in use, from glider dialog*</small>

!!! note
    If the script needs to change or is having difficulty, add a comment to
    **Notes** below and include it in the handover / notification to the lead pilot.

---

## Energy & Consumption

<small>*Comment if too high or too low.*</small>

- [ ] **Consumption**
- [ ] **`m_lithium_battery_relative_charge` (%)**
- [ ] **`m_coulomb_amphr_total` (amp-hrs)**
- [ ] **Expected end date** &emsp;<small>*at 80% and 100%*</small>

---

## Health & Vacuum

- [ ] **`m_vacuum`** &emsp;<small>*from glider dialog — typically 8–11*</small>
- [ ] **Leak-detect voltages** &emsp;<small>*from glider dialog — typically 2.4–2.5*</small>
- [ ] **Battery surface voltage** &emsp;<small>*from glider dialog*</small>
- [ ] **Battery min voltage** &emsp;<small>*record and compare against history, looking for outlying results*</small>
- [ ] **Battery max voltage** &emsp;<small>*record and compare against history, looking for outlying results*</small>

---

## Flight & Ballast

- [ ] **Dive profiles symmetric** &emsp;<small>*True / False — if false, how and why*</small>
- [ ] **Autoballast converged** &emsp;<small>*True / False — if false, how and why; add climb and dive CC here*</small>
- [ ] **`m_avg_speed`** &emsp;<small>*from glider dialog — watch for trend changes*</small>
- [ ] **Pitch / Roll** &emsp;<small>*from SFMC — watch for trend changes*</small>
- [ ] **Battpos** &emsp;<small>*from SFMC — watch for trend changes*</small>

---

## Campaign & Notes

- [ ] **Has the campaign plan changed and been updated?** &emsp;<small>*why and what? Campaigns can change for PI / distress / feature / other*</small>

    !!! note
        If yes — update the **Campaign Log** and *mark important*.

- [ ] **Notes** &emsp;<small>*free-form — anything we need to keep an eye on?*</small>

    !!! note
        If there is a concern, notify the lead pilot(s), add it to the handover email, or both.

- [ ] **Weather** &emsp;<small>*wave and wind speed and direction (e.g. from Windy)*</small>
- [ ] **Obstacles** &emsp;<small>*ice edge, shallows, shelf edge, etc. — piloting concerns that might lead to a change of mission or campaign*</small>

---

!!! info "Saving this log"
    - Make sure the location of this log is referenced in the **handover email** and the **campaign plan**.
    - If highly customised for a particular campaign, save a new template of the log to the expedition's folder.
    - Typically a pilot saves this template locally and fills it out each day.
