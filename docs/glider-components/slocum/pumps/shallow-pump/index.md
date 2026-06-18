---
title: Shallow Pump
description: Slocum shallow (piston) buoyancy pump — design, depth/gearbox variants, the rolling-diaphragm (Bellofram) seal, vacuum requirement, top-inflection limits, maintenance, testing, and field troubleshooting.
---

# Shallow Pump

The shallow buoyancy pump is a **single-stroke piston** design that moves
**seawater directly** into and out of a short port on the nose centerline (the
stagnation point) to change the vehicle's displacement. It uses a **90-watt
motor** and a **rolling-diaphragm (Bellofram) seal**. On G3 gliders the pump is
high-displacement (≥ ~960 cc).

!!! info "Source"
    Paraphrased and consolidated from the *Slocum G3 Glider Operators Manual*, the
    TWR user forum, and the UG2 community Slack. Pumps are **factory configured** —
    contact `glidersupport@teledyne.com` before changing pump settings. See also
    the [Deep Pump](../deep-pump/index.md).

---

## Depth / gearbox variants

The shallow pump ships with different **gearbox/motor** combinations rated for
different pressures (commonly **30 / 50 / 100 / 150 / 200 m**). The mechanical
gear drive is not the limiting factor — the limit is the energy that must be
pulled from the battery on the return stroke. Pick the gearbox/motor for your
working depth to get **quick inflections** (more important in shallow water) and
to minimise return-stroke energy.

!!! tip "100 m vs 200 m — which to buy"
    Both are piston pumps. Choose the **200 m** pump if the water is deeper than
    100 m and you want to sample below 100 m. The only advantage of the **100 m**
    pump is slightly more efficient flight (slightly longer missions); choose it
    only if limiting profiles to 100 m is acceptable *and* maximum endurance is
    the priority.

---

## Vacuum requirement & back-drive brake

!!! danger "Never run the shallow pump without vacuum or external pressure"
    The rolling diaphragm must have either external water pressure **or** internal
    vacuum on it, or it can be damaged. Draw the internal vacuum to about
    **6 inHg below external atmosphere** so the diaphragm folds smoothly as it
    rolls. A **latching brake** holds the motor at rest to eliminate back-drive of
    the pump under pressure.

---

## Top-inflection depth limits

Unlike the deep pump (which can retract at any depth), a shallow pump can only
retract within its rated range — push it deeper and you risk an abort, and
back-driving the pump at depth can over-volt the electronics (protection exists,
but respect the limits). Operator rules of thumb for the **deepest** sustained
top inflection:

| Pump | Practical top-inflection depth |
|---|---|
| 30 m | < ~10 m |
| 100 m | ~20 m (e.g. to clear shipping lanes) |
| 200 m | ~50 m |

---

## Reducing drive for slow / efficient flight

The full drive is `±1000` cc, but the glider flies well on as little as
**~300 cc** of total drive. Reducing drive ("flying slow") is useful in shallow
water or to save energy:

- Set `b_arg: d_bpump_value(x)` in your yo file (this bounds `m_ballast_pumped`).
- Or set it live, e.g. `put c_dive_bpump -200` / `put c_climb_bpump 200` with
  `put c_autoballast_state 0`, returning to `±1000` when full drive is needed.
- The **autoballast** software feature can set reduced drive automatically.

---

## Maintenance — the Bellofram

The rolling diaphragm (Bellofram) is the part to watch: **cracks or creases on a
Bellofram are a death sentence for a shallow pump.**

- While installed and **retracted**, rinse debris and grit out with a standard
  garden hose first.
- Then hand-clean with **tap water and mild (dish) soap** and a soft cloth. Do
  **not** use solvent-based cleaners.
- Apply a thin layer of **Molykote 316 or 3M Silicone Lubricant** (not a silicone
  spray containing acetone) to prevent stiction and stop debris sticking.
- Inspect: a healthy Bellofram is **smooth and uniform under vacuum** and slightly
  "wavy" with no vacuum. **Creases** can be felt with a finger and won't flatten
  against the cylinder wall; **abrasion** feels rough and looks like non-uniform
  cloth.

!!! note "Service life"
    Shallow (rolling-diaphragm / bellophragm) pumps have a **10,000-cycle** service
    life, or **20,000 `m_tot_num_inflections`** when profiling to full depth. When
    not profiling to full depth, ask Glider Support about
    `m_pump_effective_num_cycles`.

---

## How to test

From `lab_mode`:

1. `wiggle on`
2. `report ++ m_ballast_pumped`
3. Confirm the pump completes a full extension (`m_ballast_pumped = +400 cc`) and
   full retraction (`-400 cc`) without errors.
4. `wiggle off`

To confirm the pump is even active: on every power-up the pump extends buoyancy
to full displacement, and `report ++ m_ballast_pumped` shows the position moving.

With a properly ballasted glider, **positive cc → positive buoyancy → climb**;
**negative cc → dive**.

| Sensor | Description |
|---|---|
| `m_ballast_pumped` | Measured volume pumped (cc) |
| `c_ballast_pumped` | Commanded volume pumped (cc) |

---

## Field troubleshooting

- **`MS_ABORT_DEVICE_ERROR` / "buoyancy_pump device driver returned an error."**
  Find the mission segment of the abort and inspect the `.mlg` plus the `.sbd`/
  `.dbd` to see what the pump was doing. If it tripped at full throw or out of
  deadband, you can try explicitly setting limits (`put c_dive_bpump -200`,
  `put c_climb_bpump 200`, `put c_autoballast_state 0`) before putting the pump
  back in service.
- **Stuck piston / potentiometer failure.** A failed position potentiometer (the
  board that reads pump volume) can throw `DRIVER_ODDITY: ... Buoyancy Pump is
  FAULTED!` and a `MOVE ERROR Error reading position`, and the pump keeps taking
  itself back out of service even after `use +`. This usually needs a TWR rebuild,
  but as a field stopgap operators have set `f_ballast_pumped_safety_max` to the
  value the pump is **stuck** at, which can let you re-enable the pump (held at
  position) to run a thruster/bathtub mission toward recovery.
- A sudden pump fault accompanied by a slowly dropping **leak-detect** voltage can
  indicate water intrusion shorting the pump electronics — recover and inspect.
