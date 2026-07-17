---
title: Compass Calibration
description: The Seaglider compass and how to calibrate it — hard vs. soft iron, tcm2mat.cal, $COMPASS_USE and raw magnetometer data, per-dive and multi-dive calibration in basestation3, onboard autocal for under-ice missions, judging a calibration result, and the classic shore "whirly" and in-flight calibration procedures.
---

# Compass Calibration

The Seaglider computes heading from a 3-axis magnetometer plus a 3-axis
accelerometer: the accelerometer gives pitch and roll, which are used to
rotate the measured magnetic field into earth coordinates, and the horizontal
field then points at magnetic north. Everything the glider does with that
heading — steering, roll trim, depth-averaged currents, the smarter
`$NAV_MODE`s — is only as good as the compass calibration, and IOP's guidance
is blunt: **some form of compass calibration should be applied for every
mission.**

!!! info "Source"
    Paraphrased from the APL-UW IOP *SGX Documentation* (§4.4.3), IOP webinar
    3 (*Basestation3 CLI and customization + glider compass calibration*), and
    the UW *New compass calibration procedures for Seagliders* note (Bennett,
    2012 — the "whirly" and in-flight procedures). Defer to APL-UW IOP for
    current tooling.

---

## Hard iron, soft iron, and what the calibration does

The field the magnetometer measures is the sum of the earth's field and the
glider's own magnetic signature:

- **Hard iron** — materials with their own permanent field (the steel in
  battery-cell casings is the classic one). It rides in the compass's own
  coordinate frame, so it appears as a constant **offset** on each axis.
  Usually — but definitely not always — the larger error source.
- **Soft iron** — materials that become magnetized in the presence of another
  field. Its effect changes with orientation, **stretching and rotating** the
  measurement.

Picture a glider tumbling through every orientation in a clean environment:
the tip of the measured field vector sweeps out a **sphere centered on the
origin** (the earth's field is constant in magnitude). Hard iron shifts that
sphere off the origin; soft iron squashes it into an ellipsoid. Calibration
is simply finding the transformation that turns the measured ellipsoid back
into a sphere on the origin: an offset vector `(p, q, r)` for hard iron and a
3×3 matrix for soft iron.

Those numbers reach the glider through the **`tcm2mat.cal`** control file:

```text
hard0="p q r"
soft0="a b c d e f g h i"
```

Drop the file into the glider's mission (or home) directory on the
basestation and it uploads on the next call, exactly like `targets` or
`science`, with the sent copy archived with dive/call numbers appended. If
only `hard0` is present, only the hard-iron correction is applied. In a
perfectly clean environment the solution would be `hard0="0 0 0"` and an
identity matrix — small hard-iron values and near-identity soft iron mean a
clean magnetic environment, not a wasted effort.

## Calibrate every mission — and prefer in-situ

The calibration changes even when the glider doesn't: sitting in storage,
riding in a steel shipping container, or lying on a ship's deck can all
re-magnetize the hard iron. A land calibration done before shipping may be
stale by launch day. For that reason IOP now skips the land calibration
entirely and **calibrates in situ** during the first dives of the mission.

Two facts make this easy:

- **No absolute heading reference is needed.** The math never uses "true"
  heading — a known orientation is only useful as an error metric afterwards.
  In-situ calibration works in open water.
- **`$COMPASS_USE` must be at least 4** so the glider sends back the raw
  magnetometer field with every sample, alongside pitch/roll/heading. It is
  the default in modern firmware, but double-check — without the raw field
  data no calibration (during or after the mission) is possible, and there is
  no downside to always collecting it.

## Computing a calibration on the basestation

Three routes, all producing the same `hard0`/`soft0` lines:

| Route | When |
|-------|------|
| **Per-dive plot in vis** | Automatic — every dive gets a calibration result and plot in the plot ribbon (unless the numerics fail to converge) |
| **Tools → Compass calibration in vis** | Multi-dive regression: pick a set of dives (e.g. 76, 77, 115, 117) and get a combined solution with scores |
| **`Magcal.py`** | Same engine from the command line, single or multiple dives |

Modern firmware also reports the calibration *actually in use* in the `iron`
line of each dive's log file — so reprocessing always knows how the data was
corrected on board.

### Picking dives: coverage is everything

The solver wants points spread around the sphere, and a well-trimmed glider
holding one heading gives it the opposite — a short arc on one side of the
circle. Ways to get good coverage:

- Select dives **on either side of a target change** (different legs =
  different headings; reciprocal or orthogonal legs are ideal).
- **Early-mission dives are often better** than late ones: before roll is
  trimmed the glider wanders and turns more, which is bad for flying and
  great for calibration data.
- If needed, fly deliberate calibration dives — box the compass over a few
  dives on set headings, mixing steep and shallow pitch — though in practice
  natural variability usually suffices.

### Judging a result

- **Hard iron** should be consistent dive-to-dive (or between multi-dive
  groups). A jumpy hard-iron solution means a poor dataset, not a changing
  glider.
- **Soft iron** diagonal terms should be reasonably close to 1 (values down
  to ~0.8 happen, and SGX tends to show stronger soft iron than SG). A
  diagonal term of 0.2–0.4, or off-diagonal terms as large as the diagonals,
  means something is off — re-run with different dives before sending it to
  the glider.
- **Look at the plot**: is the corrected circle round, gap-free, and centered
  on zero? The quoted score is literally the RMS deviation from circularity —
  smaller is better, zero is a perfect circle.
- **If soft iron doesn't converge** you get a hard-iron-only solution. Early
  in a mission, apply it anyway — most of the error is usually hard iron, and
  some correction beats none.

## Onboard autocal (`$COMPASS_USE` bit 14)

Setting bit 14 of `$COMPASS_USE` (add **16384**) makes the *glider itself*
run a rolling three-dive calibration after every dive, logged in a `magcal`
entry with the hard/soft vectors, quality and coverage scores, and whether it
was applied. Additional bits let the glider **automatically adopt** a result
that passes the quality thresholds (the thresholds themselves are tunable
via extra variables in `tcm2mat.cal`, though changing them is rarely needed).

This was built for **under-ice missions** — launch through a hole in the ice,
no data back for months, so no basestation calibration is possible — but it
also works as a set-and-forget option in open water. IOP commonly flies with
autocal on just to watch how the onboard solution tracks the basestation one.

---

## The classic UW procedures

The MATLAB-era procedures below predate basestation3 (which has replaced the
analysis side), but they remain the reference for *how to move the glider*
to collect calibration data — and the shore procedure is still the way to get
a starting `tcm2mat.cal` onto a glider before first launch. The empirical
finding behind both: sampling complete 360° turns at **two roll angles (port
and starboard) and a couple of modest pitch angles** (±15° and ±30°) is
sufficient for ~1.2° RMS heading accuracy.

??? note "Shore 'whirly' calibration"
    Find a magnetically quiet spot (a parking lot works) away from large
    metal objects. Mount the pupa in a shop jig on a smooth surface that
    spins freely — no calibrated fixture needed. If not at a surveyed site,
    record a GPS position and date (the analysis needs the local geomagnetic
    field, which the script looks up).

    Start a terminal capture, power the glider, and run
    `hw/compass/whirly` (**not** `whirlraw`). Then, with data streaming:

    1. Roll the glider ~30° to **port**, pitch ~30° **down**, and rotate the
       jig through a full 360° taking about a minute (slow spins = good data
       density; direction doesn't matter).
    2. Repeat the one-minute spin at −15°, +15°, and +30° pitch (0° is
       skipped — a glider never flies flat). Four spins per roll side.
    3. Set level, roll ~30° to **starboard**, and repeat the four spins.

    None of the angles need to be precise — watch the streamed values and get
    close. Quit (`Ctrl-Q`), power off, close the capture, and run the
    analysis (historically the `whirlymagcal` MATLAB script) to produce the
    `tcm2mat` file for the glider.

??? note "In-flight calibration dives (forced-spin recipe)"
    The in-flight equivalent collects the same four combinations over **two
    dives to roughly 120–150 m** near each other: one dive spinning with a
    constant **port** roll at ±15° pitch, the other with a constant
    **starboard** roll at ±30° pitch. Each dive and climb must complete at
    least one full 360° turn.

    Setup (record the operational values first, restore after):

    - Temporary `science` file sampling every **5 s** to 200 m (dense
      heading/magnetometer data).
    - `$COMPASS_USE,4` — the raw magnetometer data is the whole point.
    - `$HEAD_ERRBAND,180` — stop the glider from actively steering.
    - `$C_ROLL_DIVE` and `$C_ROLL_CLIMB` set to the roll A/D limit
      (`$ROLL_MIN` for the port-spin dive, `$ROLL_MAX` for starboard) with
      `$ROLL_DEG,0` — forcing a static full roll, hence a steady spin.
    - `$GLIDE_SLOPE` 15 (first dive) / 30 (second), with `$D_TGT`/`$T_DIVE`
      sized for the pitch (e.g. 150 m / 50 min for the shallow-pitch dive).

    With basestation3, feed the resulting dives to the compass-calibration
    tool and install the suggested `hard0`/`soft0` in `tcm2mat.cal`.

!!! tip "Wanding without magnetizing the glider"
    Gliders with magnetic reed switches: rather than waving the magnet wand
    around the hull, bring it gently to the marked spot and **rotate it once
    about its own axis, like a lollipop**. The rotating field engages the
    reed switch reliably while minimizing hard-iron changes to the forward
    battery cladding — exactly the thing you just calibrated away.

!!! warning "Deepglider is different"
    The procedures above assume the moving battery pack's position doesn't
    change the hard/soft-iron fields — measured to be true for Seagliders.
    On **Deepglider** the HV pack sits much closer to the compass and this
    assumption fails; it needs its own calibration and correction scheme.

---

## See also

- [Trim & Flight Model](trim-and-flight-model.md) —
  roll trim runs on heading change, so it depends directly on a good
  calibration.
- [Batteries](../../glider-components/seaglider/batteries/index.md) — the
  steel in the packs is the main hard-iron source; battery work warrants a
  compass check.
- [Dive Cycle & Control Files](dive-cycle-and-control-files.md) —
  how `tcm2mat.cal` flows to the glider with the other control files.
