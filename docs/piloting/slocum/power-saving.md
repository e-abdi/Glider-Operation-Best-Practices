---
title: Power Saving
description: How to run a Slocum mission on the lowest possible power and keep the glider alive as long as possible while waiting for recovery — both diving and drifting, on the surface and below it. Covers low-power mode, mission trimming, drift-at-depth, surface drift in GliderDOS, and lastgasp caveats.
---

# Power Saving

This page collects the practical levers a Slocum pilot can pull to **minimize
energy use** — both to stretch a normal mission and to keep a glider alive as
long as safely possible while it waits for recovery (after a weight drop, a leak
abort, a schedule slip, or just a long pickup window). It covers saving power
**while diving** and **while drifting**, and **on the surface** as well as
**below it**.

!!! info "Source"
    Paraphrased from the *Slocum G3 Glider Operators Manual* (Rev. 1, "Emergency
    Recovery" and "G3 Missions"), the UG2 community Slack, and the Teledyne Webb Research user forum. Several of the steps below mirror
    the TWR forum's "extreme energy conservation while waiting for recovery" and
    "standard steps for going into low power usage and drifting" posts. This is a
    condensed field reference — **always simulate a low-power mission in the lab
    before flying it**, and defer to official Teledyne documentation for your
    specific glider.

---

## Where the energy goes

Roughly, a Slocum spends energy on four things:

1. **Buoyancy pump** — by far the biggest mover; every inflection costs pump
   work, and more drive (cc) and faster dives cost more.
2. **Pitch (battpos) motor** — repositioning the battery to set pitch.
3. **Science** — the science computer and sensors (CTD, optode, fluorometer,
   altimeter, etc.).
4. **Comms and "housekeeping"** — Iridium/Freewave, GPS, the flight computer's
   wake cycle, and time spent awake at the surface.

!!! tip "Measure, don't guess"
    Watch the effect of every change with `m_coulomb_amphr_total` (cumulative),
    `m_coulomb_current` (instantaneous), and `m_battery` (pack voltage). A common
    field metric is **amp-hours per day**, computed from the change in
    `m_coulomb_amphr_total` over time (e.g. between surface dialogs). Typical
    reported figures: a G2/G3 **diving efficiently** with reduced science gets
    down to **~1.4–1.9 A·h/day**; a glider **drifting on the surface** often uses
    **~2.5 A·h/day** until the console and GPS are dealt with.

!!! warning "G3 / G3S use more power than G2"
    Operators and an OOI-requested TWR investigation found newer **G3/G3S**
    gliders (and the **STM32** processor) draw noticeably more quiescent power
    than G2s — in one case ~50% more at idle. Several fixes landed in firmware
    (power fixes between **10.07→10.08** and again at **11.0**). If power use
    looks high, check your firmware version first.

---

## Saving power while diving (mission design)

These are the levers you set in the `.mi`/`.ma` files for a normal endurance
mission. Stacking several of them is what gets a glider to the low
A·h/day numbers above.

### Trim science

- **Turn science off** entirely (`put c_science_on 0`,
  `put c_science_all_on_enabled 0`) for the biggest base-load cut, or
- **Subsample**: sample only every *X* downcasts, or sample on the **downcast
  only**. Reducing what's in `sbdlist.dat` also drops the data volume you
  transfer at the surface.

### Use Low Power Mode

Low power mode reduces the wake/cycle time of the flight (and science) computers
so the glider effectively sleeps between the things that actually need
attention. Enable it from the start of a mission for the most benefit, though it
still helps near the end of a battery.

```text
sensor: u_low_power_cycle_time(sec) 30   # > 0 enables LP; 30 is the recommended max
sensor: u_science_low_power(sec)   30    # science computer powers down between samples
sensor: u_alt_reduced_usage_mode(bool) 1 # let the altimeter sleep when not needed
sensor: u_alt_min_depth(m) <as deep as comfortable>
```

- `u_low_power_cycle_time` only needs to be set **once**; it is not reset during
  the mission. Recommended **max value is 30**.
- **The altimeter blocks low power.** While the altimeter must be on, the glider
  will not enter low power. In deep, stable water, either **turn the altimeter
  off** or push `u_alt_min_depth` as deep as you safely can so the altimeter is
  needed for less of each dive. (Set it very deep during simulations.)
- **Monitor whether it's actually working** with `x_low_power_status` (it tells
  you *why* low power is disabled — altimeter on, GPS on, motors moving,
  surfacing, inflecting, etc.) and `x_cycle_time`. For science low power, watch
  `m_science_on`.

### Fly the buoyancy and pitch motors gently

- **Use autoballast.** TWR highly recommends autoballast on G3 specifically for
  energy conservation (and to avoid unnecessary speed). With 8.0+, default flight
  drive is **±260 cc**; using the full HD drive (toward ±1000 cc) "significantly
  increases energy consumed" — and legacy ±1000 cc missions can cause fast,
  steep, uncontrolled dives in shallow water.
- **Dive deep and slow.** Fewer inflections per unit of data; minimize the
  buoyancy drive used per yo.
- **Shallow pitch angle.** Operators fly endurance missions as low as **~18°**
  (vs. a typical ~26°) because the smaller angle reduces pitch-motor work — as
  long as you're not getting pushed around more than you like.
- **Fixed battpos / fixed bpump.** If you know settings that work, turn **servo
  mode off** on the pitch motor and use a fixed battery position (and a fixed
  buoyancy value) so the motors aren't constantly hunting.

### Minimize surface time and comms

- **Lengthen the surfacing interval** — surface for fewer reasons. You can
  comment out "surface for waypoint" and surface only periodically for a GPS fix
  and data transfer (see *Drifting below the surface*).
- **Spend as little time on the surface as possible** transferring files
  (smaller `sbdlist`, fewer files).

---

## Drifting below the surface (waiting submerged)

If you can afford to be underwater, **drifting at depth** ("bathtub" mission)
is usually the lowest-power way to hold station and avoid being swept around on
the surface.

- Set a target drift depth and a **wide deadband** so the buoyancy engine stays
  off most of the time. If the depth/angle deadband is tight and the glider has
  to correct constantly, drift-at-depth can actually use **a lot** of energy; if
  the deadbands are open, usage is reasonable. Example field starting point:
  `target_depth = 100`, `target_deadband = 150` (the band spans the surface so
  the glider rarely needs to pump).
- **Hours** of drift per segment is fine; the practical limit is more
  environmental/operational than a hard number. The glider can also drift
  **nose-up** (e.g. ~20° for upward-facing radiometers).
- Combine with **low power mode** and **science off/subsampled** for the lowest
  draw.
- For holding a position (virtual mooring), pick a number of dives between GPS
  surfacings, set `num_half_cycles_to_do` accordingly, and surface for **time**
  every few hours just to transfer and re-fix.

!!! note "Diving can beat surface drifting"
    Several operators found that a glider **diving efficiently in low power**
    (e.g. ~1.4 A·h/day) used *less* power than the same glider sitting on the
    surface in "extreme conservation," and diving also keeps it from being swept
    away by currents. If the glider can still dive, gently cycling deep may be
    both safer for position and easier on the battery than surface drift.

---

## Drifting on the surface (waiting for recovery in GliderDOS)

When the glider can't dive (weight blown, leak) or you want it parked at the
surface, the goal is to stay in **GliderDOS**, call in on a schedule, and shut
off everything you don't need. This is the "standard low-power drift" recipe.

**Stretch the timers and call in less often** (values are examples — set to suit
your battery and pickup window; 1–6 h callbacks are typical):

```text
put u_iridium_max_time_til_callback 3600   # up to 1800 s is the documented max for c_iridium_time_til_callback
put u_max_time_in_gliderdos 3600           # how often it cycles into a mission to try to call in
put c_science_on 0
put c_science_all_on_enabled 0
put c_console_on 0                          # turns off Freewave console
```

Then **take non-essential devices out of service** (`use - <device>`), as
appropriate for your vehicle — e.g.:

> GPS · pinger · attitude / attitude_tcm3 / attitude_rev · ocean_pressure ·
> pitch_motor · science_super · fin_motor · digifin · altimeter · thruster

…and **run a callback script** at your chosen interval.

!!! tip "The two biggest single wins on the surface"
    1. **Turn the Freewave console off.** `put c_console_on 0` has been measured
       to save **~1 A·h/day** on a surfaced glider (e.g. ~2.5 → ~1.5 A·h/day).
       See the [Freewave page](../../glider-components/slocum/freewave/index.md#power-the-console-and-low-power-drift).
    2. **Cycle the GPS instead of leaving it on.** Use a callback script that:
       turns GPS on (`c_gps_on 1`), does a short callback for a fresh fix, then
       turns GPS off (`c_gps_on -1`) before the long callback. (The net win
       depends on call overhead — measure it; some find it nearly a wash.)

!!! danger "Turn comms back on before you send a boat"
    If you `use - console` or `put c_console_on 0`, **remember to re-enable it**
    before a recovery crew goes out expecting to home in on the Freewave or GPS.
    The Freewave is your in-range backup.

---

## Staying out of a mission: lastgasp and reverting settings

Keeping a stuck glider in GliderDOS is fragile — the firmware fights you:

- **Settings silently revert.** Operators report that within a day,
  `u_max_time_in_gliderdos` reverts to 900, and `c_science_on` /
  `c_science_all_on_enabled` flip back to 1, after which a long callback lets the
  glider sequence into `initial.mi` / `lastgasp.mi` and possibly dive or abort.
- A reported workaround to **keep it from sequencing** is
  `put u_max_time_in_gliderdos -1` (stay in GliderDOS indefinitely). Re-check
  your settings every call.
- **`lastgasp.mi`** is the minimal survival mission the glider falls into; like
  `initial.mi` it does **not** use the 8.0 default buoyancy drive changes. Note
  that you **cannot take a *critical* device (e.g. Freewave/console) out of
  service from GliderDOS** with the glider on the pier — it's a critical device,
  not even required in `autoexec.mi`.
- A simple robust approach used in the field: just **increase the GliderDOS and
  callback timeouts and run an Iridium callback script** on a fixed cycle (e.g.
  ~11 min when close to pickup, longer when not) so the glider keeps reporting
  position without diving.

!!! note "Emergency-recovery levers (from the manual)"
    For an emergency, TWR's documented moves include raising
    `u_iridium_max_time_til_callback` (≤ 1800 s), raising
    `u_max_time_in_gliderdos` (e.g. 900 → 3600) **only if the weight is blown or
    you're sure it's safe**, switching to a `callback 30` script on Dockserver,
    running energy-conservation scripts, and turning on **Argos ALP** (all
    location processing) for an independent position source. Contact
    `glidersupport@teledyne.com` for case-specific guidance.

---

## Know when to stop: battery shelves

Power saving buys time, but the **battery voltage shelf** sets the real deadline.

- With the older **3S lithium** design, TWR recommends you **stop diving and
  drift once energy reaches the first shelf**.
- With the **4S** design you can keep operating on the first shelf, but the
  appearance of the **second shelf drop may be the last time the glider
  communicates** — do not deplete either chemistry to the second shelf
  operationally.
- Derate stored capacity (~3%/year is TWR's rule of thumb; field experience
  suggests partly-used packs can lose more). See the
  [primary battery page](../../glider-components/slocum/batteries/primary/index.md)
  for capacity, derating, and the voltage-shelf details.

---

## Quick reference

| Lever | Command / sensor | Effect |
|---|---|---|
| Low power mode | `u_low_power_cycle_time` > 0 (max 30) | Flight computer sleeps between needs |
| Science low power | `u_science_low_power` | Science computer powers down between samples |
| Altimeter not blocking LP | `u_alt_reduced_usage_mode 1`, `u_alt_min_depth` deep / altimeter off | Lets low power activate more of the dive |
| Is low power active? | `x_low_power_status`, `x_cycle_time`, `m_science_on` | Diagnoses why LP is/ isn't on |
| Science off | `c_science_on 0`, `c_science_all_on_enabled 0` | Cuts base load |
| Freewave console off | `c_console_on 0` | ~1 A·h/day on the surface |
| GPS cycling | `c_gps_on 1` / `c_gps_on -1` in a callback script | Avoids leaving GPS on continuously |
| Stretch callback | `u_iridium_max_time_til_callback` | Fewer Iridium calls |
| Stay in GliderDOS | `u_max_time_in_gliderdos` (or `-1`) | Avoid sequencing into a mission |
| Gentle buoyancy | autoballast, smaller `bpump` drive (±260 vs ±1000) | Less pump work |
| Gentle pitch | shallow pitch (~18°), fixed battpos, servo off | Less pitch-motor work |
| Drift at depth | `target_depth`, wide `target_deadband` | Buoyancy engine mostly off |
| Out of service | `use - <device>` | Removes a device's draw |
| Monitor energy | `m_coulomb_amphr_total`, `m_coulomb_current`, `m_battery` | Track A·h/day |

!!! warning "Simulate first, and watch for reverts"
    Low-power and drift settings interact in non-obvious ways (the altimeter,
    surface behaviors, and firmware all override sensors). **Simulate the
    mission in the lab before flying**, and on a stuck glider **re-verify your
    settings every call** — several of them revert on their own.
