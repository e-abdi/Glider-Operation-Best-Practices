---
title: Trim & Flight Model
description: Trimming a Seaglider and working with the Flight Model System — pitch trim ($C_PITCH, $PITCH_GAIN, $PITCH_VBD_SHIFT), the Pitch Adjuster, pitch-over-VBD for endurance, buoyancy trim and $C_VBD, roll trim, estimating volmax in a tank before sea trial, and when to apply the FMS-recommended $HD_A / $HD_B values on the glider.
---

# Trim & Flight Model

Trimming — teaching the glider's control model to match how the vehicle
actually flies — is where most of a Seaglider pilot's early-mission effort
goes. Pitch trim is arguably the **single biggest influence on flight**: a
well-trimmed vehicle flies cleanly on both profiles, dives and climbs in about
the same time, and wastes far less energy on the VBD; a badly trimmed one
burns battery, and sometimes doesn't fly at all. This page covers the practical
trimming workflow (pitch, then buoyancy, then roll), pre-deployment ballasting,
and the basestation's automated Flight Model System (FMS).

!!! info "Source"
    Paraphrased from the APL-UW IOP office-hours series (pitch trimming;
    ballasting and volmax; flight-model questions) and webinar series
    (*Piloting with basestation3*), the UW *Determining Seaglider Velocities
    Automatically* flight-model paper (Bennett, Stahr & Eriksen), and the
    APL-UW *SGX Documentation*. Numbers quoted here are IOP starting points,
    not gospel — confirm parameter definitions in the
    [Parameter Reference Manual](https://iop-apl-uw.github.io/basestation3/html/Parameter_Reference_Manual.html)
    and defer to APL-UW IOP guidance.

---

## Ballasting before the mission: estimating volmax in a tank

Before a sea trial, the glider needs lead trimmed so that its maximum volume
(`volmax`) gives the right thrust in the density of the operating area. IOP's
tank procedure:

1. Weigh the glider in air to get its mass **M**.
2. Soak it **overnight**, fully submerged, in a freshwater tank.
3. Compute the tank water density **ρ<sub>tank</sub>** from temperature (and
   salinity if a saltwater tank).
4. With an accurate scale, measure the glider's weight in water **W<sub>i</sub>**
   at an intermediate VBD position **VBD<sub>i</sub>** (e.g. 2000 A/D counts).
5. Compute volmax:

    ```
    volmax = (M − Wi) / ρtank + ($VBD_MIN − VBDi) × VBD_CNV
    ```

    where `VBD_CNV = −0.2453 cc/AD count`, `$VBD_MIN` (~400 counts) is bladder
    **full** and `$VBD_MAX` (~3960 counts) is bladder **empty** — note the
    counter-intuitive naming: *smaller counts mean more volume*.

6. Repeat at several VBD positions (IOP uses 2000, 2250, 2500, 2750, 3000
   counts) and average.
7. Compute the target mass for the desired thrust and target density with the
   **Tools → Ballast worksheet** in vis.

!!! note "It's only a rough number"
    The tank estimate is good to perhaps **±100 cc**. The real value is
    refined in the water: FMS regressions and the `mission_volmax` /
    `FM_vbdbias` plots converge on the true volume over the first dives.

---

## The trimming workflow

After launch, the plots to live in are the first few in the vis plot ribbon:
the **dive plot**, the **vertical-velocity regressions**, the **pitch
regressions**, and the **roll regressions**. The classic order of work, easiest
and highest-impact first:

1. **Pitch** — often meaningful after a single dive.
2. **Buoyancy ($C_VBD)** — from the vertical-velocity regression.
3. **Roll** — needs straight-flight data, so it firms up later.

The regressions all follow the same idea: the plot shows what the glider
*observed* against what its on-board control model *predicted*, and the fits
propose new model parameters that would bring the prediction onto the
observation. The RMS quoted with each fit tells you how much better it would
be. When a regression is confusing, go back to the dive plot, turn off all
traces except the one you care about (desired vs. observed pitch, say), and
reason it out directly — the two views should tell the same story.

### Pitch trim

The design principle: absent VBD changes, a fixed battery-mass position should
produce a constant vehicle pitch. On the dive the VBD barely moves after the
initial bleed (confined by `$D_NO_BLEED`), so pitch is essentially set once;
on the climb the VBD is the primary speed control, and the resulting pitch
change is compensated through `$PITCH_VBD_SHIFT`.

| Parameter | Meaning |
|-----------|---------|
| `$C_PITCH` | Battery position (A/D counts) for level (neutral) pitch |
| `$PITCH_GAIN` | Degrees of vehicle pitch per cm of pitch-mass movement |
| `$PITCH_VBD_SHIFT` | VBD displacement expressed as equivalent mass-shifter movement (cm/cc, default 0.00167) — compensates pitch for oil moving fore/aft |

Three fits appear on the pitch regression, in increasing sophistication:

- **Linear fit** — new `$C_PITCH` and `$PITCH_GAIN`. Most reliable, good
  first move when far out of trim.
- **Non-linear fit, shift held fixed** — accounts for the VBD's effect using
  the current `$PITCH_VBD_SHIFT`. Robust; a good default go-to.
- **Non-linear fit including shift** — also fits a new `$PITCH_VBD_SHIFT`.
  Historically the shift was treated as a constant of the mass-shifter type,
  but fitting it works well *once the glider is roughly in trim*; be careful,
  as the fit can dump too much variability into the shift at the expense of
  the gain.

!!! tip "Reading pitch on the dive plot"
    Isolate desired vs. observed pitch on the dive plot. If the dive and climb
    offsets from desired are about equal, the **center is close**. If the
    glider consistently *doesn't pitch as far as asked*, the mass isn't moving
    far enough — the **gain needs to come down** (lower gain = more mass
    movement per degree). A well-trimmed glider shows a symmetric depth trace:
    dive time ≈ climb time.

#### The Pitch Adjuster — for gliders that have changed

After a refurb, a lead change, or a sensor swap, `$C_PITCH` may be so far off
that the first dives are too ugly for the regressions to mean anything. The
*Pitch Adjuster* enables closed-loop pitch control so the glider flies well
enough to gather useful regression data:

- `$PITCH_ADJ_GAIN` — enables the loop; correction = (desired − observed) ×
  gain, in cm/degree. Starting point: **0.03**.
- `$PITCH_ADJ_DBAND` — deadband in degrees before the adjuster acts.
  Starting point: **1**.

IOP practice is to **start missions with the adjuster on** so `$C_PITCH` can
be established, then turn it off once the glider is diving deep and confirm it
is no longer needed (it usually isn't). For chronically hard-to-trim vehicles,
running the whole mission with a light adjuster gain is a legitimate strategy.

#### Pitch-over-VBD — trimming for endurance

The glider's native reaction to flying slow is to pump — and pumping at depth
is the most expensive thing it does. Momentary slowdowns (internal waves, roll
coupling, flight near stall) can trigger pumping that was never needed. Two
defenses, generally switched on after dives ~15–20 once basic trim is done:

| Parameter | Role | Typical value |
|-----------|------|---------------|
| `$W_ADJ_DBAND` (cm/s) | Deadband on *VBD* speed corrections — only act when \|w_obs\| < \|w_desired\| − deadband. Set near the RMS w variability so internal waves stop triggering pumps | 3 |
| `$PITCH_W_DBAND` (cm/s) | Deadband on *pitch* speed corrections | 0.5 |
| `$PITCH_W_GAIN` (cm per m/s) | Gain for correcting speed with pitch instead of the pump (climbs only). Positive = only speed up a slow glider; negative = corrections both ways | 3 (range ~2–10) |

!!! warning
    `$PITCH_W_GAIN` and `$PITCH_ADJ_GAIN` cannot be used at the same time —
    finish establishing `$C_PITCH` first, then switch strategies.

### Buoyancy trim — `$C_VBD`

The vertical-velocity plot shows desired w (classically 10 cm/s), observed w
(from pressure), and the on-board hydro model's prediction. Early in a mission
the standard move is the **buoyancy-only fit**: adjust `$C_VBD` (the neutral
VBD position) until the model rides on the observations. Later, the **full
flight-model fit** (buoyancy + lift + drag) and the **three-dive regression**
— which pools the last three dives for a wider flight regime — refine things
further. Remember that stratification shows up here too: a slow climb isn't
necessarily bad trim, it may just be lighter water.

### Roll trim

Two plots, and a heuristic:

- **Roll control vs. roll** — where the battery mass is rolled vs. how the
  vehicle actually rolled. Useful, but not the goal in itself.
- **Roll-rate regression** — observed *heading change* vs. roll position,
  fitted with **separate centers for dive and climb** (the vehicle is
  asymmetric; remember it banks opposite senses on dive vs. climb). The
  "centered" fit uses only straight-flight data, so it needs longer dives
  before it means much.

What actually matters is not flying flat but flying **straight** — and, in
current, pointing at the target. The dive-plot heuristic: turn everything off
except roll and heading. Diving with heading *decreasing* (turning left) →
**decrease** the roll center; heading *increasing* → **increase** it.

---

## The Flight Model System (FMS)

Seagliders have no speedometer; speed through water is inferred from a steady
flight model balancing buoyancy, lift, and drag. The basestation's **Flight
Model System** runs the regressions automatically and consistently for **every
dive** of a mission, estimating the lift/drag coefficients (`$HD_A`, `$HD_B`
— `$HD_C` is held constant) and the volume offset (`vbdbias` / volmax) that
best explain the observed vertical velocities. Those estimates feed the
hydro model used for CTD flushing corrections, depth-averaged currents, and
science processing — and FMS issues recommendations the pilot *may* apply to
the glider itself.

This replaces the old hand-run `regress_vbd` MATLAB workflow (and derivatives
like the Seaglider Toolbox), which required careful manual data selection and,
done badly, could actively hurt navigation when the results were applied to
the glider. It also tracks changes over a deployment — biofouling and damage
show up as drifting coefficients — where the old approach assumed one
characterization for the whole mission.

### When to copy FMS values onto the glider

The on-glider `$HD_A/B/C` affect how the glider *chooses* pitch and VBD (and
heading, under `$NAV_MODE,2`/`3`, plus the informational `$IMPLIED_C_VBD`).
The basestation's per-dive values affect *data processing*. They do not need
to match dive-by-dive. IOP practice:

- Update the glider **once or twice over the first 10–20 dives**, then leave
  it alone and just monitor the `FM_ab_dives` plot for any sustained trend
  worth capturing.
- Unless the on-glider values are so far off that the hydro model thinks the
  glider is stalled (or QC flags it as flying too slow), they can be left
  alone. When those problems *do* appear, the culprit is usually **not**
  `$HD_A/B/C` — it's almost always something like a wrong `mass` in
  `sg_calib_constants.m`.
- Applied an update and flight got worse? Just switch back to the previous
  values.

!!! danger "Mass is baked in at dive 1"
    FMS bases everything on the vehicle mass in `sg_calib_constants.m` at
    **dive 1** — changing the file mid-mission does not re-baseline it, and a
    wrong mass is the classic way to send the whole hydro model (and the CTD
    corrections downstream of it) off the rails. Weigh carefully, enter it
    once, get it right. Similarly, bad conductivity data will corrupt the
    density input to the model — a step change in the `mission_volmax` or
    `FM_vbdbias` estimates can be the first symptom of a CT problem rather
    than a real volume change.

### Reprocessing old missions

Any previous mission can be re-run through the modern FMS: install
basestation3 locally (Linux and macOS supported) and use **`Reprocess.py`**,
which starts from the `.log`/`.eng` files of a previous conversion and
regenerates netCDFs and plots (`Base.py` is the full pipeline from raw
transmitted files — more than you usually need). View the results with a local
`vis.py`. Most missions reprocess cleanly; seaglider.pub users are asked to
reprocess on their own machines.

---

## Tactics: strong currents and making progress

Trim feeds directly into how well the glider handles current. IOP guidance for
surface-intensified currents, kayaker-style — don't fight it head-on,
cross it perpendicular unless it's pushing you the right way:

| Lever | Effect |
|-------|--------|
| Dive deep and long — or short and fast | If there's calm water below the current, spend the dive in it; if not, get through the layer quickly |
| Keep targets 5–10 km out with big radii | Close targets make the glider fly steep, low-buoyancy dives; far targets keep flight efficient (`ExtraTargetsAlongLine.py` in basestation3 tools helps seed intermediate waypoints) |
| Tune roll | Forward progress depends on actually pointing at the target |
| `$NAV_MODE,2` (or `3`) | Usually the right navigation mode; `3` steers relative to current; `$NAV_MODE,0` + `$HEADING` when you must take manual control |
| Reduce `$SM_CC` | Less surface pumping = less time drifting on the surface (max useful value is `($VBD_MIN − $C_VBD) × VBD_CNV`; may be overridden per `$NOCOMM_ACTION`) |
| Deepen `$D_FLARE` | Faster initial descent through the surface layer |
| Lower `$T_DIVE` relative to `$D_TGT` | Steeper pitch — usually *better* horizontal speed |
| Raise `$MAX_BUOY` | More thrust; typical ballasting leaves headroom beyond the usual ~250 cc — works best combined with steeper pitch |

---

## See also

- [Dive Cycle & Control Files](dive-cycle-and-control-files.md) — where
  `$C_VBD`, `$MAX_BUOY`, `$D_FLARE` and friends fit in the dive; deck-dive
  data hygiene that keeps FMS running.
