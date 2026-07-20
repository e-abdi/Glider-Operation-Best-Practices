---
title: Slocum Ballasting Checklist
description: Printable tank-ballasting checklist for the Slocum G3 glider.
---

# Slocum Ballasting Checklist

[Print this page :material-printer:](#){ .print-button onclick="window.print(); return false;" }

---

**Mission:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; **Glider S/N:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_

**Engineer:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; **Date:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

!!! info "Source"
    Paraphrased from the *Slocum G3 Glider Maintenance Manual* (Chapter 3,
    "Ballasting"). See the [Ballasting Procedure](../ballasting-procedure.md)
    for the full explanation of each step.

---

## 1. Before Powering Up

- [ ] Glider closed with a proper vacuum — ≥ 6 in Hg shallow / ≥ 7 in Hg deep
- [ ] PEEK MS plug torqued to 15 in-lb
- [ ] Ballast tank filled, large enough to fully submerge the glider, and a way to lift it in/out confirmed

## 2. Setting Ballast Mode

- [ ] Power the glider (external 15 VDC or green go-plug)
- [ ] If in PicoDOS: `app` to start GliderDOS
- [ ] `Ctrl-C` to gain control
- [ ] `callback 30`
- [ ] `lab_mode on`
- [ ] `ballast` — confirm pump/pitch vernier at 0 and bladder deflated
- [ ] Science sensors live for tank density (`loadmission sci_on.mi` or the `c_science_*` puts)

## 3. Immersing the Glider

- [ ] Wings fitted (or taped to the aft hull if the tank is too small)
- [ ] All trapped air purged from nose cone and aft cover
- [ ] HD (deep) pump: extra care taken to clear entrapped air

## 4. Weight Adjustment

- [ ] Tank temperature/conductivity read and density calculated
- [ ] Target (deployment) water temperature and density entered in the Ballast Adjustment Spreadsheet
- [ ] Weight added/removed (external or internal) toward the spreadsheet's target
- [ ] If too heavy: spring-scale check at fore/aft end caps done before removing weight
- [ ] Neutral buoyancy confirmed in the tank at the reference state (0 cc pump / 0 in pitch / 0° roll / bladder deflated)

## 5. H-Moment

- [ ] H-moment measured (`report ++ m_pitch m_battpos`, or wing-mass roll-response method) — only needed on initial ballast or after a configuration change
- [ ] H-moment within 4–7 mm (5–6 mm ideal; toward 7 mm if running a thruster)
- [ ] Roll weights adjusted as needed and re-measured

## 6. Close-Out

- [ ] Exit `ballast` / `lab_mode`; confirm glider is back on a normal mission before deployment
- [ ] Glider re-sealed with proper vacuum on the final close (not just a working ballast open)
- [ ] Weight/H-moment changes logged for this glider

---

**Notes:**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

| Role | Name | Signature | Date |
|---|---|---|---|
| Ballasted by | | | |
| Checked by | | | |
