---
title: Post-Recovery Maintenance Checklist
description: Maintenance steps to perform on a Slocum G3 glider after recovery from a saltwater deployment — rinsing, inspection, anode and O-ring care, desiccant, and storage prep.
---

# Post-Recovery Maintenance Checklist

[Print this page :material-printer:](#){ .print-button onclick="window.print(); return false;" }

Maintenance to carry out on a Slocum G3 glider after recovery. Work through it
as soon as practical after the glider is out of the water — salt left to dry
promotes corrosion and can inhibit moving parts on the next power-up.

!!! info "Source"
    Compiled from the *Slocum G3 Glider Operators Manual* (Rev. 1) and the
    *Slocum G3 Glider Maintenance Manual* (Rev. A). Defer to the official
    Teledyne documentation for your specific glider configuration.

---

**Glider S/N:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; **Mission:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; **Date (UTC):** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_

**Engineer:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## 1. On Deck / Immediately After Recovery

- [ ] Secure the glider on its cart or cradle &emsp;<small>*never leave it where it can roll off a surface*</small>
- [ ] Note recovery date/time and final GPS position
- [ ] Power down the glider properly **before** removing the green plug

!!! warning "Deflate the air bladder before removing the aft tail cowling"
    With the cowling off, the bladder is unsupported and can over-inflate.
    Deflate it first: `put c_air_pump 0` to open the solenoid and release the
    external bladder.

---

## 2. Data & Power

- [ ] Offload all engineering and science data from the glider
- [ ] Record final energy state &emsp;<small>`m_coulomb_amphr_total`, `m_lithium_battery_relative_charge`, battery voltage</small>
- [ ] Plan battery action &emsp;<small>*rechargeable packs turn themselves off at 10 V — recharge before storage (see Batteries → Rechargeable)*</small>

---

## 3. Fresh-Water Rinse

!!! danger "Rinse after every saltwater exposure"
    Rinse the glider with fresh water every time it is exposed to salt water.
    Salt crystals promote corrosion and can inhibit moving parts on the next
    power-up.

- [ ] Rinse the **whole glider** with fresh water
- [ ] Rinse the **tail fin / rudder** thoroughly &emsp;<small>*prevents salt crystals from inhibiting fin motion next power-up*</small>
- [ ] Rinse the **pressure (depth) transducer** thoroughly
- [ ] Rinse the **CTD and science sensors** per their own guidance
- [ ] Dry the recovery strobe / dome and rinse with fresh water *(if fitted)*

---

## 4. Thruster Service *(if fitted)*

- [ ] Remove the thruster hub &emsp;<small>*7/64" hex wrench*</small>
- [ ] Rinse the thruster thoroughly with fresh water
- [ ] Apply **molybdenum disulfide grease** &emsp;<small>*supplied with the thruster kit*</small>
- [ ] Replace the hub

---

## 5. External Inspection

- [ ] Inspect the **hull** for damage &emsp;<small>*carbon-fiber hulls: check O-ring sealing surfaces for scratches/defects that could lead to a leak*</small>
- [ ] Inspect **anodizing and paint** for scratches &emsp;<small>*exposed aluminium corrodes — touch up with automotive paint (nail polish works in an emergency)*</small>
- [ ] Inspect **wet-mate connectors** (Teledyne Impulse) for damage and clean pins
- [ ] Inspect the **external air bladder** for damage &emsp;<small>*inspect before and after every deployment*</small>
- [ ] Inspect the **recovery system / lanyard** *(if fitted)*
- [ ] Care for **dummy and green plugs** &emsp;<small>*OLube or silicone spray; keep contact pins clean*</small>

---

## 6. Sacrificial Anodes

The forward and aft end caps carry sacrificial zinc anodes that protect exposed
aluminium and stainless steel from corrosion.

- [ ] Inspect anodes for wear; replace if significantly consumed &emsp;<small>*contact glidersupport@teledyne.com for sizing*</small>
- [ ] **Forward anode continuity** — probe between the forward anode and the top pump flange screw (ohmmeter); confirm **< 10 Ω**
- [ ] **Aft anode continuity** — probe between the aft anode and the ejection weight tube (ohmmeter); confirm **< 10 Ω**

---

## 7. O-Rings & Seals *(if opening the glider)*

!!! tip "O-ring care"
    Inspect O-rings for cleanliness, nicks, and slices, and the sealing surfaces
    for scratches, dents, and dirt. Lubricate with **Parker Fibrous O-Lube
    884-4**. Wear eye protection and chemical-resistant gloves. Replace any O-ring
    that is damaged.

- [ ] Inspect main-hull double O-rings and sealing surfaces
- [ ] Re-lubricate or replace O-rings as needed &emsp;<small>*G3 main-hull O-ring P/N 304697 — **not** interchangeable with G2*</small>

---

## 8. Desiccant

- [ ] Replace desiccant packs &emsp;<small>*use fresh desiccant for each deployment*</small>
- [ ] If the glider will stay open, store desiccant in **sealed plastic bags** &emsp;<small>*saturated desiccant gains ~40 g and affects ballasting; dry pouch ≈ 114 g*</small>
- [ ] Open and re-seal the glider in a controlled, dry environment where possible

---

## 9. Vacuum & Leak Check

- [ ] Pull and confirm internal **vacuum** &emsp;<small>*low/falling vacuum indicates a leak; positive pressure may indicate gas accumulation — vacuum varies with temperature*</small>
- [ ] Check fin leak-detect reading &emsp;<small>`m_digifin_leakdetect_reading` should sit near 1025; below 1018 indicates a leak</small>

---

## 10. Storage Preparation

- [ ] Recharge / service batteries as planned
- [ ] Confirm desiccant installed and glider sealed
- [ ] Store within the recommended temperature range &emsp;<small>*+10 to +25 °C for optimum battery life*</small>
- [ ] Secure the glider for storage or shipping &emsp;<small>*if crating, use all straps; secure cylindrical parts so they cannot roll*</small>

---

## Sign-Off

| Section | Completed by | Time (UTC) | Notes |
|---|---|---|---|
| Rinse complete | | | |
| External inspection | | | |
| Anode continuity OK | | | |
| Desiccant replaced | | | |
| Ready for storage | | | |
