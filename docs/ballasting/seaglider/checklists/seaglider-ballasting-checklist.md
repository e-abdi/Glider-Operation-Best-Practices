---
title: Seaglider Ballasting Checklist
description: Printable tank-ballasting checklist for the Seaglider.
---

# Seaglider Ballasting Checklist

[Print this page :material-printer:](#){ .print-button onclick="window.print(); return false;" }

---

**Mission:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; **Seaglider ID:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_

**Engineer:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; **Date:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

!!! info "Source"
    Paraphrased from the APL-UW IOP office-hours session on ballasting and
    volmax estimation and from operator service correspondence. See the
    [Ballasting Procedure](../ballasting-procedure.md) and
    [Trim Sheet & Re-ballasting](../trim-sheet-and-reballasting.md) for the
    full explanation of each step.

---

## 1. Setup

- [ ] Trim sheet updated for every change since last ballast (sensors, batteries, VBD, fairings, wings/rudder)
- [ ] Target density for the mission written into the trim sheet — and checked if the glider just came back from service
- [ ] Lead and foam inventoried: each piece weighed, position noted, every hull face photographed
- [ ] Wings and rudder weighed; set fitted recorded
- [ ] Freshwater tank filled, deep enough to fully submerge the glider vertically (≥ ~2 m)
- [ ] Hanging scale / load cell rigged over the tank
- [ ] Suspension line ready (ties off at the rudder)
- [ ] Comms cable available and connected, with slack — no surface expression
- [ ] Antenna left disconnected and dangling free

## 2. Dry Weight

- [ ] Complete glider (wings, rudder, everything) weighed dry — record mass **M**
- [ ] **M** compared with the trim sheet's summed mass — difference: \_\_\_\_\_\_ g (tens of grams OK; hundreds = find the error)
- [ ] Glider soaked overnight, fully submerged and vertical, in the tank

## 3. Tank Density

- [ ] Tank temperature recorded (and salinity, if not freshwater)
- [ ] Tank water density computed

## 4. Weight-in-Water at Multiple VBD Positions

- [ ] Weighed in water at ≥ 5 VBD positions (e.g. 2000 / 2250 / 2500 / 2750 / 3000 counts)
- [ ] `volmax` computed at each position
- [ ] All values agree to within ~±5–10 cc (outliers re-checked)
- [ ] Average `volmax` recorded: \_\_\_\_\_\_\_\_\_\_ cc

## 4b. Neutral-Point Trim Test (if used)

- [ ] Predicted `$C_VBD` / `$C_PITCH` for tank density taken from the trim sheet
- [ ] VBD stepped to neutral mid-water, pitch to level, roll swept and centred
- [ ] Observed `$C_VBD` \_\_\_\_\_\_ &emsp; `$C_PITCH` \_\_\_\_\_\_ &emsp; `$C_ROLL` \_\_\_\_\_\_ recorded with tank density
- [ ] Trim sheet calibrated to the observed centers ("mystery mass")

## 5. Weight Adjustment

- [ ] Target thrust and target deployment density entered into the vis Ballast worksheet
- [ ] Lead added/removed per the worksheet's recommendation
- [ ] Maximum thrust in target water checked — aim for ~250–300 cc
- [ ] Pitch-mass stroke near nominal (~70 %) after lead changes
- [ ] `$MASS`, `$C_VBD`, `$C_PITCH` updated on the glider and in `sg_calib_constants.m`
- [ ] ±100 cc uncertainty accounted for in the deployment plan

## 6. Before First Water Time

- [ ] Spare foam, lead and tools packed for on-deck adjustment; crew briefed
- [ ] First dive planned as a **tethered** / on-a-line test
- [ ] First mission is shallow, enclosed, and local — not open-ocean or deep
- [ ] Post-tank weight/volmax figures logged for this glider

---

**Notes:**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

| Role | Name | Signature | Date |
|---|---|---|---|
| Ballasted by | | | |
| Checked by | | | |
