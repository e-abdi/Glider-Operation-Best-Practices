---
title: Autoballast
description: How the Slocum autoballast feature automatically tunes buoyancy drive — what it does (centering the dive/climb drive for a 1:1 speed ratio and the lowest drive that flies), the sensors and states involved, how to set it up in yo/drift and surface behaviors, how to monitor and reset it in the field, and the shallow-water and simulation gotchas.
---

# Autoballast

**Autoballast** is the Slocum software feature that automatically tunes how much
buoyancy drive the glider uses, so a pilot only has to specify the *total* drive
they want and let the glider find the rest. It does two things:

1. **Reduces the drive** used on dives and climbs to the smallest amount that
   still flies the glider acceptably — saving energy and reducing speed.
2. **Centers** that drive so the dive and climb are balanced (a dive/climb speed
   ratio near **1:1**) and the pump does **not** have to fully extend at the
   surface every cycle.

It is especially valuable on **G3** gliders, whose high-displacement pumps move a
lot more volume — running them at full `±1000 cc` drive "significantly increases
energy consumed" and can cause fast, steep, uncontrolled dives in shallow water.
See [Power Saving](power-saving.md), which recommends autoballast as a core
energy-conservation lever.

!!! info "Source"
    Paraphrased from the `masterdata` autoballast/speed-control sensor block and
    the *Slocum G3 Glider Operators Manual* (the public
    `doco/how-it-works/autoballast.txt`), with field practice from the Teledyne
    Webb Research user forum and the UG2 community Slack. The concept — the glider
    "adjusts the center point of the drive to provide a dive/climb ratio of one"
    given a user-defined total volume — is described in TWR's UUST 2013 Slocum
    paper. Defaults and sensor names vary by firmware; **confirm against your
    `masterdata` and simulate before flying.**

---

## What it does

Without autoballast you command a fixed buoyancy: full drive is `±1000 cc`, but a
glider flies fine on far less (often **~300 cc total**, sometimes less). Picking
that reduced drive by hand — and re-centering it as ballast, water density, and
payload change — is fiddly. Autoballast does it continuously:

- You give it **one number**: the **total** drive volume you want (the spread
  between the dive and climb buoyancy). There is **no separate "climb" value** —
  the single total is split around a center point the glider chooses.
- The glider **starts at full drive** (`c_dive_bpump −1000`, `c_climb_bpump
  +1000`) and **steps the drive down on each yo** as it converges.
- If vertical speed falls **below your minimum**, it **adds drive back** until the
  glider is fast enough again.
- The converged, reduced drive is **maintained at the surface** too, so the pump
  isn't fully extended every surfacing (more surface stability, less energy).

!!! example "What \"total drive\" means"
    If you ask for a total of **300 cc** and the glider is perfectly ballasted, it
    will settle on roughly **−150 cc on dives and +150 cc on climbs**. The total
    is recorded as `c_autoballast_volume` in the data files; the live split is
    `c_dive_bpump` / `c_climb_bpump`.

---

## Key sensors

| Sensor | Role |
|--------|------|
| `c_dive_bpump` | Live ballast (cc) used on the **dive** (negative). Watch in the surface dialog |
| `c_climb_bpump` | Live ballast (cc) used on the **climb** (positive) |
| `c_autoballast_volume` | The total drive you requested (read from the yo `b_arg` `d_bpump_value`) |
| `c_autoballast_state` | Current state of the autoballast routine (see below); writable to **force** a state |
| `f_min_ballast` | Floor on total drive (default **250 cc**) — a total below this aborts the mission |
| `f_min_pump` | Minimum delta ballast used for a climb or dive (default 10 cc) |
| `u_autoballast_abort` | If autoballast fails to converge: `1` = abort, `0` = go to state 3 and keep flying on the last amounts |
| `u_autoballast_end_on_converge` | `1` = stop adjusting once converged; `0` = keep running autoballast |
| `c_speed_min` / `c_speed_max` | Slowest / fastest allowed depth rate for speed control (set per dive/climb) |
| `f_depth_rate_method` | Which filtered depth rate drives speed control (default `3` = running average, `m_depth_rate_avg_final`) |
| `c_time_ratio` | Climb/dive time ratio that must be maintained (default 1.1) |
| `c_wait_for_pitch` / `c_wait_for_ballast` | Let pitch and ballast settle after an inflection before enabling speed control |
| `u_diveclimb_msg_print` | Verbosity of autoballast messages (`-1` none, `0` errors, `2` basic, `99` all) |

### `c_autoballast_state` values

| State | Meaning |
|-------|---------|
| `0` | Uninitialized — set this to **reset/reinitialize** autoballast |
| `1` | Initialized, still converging |
| `2` | **Converged successfully** |
| `3` | Converged unsuccessfully — a dive/climb amount hit the pump's max (`X_BALLAST_PUMPED_MAX` / `X_DE_OIL_VOL_MAX`) |
| `4` | Converged unsuccessfully — the climb−dive spread is below your requested total |
| `5` | Converged unsuccessfully — more complex; examine the `.mlg` |

---

## Setting it up

Autoballast is configured through behavior arguments, and it must be specified in
**two places**:

- The **`yo`** (or **`drift`**) behavior — the diving behavior, via the
  `b_arg: d_bpump_value(X)` total drive (and the speed-control args such as the
  minimum depth rate).
- **Every `surface`** behavior — so the reduced drive is used on the surface too,
  not just while diving.

The TWR software release ships a standard autoballast mission (historically
**`astock.mi`**, using `yo14.ma` and the `surfac2x.ma` surface files) — the
easiest starting point is to base your mission on that template rather than
wiring it up from scratch.

!!! warning "Don't set the total below `f_min_ballast`"
    If `d_bpump_value` is smaller than `f_min_ballast` (default **250 cc**), the
    mission **aborts**. Review the masterdata description before lowering
    `f_min_ballast` itself.

!!! tip "Shallow water: trim the first dive by hand"
    Autoballast **starts at full `±1000 cc` drive** and works down. In shallow
    water with a small target altitude, that first full-drive dive can drag the
    bottom before autoballast converges. **Reduce `c_dive_bpump` before the
    initial dive** to avoid bottom-sampling on the way to a converged solution.

---

## Monitoring

Watch these in the surface dialog every piloting day:

- **`c_autoballast_state`** — is it at `2` (converged successfully)? A `3`/`4`/`5`
  means it could not converge on the drive you asked for.
- **`c_dive_bpump` and `c_climb_bpump`** — the live drive amounts. A healthy
  solution is roughly symmetric around zero; a lopsided pair means the glider is
  out of trim (ballast, density, or a stuck pump).
- **Dive and climb speeds** vs. your `c_speed_min` — if the glider keeps bumping
  the minimum it will keep adding drive (and energy).

Raise `u_diveclimb_msg_print` to `2` (basic) if you want autoballast to narrate
what it is doing.

---

## Resetting autoballast in the field

Autoballast converges to the **water it converged in**. If you move into water of
very different density (or it just isn't doing a good job), you can make it
**reinitialize without exiting the mission** by forcing the state back to
uninitialized from a surface dialog:

```
!set c_autoballast_state 0
```

It then re-converges from full drive over the next several yos.

!!! warning "Reinitializing costs a little energy and re-runs the motors"
    When you reset it, the buoyancy (and pitch) motors work to re-find the
    solution, and the glider briefly flies on full drive again. That's usually
    fine, but in **shallow water** remember it restarts at `±1000 cc` — re-apply a
    reduced `c_dive_bpump` for the first dive if bottom clearance is tight.

!!! danger "A glider reset reverts to masterdata defaults"
    If the glider **resets** during a deployment (power cycle, `exit reset`,
    watchdog), `c_dive_bpump` / `c_climb_bpump` go back to the masterdata defaults
    of **`±1000 cc`** and autoballast starts converging from scratch. After any
    reset in shallow or busy water, check the drive before the next dive.

**If autoballast seems stuck or sluggish**, operators nudge it by changing the
**total** drive a little and back — e.g. raise the total to ~450 cc, then bring it
back to 400 or 375 — and re-checking the dive/climb speeds. And be aware that
autoballast has **limits**: if the surface density is far from where it converged,
the glider can reach the **end of its ability to compensate** and fly poorly until
you reset it (or adjust trim).

---

## Simulation caveat

!!! note "Simulate with full buoyancy, not a converged solution"
    Run simulations at **full drive** (`d_bpump_value −1000`, `c_bpump_value
    +1000`). If a simulated dive or climb stalls ("WE GOT STUCK not moving
    vertically"), confirm full drive is set in the yo dive/climb behaviors and
    check the simulated bottom (`s_water_depth_avg`) and altimeter-on depth
    (`u_alt_min_depth`). Autoballast's drive-reduction is meant to converge in
    **real water**, not the simulator.

---

## See also

- [Power Saving](power-saving.md) — autoballast in the wider energy-conservation
  picture (reduced drive, gentle pitch, drift-at-depth).
- [Pitch Vernier](../../glider-components/slocum/pitch/index.md) — pitch trim,
  which works alongside autoballast to set flight angle.
- [Shallow Pump](../../glider-components/slocum/pumps/shallow-pump/index.md) /
  [Deep Pump](../../glider-components/slocum/pumps/deep-pump/index.md) — the drive
  autoballast is commanding, and `c_autoballast_state 0` as a pump-troubleshooting
  step.
- [Aborts](aborts.md) — `f_min_ballast` and convergence failures as abort causes.
