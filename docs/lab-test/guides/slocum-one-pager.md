---
title: Slocum One-Pager
description: Quick-reference notes and commands for Slocum glider lab operations.
---

# Slocum One-Pager

Quick-reference notes for common Slocum operations. This page grows over time — add notes as new important reminders are identified.

---

## Power-up

!!! danger "Never power up a shallow glider without a vacuum."

---

## External Power

!!! danger "Never power on a glider with more than 16.3 VDC from an external power supply."

---

## Powering Down

!!! danger "Never pull the green plug or external power without first issuing `exit` and getting the glider's confirmation — it can corrupt the file system."

    If the emergency battery is left latched (main battery disconnected without a clean `exit`), the BMS board sounds a buzzer until the glider is powered back up and exited properly.

---

## Lab-Only Modes

!!! danger "Never deploy a glider that is still in `lab_mode`."

!!! danger "Never exit to Pico on a deployed glider."

---

## Air Bladder Before Disassembly

!!! warning "Deflate the air bladder (`put c_air_pump 0`) before disassembling the glider."

---

## Sealing Surfaces

!!! warning "Keep hull sealing surfaces and O-ring grooves free of debris and sharp tools — damage means a leak risk and a mandatory pressure test before the glider is operational again."

---

## G2 vs. G3 O-Rings

!!! note "G2 and G3 hull O-rings are not interchangeable — a G2 ring (G-024) will not close a G3 hull (304697)."

---

## CTD Dry-Run Limit

!!! warning "Never run the pumped CTD (Seabird SBE) dry for more than 30 seconds at a time."

---

## Software Updates

!!! warning "Always read the release's `readme.txt` before updating glider software — and simulate afterward if possible."

---

!!! info "Source"
    Paraphrased from the *Slocum G3 Glider Operators Manual*, the *Slocum G3
    Glider Maintenance Manual*, and the Teledyne Webb Research user forum.
    Always defer to the official Teledyne documentation for your specific
    glider.
