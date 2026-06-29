---
title: Thruster
description: The optional 10-Watt Slocum thruster: what it is, the three ways it's used (thruster-assisted yos, drift_at_depth horizontal flight, surface lens penetration), the four control modes, surface burst, energy penalty, installation and in-air checkout, post-deployment care, and field troubleshooting.
---

# Thruster

The **thruster** is an optional propulsion module that bolts onto the tail of a
G2/G3 Slocum, giving the buoyancy-driven glider an actively-powered push. It is a
**high-efficiency ~10-watt** unit whose larger blades **sweep back to reduce drag
when not running**, so a glider that carries one but isn't using it pays only a
small flight penalty.

It buys you **speed and capability** — fighting strong currents, holding
horizontal flight while drifting at depth, and "punching" through low-density
surface layers — but it is **never free**: running it costs far more energy than
gliding. Energy budgets must be watched carefully whenever the thruster is in
use.

!!! info "Source"
    Paraphrased from the *Slocum Glider Operators Manual* (Rev. 1, "Optional
    10-Watt Thruster"), the TWR `doco/how-it-works/thruster.txt` design note,
    `masterdata.txt`, the Teledyne Webb Research user forum, and the UG2
    community Slack. This is a condensed field reference — always defer to the
    current `thruster.txt` and official Teledyne documentation for your specific
    glider and firmware. Default values quoted here are masterdata defaults and
    can differ on your glider.

---

## The energy trade-off

The thruster is a tool for getting somewhere faster or holding a position, not a
default flight mode. The community consensus:

- A glider that normally burns **~3–5 coulomb A·h/day** can jump to **~10–15
  A·h/day** with the thruster working — be ready for the "energy shock."
- In return you can roughly **halve transit time** to a science location, so the
  penalty can be worth it as **energy per distance** even though it's worse as
  **energy per day**.
- **Thruster-assisted yos** are generally the better transit use; the pure
  horizontal **bathtub/drift mode** is rarely the winner for transit (it has
  niche shallow-water or science uses).
- For fighting current, a thruster is often the deciding factor — but combine it
  with good current strategy (fly across the current, inflect below the fast
  surface layer; see [Power Saving](../../../piloting/slocum/power-saving.md) and
  the piloting notes).

!!! tip "Three blessed mission templates"
    Slocum thrusters have settled into three established uses, each with a sample
    mission:

    1. **Thruster-assisted yos** — speed during normal sawtooth flight.
    2. **Lens penetration** — `astock.mi` / `surfac2X` surface behaviors.
    3. **Horizontal flight at depth** — `bathtub.mi` with `drift_10.ma`.

    The recommended packaged mission is **`thrstock.mi`** (electric-1000 target).

---

## How it's commanded

In the `yo`, `drift_at_depth`, and `surface` behaviors you select a **mode**
(`use_thruster`) and a **value** (`thruster_value`). The same four modes apply in
the dive/climb (`d_`) and climb-to-surface (`c_`) halves of a yo:

| `use_thruster` | Mode | `thruster_value` means | Notes |
|:--:|---|---|---|
| **0** | Not in use | — | Default. |
| **1** | % of glider voltage | 0–100 % of `m_battery_inst` | Ramped up (not stepped) to avoid a power spike. |
| **2** | % of max thruster voltage | 0–100 % of `f_thruster_max_v` | e.g. 40 % of 9 V ≈ 3.6 V to the thruster. |
| **3** | Depth-rate feedback | m/s depth rate (**< 0 for climb/surface**, > 0 for dive) | Dive/climb/surface only — not `drift_at_depth`. Used for lens penetration. |
| **4** | Power feedback | watts (between `f_thruster_power_min`/`max`) | **Recommended mode.** Mission aborts at init if value is out of range. |

- **Recommended default:** mode **4** (power control) for most uses; mode **3**
  (depth-rate) for lens penetration and surface assist.
- The command is **clipped** so the estimated input voltage stays between
  `f_thruster_min_v` (default **3.0 V**) and `f_thruster_max_v` (default
  **9.7 V**).
- After a behavior activates the thruster, the controller waits
  `u_thruster_inflection_holdoff` seconds before turning it on (defaults ~**60 s
  shallow / 120 s deep**), and it stays **off while inflecting** or if measured
  **pitch is in the wrong direction** for the commanded vertical motion.
- `x_thruster_state` records **why** the thruster is or isn't running (mode not
  enabled, holding for holdoff, wrong pitch direction, burst mode, adjusting up/
  down to hit a depth rate, etc.) — the first thing to read when it's not
  behaving.

!!! note "Two device drivers"
    The motor controller is declared as one of two devices:

    - **`thruster`** — has electrical **current feedback**; **G2 only**. Enables
      current-based speed estimation, power/energy monitoring
      (`m_thruster_power`, `m_avg_thruster_power`, `m_thruster_amphr/watthr`),
      and current-based error reporting.
    - **`thruster_g1`** — **no current feedback**; works on any glider. Speed is
      estimated from input **voltage** instead.

---

## Surface burst (anti-fouling)

By default, whenever the thruster is installed the glider gives it a **short
burst right before diving** after each surfacing, to clear buildup off the prop:

- Controlled by `thruster_burst(bool) 1` in the `surface` behavior (on by
  default; can be disabled).
- `u_thruster_burst_volts` (default ~6 V) and `u_thruster_burst_secs` (default
  ~15 s) set the burst.
- This is reported as `x_thruster_state = 9` (burst mode).

---

## Lens penetration

The thruster can **punch the glider through a low-density surface lens** that
buoyancy alone can't beat. It runs in **depth-rate mode (3)** in the `surface`
and/or `yo` behaviors, commanded to hold a minimum (negative) depth rate so that
if a lens stalls the climb, the thruster kicks in.

Because the pressure transducer can drift, a special surface-completion mode
(`c_stop_when_air_pump`) keeps the thruster on until the glider is **confidently
at the surface** — typically detected by reaching surface depth **and** seeing a
large vacuum change plus a nose-down pitch (both signs the air bladder has
inflated). `x_why_lens_completed` records which condition ended it. A side effect:
the thruster may run a few extra seconds at the surface while the bladder
inflates.

Useful monitoring sensors (worth adding to `config.srf`): `c_thruster_surface_secs`,
`c_thruster_depth_rate_secs`, `c_thruster_surface_depth`, `c_thruster_depth_rate_depth`.

---

## Drift-at-depth / horizontal flight

For horizontal flight while hovering, choose a depth-control method with the
`depth_ctrl` b_arg:

| `depth_ctrl` | Method | Use |
|:--:|---|---|
| **0** | Buoyancy (bpump) increments depth | Default; fine at near-zero speed, sluggish with thruster. |
| **1** | Servo bpump (PD on depth) | **Untested** per the design note. |
| **2** | **Pitch-based** (PID outputs pitch, thruster provides drive) | **Recommended for thruster** horizontal flight. |

- **Method 2** uses the pitch servo (and thus the thruster) to hold depth, only
  falling back to buoyancy when pitch saturates or the glider stops moving
  vertically. It is **not** appropriate for non-thruster missions — without
  forward speed there's no lift to change depth.
- **Steering is off by default** in `drift_at_depth`; enable it with
  `enable_steering(bool) 1`.
- When the thruster is on, the heading and pitch autopilots **swap to
  thruster-specific gains** (`u_thruster_hd_fin_ap_*` for steering) so the
  controller is tuned for powered flight.

---

## Installation & in-air checkout

??? note "Installation outline (from forum t=216)"
    **`autoexec.mi` edits:**

    1. Confirm the thruster is **uncommented** in the installed-devices list.
    2. Add the glider-specific current cal to the cal section, e.g.
       `sensor: c_thruster_current_cal(nodim) 0.0384` (A/count — value is
       per-glider).

    **Hardware:**

    1. Line up the tail-tube holes with the threaded holes on the thruster.
    2. Secure it with the hardware from the **dummy thruster** it replaces.
    3. Connect to the 6-pin connector on the aft endcap (use **3M silicone
       spray**).
    4. Open the glider between the aft hull and science bay; find the 4-pin
       connector on the back of **J70** and mate it to its counterpart beneath
       the forward-port corner of the aft electronics tray (keep it tie-wrapped
       to the mainboard corner guard).
    5. Use the **new-style green plug** — the old style is retired.

**In-air checkout** (Operators Manual / forum):

1. **Make sure the propeller blades are clear of the cart** — and remember the
   **blades are sharp**.
2. `report ++ m_thruster_current m_thruster_power`
3. `put c_thruster_on 30` — **only for under a minute.**
4. Confirm the blades spin **clockwise viewed from the aft (tail) end** and that
   `m_thruster_current` updates regularly.
5. `put c_thruster_on 0`, then `report clearall`.

!!! danger "Never run the thruster dry for long"
    Running the thruster out of water for more than a momentary pre-deployment
    check can **break the prop blades and overheat the motor**. Coupling
    noise/chatter while out of water is **normal**. The thruster spins **clockwise
    viewed from the rear** — always.

---

## Post-deployment care

!!! warning "Do not let a salt-water-submerged thruster dry out"
    After a deployment, service the thruster promptly:

    1. Remove the **thruster hub** with a **7/64 hex** wrench.
    2. Rinse thoroughly with **fresh water**.
    3. Apply **molybdenum disulphide grease** (supplied in the thruster kit).
    4. Replace the hub.

---

## Energy & error monitoring

Add these to your logs for long-term monitoring:

- **`longterm.dat`:** `m_thruster_power_spike`, `m_thruster_amphr`,
  `m_thruster_watthr`.
- **`sbdlist.dat`:** `m_thruster_power 180`, `c_thruster_on 180` (adjust rate).
- **`config.srf`:** `m_thruster_power_spike` (plus the lens-penetration sensors
  above).

**Error reporting / aborts:** for the `thruster` (current-sensing) device, a
running average of `m_thruster_current` is checked while commanded on — if the
average exceeds `u_max_thruster_current`, **or reads exactly 0**, a **device
error is raised and the mission aborts**. `m_thruster_power_spike` tallies
excursions above `f_thruster_power_max`. The abend behavior can also use the
thruster during an abort ascent (`use_thruster_for_ascent`) to hold a minimum
ascent rate.

---

## Side effects to plan for

- **Oxygen optode noise.** Running the thruster corrupts readings from a
  **tail-mounted DO optode** (the tail isn't a good flow location even normally,
  and the thruster makes it worse). If a deployment needs both heavy thruster use
  and DO data, **mount the optode in the flow** (tail tube or front), not in the
  thruster's wake.
- **Self-noise.** Like the buoyancy pump and altimeter, a running thruster is a
  loud acoustic source — relevant for [passive acoustic
  monitoring](../../../piloting/slocum/passive-acoustic-monitoring.md) missions.

---

## Troubleshooting

| Symptom | Likely cause / what to check |
|---|---|
| **Choppy / non-smooth spin** at higher power (e.g. fine at 10–25 %, rough at 30 %+), little propulsion | Reported on a bench/ballast-tank G3 even after re-greasing — a mechanical/controller fault worth raising with Teledyne; the prop should spin smoothly and pull forward at low power. |
| Mission **aborts at initialization** with a thruster behavior | In **power mode (4)**, `thruster_value` is outside `f_thruster_power_min`…`max`. Bring it into range. |
| **Device error / abort** while running | Average current over `u_max_thruster_current`, or current reading **0** (bad cal/wiring/stalled prop). Check `c_thruster_current_cal`, connectors, and that the prop is free. |
| Thruster **never turns on** when expected | Read `x_thruster_state`: still within `u_thruster_inflection_holdoff`, pitch in the wrong direction, or mode not enabled. |
| **Energy draining fast** | Expected — thruster can ~3× daily consumption. Reconsider mode/value; prefer assisted yos over bathtub for transit. |
| Blades won't spin freely / noisy after recovery | Service per post-deployment care (7/64 hub, rinse, MoS₂ grease). Coupling chatter **in air** is normal. |

---

## Quick reference

| Command / sensor | Meaning |
|---|---|
| `put c_thruster_on 30` | In-air checkout: % command for a brief spin (then `0`). |
| `report ++ m_thruster_current m_thruster_power` | Watch thruster current/power during checkout. |
| `use_thruster` (b_arg) | Mode 0/1/2/3/4 — off / %V / %maxV / depth-rate / power. |
| `thruster_value` (b_arg) | Value whose meaning depends on the mode. |
| `x_thruster_state` | Why the thruster is / isn't commanded on. |
| `f_thruster_min_v` / `f_thruster_max_v` | Voltage clip limits (≈3.0 V / 9.7 V). |
| `f_thruster_power_min` / `f_thruster_power_max` | Power-mode bounds (≈1 W / 10 W). |
| `m_thruster_amphr` / `m_thruster_watthr` | Integrated energy used by the thruster. |
| `thruster_burst` (b_arg) | Pre-dive anti-fouling burst (on by default). |

---

## See also

- [Power Saving](../../../piloting/slocum/power-saving.md) — the energy budget the
  thruster competes with, and current-fighting strategy.
- [Pumps](../pumps/index.md) — the buoyancy engine the thruster assists; pump
  choice (shallow vs. deep) shapes how you fight current.
- [Fin / Digifin](../digifin/index.md) — steering, which switches to
  thruster-specific autopilot gains when the thruster is on.
- [Passive Acoustic Monitoring](../../../piloting/slocum/passive-acoustic-monitoring.md)
  — the thruster as a self-noise source.
