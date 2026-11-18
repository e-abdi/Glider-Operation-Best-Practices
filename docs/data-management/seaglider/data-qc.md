---
title: Data Quality Control
description: Where Seaglider data gets quality-controlled, from the glider to the basestation and the scientist — what the glider itself does (and doesn't), data completeness and basestation alerts, the basestation3 automated QC (QC flags, GPS, depth, CT bounds and spike tests, VBD-bleed and slow-apogee checks, conductivity anomalies, thermal-inertia and legato corrections, DAC and oxygen checks), the Flight Model System's role, manual QC with sg_directives.txt, the QC parameters in sg_calib_constants.m, and common pitfalls.
---

# Data Quality Control

Seaglider QC is built in layers, loosely patterned on Argo. The **glider**
records raw measurements and does almost no data QC of its own. The
**basestation** converts every dive into a per-profile NetCDF file and runs
a fully automated QC pass on it, the equivalent of Argo's *real-time* QC.
The **scientist** can then review each profile and override the automated
result with directives, the equivalent of *delayed-mode* QC.

!!! info "Source"
    Paraphrased from the UW *Seaglider Quality Control Manual* (v1.15 with
    revisions to 2023, shipped as `docs/Seaglider_Quality_Control_Manual.html`
    in the [basestation3 source](https://github.com/iop-apl-uw/basestation3)),
    the basestation3 code itself (`MakeDiveProfiles.py`, `QC.py`, checked
    October 2026) and its *Alerts Reference Manual*, the APL-UW IOP
    *Basestation3 best practices* note and *SGX Documentation*, the 2026 IOP
    office hours on the flight model and on basestation data processing, and
    operator correspondence. Where the manual and the code differ, this page
    follows the code. Defaults change between releases, so check
    `sg_config_constants()` in `MakeDiveProfiles.py` for your version, and
    defer to APL-UW IOP.

---

## Where QC happens

| Stage | What it does | Who acts on it |
|---|---|---|
| On the glider | Records raw values (frequencies, phases, counts), converts pressure to depth for its own use, logs timeouts and warnings. No data flagging | Pilot, through the log and self-test |
| Self-test | Checks sensors before launch; provides in-air reference values used later in processing | Pilot / technician |
| Transfer and alerts | Files arrive in fragments; incomplete dives can be re-requested. The basestation raises alerts for timeouts, CT parse errors, mismatched constants | Pilot |
| Basestation, automated | Bounds and spike tests, corrections, per-point QC flags, per-dive overall flags | Runs on every call-in |
| Flight Model System | Estimates speed through water, which the CTD correction and currents depend on | Runs on every dive; pilot watches its plots |
| Manual review | `sg_directives.txt` marks or un-marks points and profiles, then reprocesses | Scientist |

---

## On the glider

The glider's job is to record, not to judge. It stores what the instruments
report, mostly in raw form. The Sea-Bird CT sail logs temperature and
conductivity **frequencies**, the optodes log phases, and the conversion to
physical units happens on the basestation using `sg_calib_constants.m`, not
the coefficients loaded on the glider. Those onboard coefficients are only
used for the glider's own density estimate (see
[Sensor Configuration](../../glider-components/seaglider/sensors/index.md#ct-sail-sbe)).

What the glider does provide for QC:

- **Depth from pressure.** The glider converts pressure to depth onboard with
  a fixed linear factor for its own control. The basestation inverts this to
  recover pressure, then recomputes a proper depth using latitude. A pressure
  sensor that wasn't zeroed at sea level shows up later as the CT apparently
  being out of the water. See [Pressure Sensor](../../glider-components/seaglider/pressure-sensor/index.md).
- **Timeouts and warnings.** The last field of the `$ERRORS` line in each
  dive log counts sensor timeouts, and the glider writes `$WARN` lines for
  problems such as timeouts, unreadable CT output and compass-calibration
  errors. A sample that was expected but never arrived ends up flagged as
  missing in the NetCDF file. The basestation turns these into alerts
  (next section).
- **Self-test reference values**, used by the basestation:
    - **CT sail.** Put `sbe_cond_freq_C0` (the zero-conductivity frequency
      from the cal sheet, about 2900 Hz) in `sg_calib_constants.m`. The
      self-test then reports the measured in-air conductivity frequency next
      to the calibration value, which is a quick sanity check on the
      conductivity cell and its calibration.
    - **RBR legato.** The self-test's sea-level pressure reading goes into
      `legato_sealevel`. If it is missing, the basestation raises a
      `MISSING_SEALEVEL` alert and assumes a default value.
    - **Optodes.** In-air optode readings and sea-level pressure from the
      self-test let the basestation correct optode calibration drift.

!!! tip "Keep a self-test in every mission directory"
    Some vis and basestation features, including the self-test history,
    only work when at least one self-test sits in the mission directory
    listed in `missions.yml`. It also makes later troubleshooting much
    easier.

---

## Checking data completeness

QC can only work on data that arrived. After each dive:

- Compare the size of the processed `p*.dat` file with the first number on
  the `$DATA_FILE_SIZE` line of the dive's `.log` file.
- With SciCon, check the per-dive and per-climb directories for the
  expected `.dat` / `.eng` files.
- Where pieces are missing, `comm.log` shows which fragment didn't complete.
  Queue it for retransmission at the next surfacing with `resend_dive` in
  `pdoscmds.bat`. You can resend a whole dive or just specific fragments.

### Basestation alerts worth watching

Basestation3 checks each call-in and sends alerts (by email or other
channels set up in `pagers.yml`). The ones that bear on data quality:

| Alert | What it means |
|---|---|
| `CONVERSION_ISSUES`, `BAD_DATA_FILE` | Fragments missing, partly uploaded or corrupted. Usually fixed with `resend_dive` |
| `TIMEOUT` | A sensor timed out more than the threshold (default 5) in one file. A few per dive are tolerable for serial sensors. For frequency sensors such as the CT sail, any timeout is a warning sign |
| `GLIDER_TIMEOUT` | More than 3 timeouts of one kind (pressure, GPS PPS…) in a dive |
| `CT_PARSE_ERRORS` | More than 3 unreadable CT records in a dive. Hundreds mean a failing or flooded CT, or a wiring or configuration problem. Treat that dive's CT data as suspect |
| `TCM2MAT_ERROR` | Repeated errors applying the compass calibration. Headings, and so the currents, may be wrong |
| `SBECT_COEFFICIENT` | The CT coefficients on the glider differ from `sg_calib_constants.m`. Small differences are normal (see [Sensor Configuration](../../glider-components/seaglider/sensors/index.md#ct-sail-sbe)) |
| `MISSING_SEABIRD_CAL`, `INCORRECT_CT` | CT calibration missing, or legato data found without `sg_ct_type = 4` |
| `MASS_MISMATCH` | `mass` in `sg_calib_constants.m` differs from `$MASS` on the glider. The basestation uses the file's value |
| `GPS_HORIZONTAL_ERROR` | A GPS fix's error is larger than allowed (`GPS_position_error`) |
| `BAD_GPCTD_CLOCK` | The GPCTD's clock is wrong, so its data falls outside the dive and is thrown out |
| `FMS`, `FMS_DECK_DIVES` | Flight-model warnings, e.g. a large rise in drag (possible biofouling), too few different pitches to fit drag, or FMS not running because deck dives are in the mission directory |

---

## The basestation pipeline

For each dive the basestation decodes the transmitted `.dat` files into
`.asc` and `.eng` files, reads the `.log` file, runs the corrections and
QC, and writes one **NetCDF file per dive**. Plots are drawn from the
NetCDF files.

- **Inputs.** Per dive: the `.log` and `.eng` files. Per deployment:
  `sg_calib_constants.m` (calibrations, vehicle constants, QC settings) and
  an optional `sg_directives.txt` (manual QC). The `cmdfile`, `science` and
  `targets` files are not used.
- **Raw data is never lost.** The `.nc` file keeps every uncorrected
  variable alongside the corrected ones, so a profile can be reprocessed
  from the `.nc` file alone.
- **Reprocessing happens automatically** when an input is newer than the
  `.nc` file, for example after editing `sg_calib_constants.m` or
  `sg_directives.txt`. To reprocess a whole mission, use `Reprocess.py`
  (from existing `.log`/`.eng` files) or `Base.py --force` (from the
  original transmissions). See
  [Trim & Flight Model](../../piloting/seaglider/trim-and-flight-model.md#reprocessing-old-missions).
- **Sensor extensions** run after the CTD and speed corrections and can add
  their own QC. One example marks parts of a passive-acoustic spectrum
  recorded while a motor was running. By convention an extension never
  changes an existing column; it adds new ones (e.g. a corrected
  `conductivity_offset`).
- **Suggestions.** Where the automated QC suspects a problem but won't act
  on its own (deep conductivity anomalies, possible warm-water pulses), it
  writes a ready-made directive to `sg_directives_suggestions.txt` in the
  mission directory. Copy the ones you agree with into `sg_directives.txt`.

### QC flag values

Every QC'd variable has a parallel `_qc` variable using Argo-style codes:

| Code | Name | Meaning |
|:-:|---|---|
| 0 | `QC_NO_CHANGE` | No QC performed |
| 1 | `QC_GOOD` | Trustworthy |
| 2 | `QC_PROBABLY_GOOD` | Likely good |
| 3 | `QC_PROBABLY_BAD` | Suspect, possibly correctable |
| 4 | `QC_BAD` | Untrustworthy and uncorrectable |
| 5 | `QC_CHANGED` | Changed manually |
| 6 | `QC_UNSAMPLED` | Deliberately not sampled |
| 8 | `QC_INTERPOLATED` | Value replaced by interpolation |
| 9 | `QC_MISSING` | Expected but missing (instrument timed out) |

---

## Automated QC, step by step

### GPS fixes

Three fixes matter for each dive: GPS1 (on surfacing), GPS2 (just before
diving) and the final fix (which becomes the next dive's GPS1). If the
times are out of order (GPS2 not after GPS1, or the final fix not after
GPS2), the dependent calculation (surface drift or depth-averaged current)
is flagged `QC_BAD` and skipped. The position error is the receiver's
reported error, or `GPS_position_error` (default 100 m). Positions are
**not** checked against land.

### Depth and CT depth

Depth is recomputed from pressure using the dive's average latitude. For
an unpumped CT the basestation also works out the depth of the CT itself
from the vehicle's pitch and the sail's geometry. A pumped CTD reports its
own pressure. Any point where the CT is **above the surface** (negative CT
depth) gets its conductivity marked `QC_BAD`. That happens in high seas, on
breaching during the surface maneuver, or when the pressure sensor wasn't
zeroed. In the last case, correct it with `depth_bias`. Pressure is not
checked for being monotonic on the dive or climb.

Other pressure options in `sg_calib_constants.m`: `depth_slope_correction`
for data recorded with a wrong pressure slope, and `smooth_truck_pressure`
(off by default) to smooth a noisy glider pressure signal. A legato's own
pressure channel is despiked automatically, and the despiked points are
marked `QC_INTERPOLATED`.

### Temperature, conductivity and salinity

Every sampled point starts as `QC_GOOD` and unsampled points as
`QC_UNSAMPLED`. On the **raw** values:

1. **Frequency bounds** (unpumped CT only, if you set them) mark
   out-of-range frequencies `QC_BAD`.
2. **Global bounds**: temperature and salinity outside the limits are
   `QC_BAD` at any depth. A salinity failure not explained by temperature
   is blamed on conductivity.
3. **Spike tests** on temperature and conductivity look for single-point
   electrical noise. Each point is compared with the average of its two
   neighbours, normalised by their depth separation, against a shallow or
   deep limit. In the raw variables spikes are marked `QC_PROBABLY_BAD`.
   The same tests run again on the corrected copies, where spikes are
   marked `QC_INTERPOLATED` and filled in.
4. A bad temperature or conductivity point makes the matching salinity
   `QC_BAD`.

For a **GPCTD** or **legato**, the first raw pass runs the bounds tests
only, with no spike test. A GPCTD writes invalid values at the end of each
record, and the bounds test is what removes them.

There is **no gradient test**, and the limits are not adjusted for regional
climatology. Override them per deployment if needed.

| Test | Default | Parameter(s) |
|---|---|---|
| Temperature range | −2.5 to 43 °C | `QC_temp_min`, `QC_temp_max` |
| Salinity range | 19 to 45 PSU | `QC_salin_min`, `QC_salin_max` |
| Temperature spike | 0.05 °C/m shallow, 0.01 °C/m below 500 m | `QC_temp_spike_shallow`, `QC_temp_spike_deep`, `QC_temp_spike_depth` |
| Conductivity spike | 0.006 S/m per m shallow, 0.001 below 500 m | `QC_cond_spike_shallow`, `QC_cond_spike_deep`, `QC_cond_spike_depth` |
| Overall CTD | at most 30 % of points bad | `QC_overall_ctd_percentage` (0.3) |
| Overall speed | at most 20 % of speeds bad | `QC_overall_speed_percentage` (0.2) |
| What a failed test sets | bounds → `QC_BAD`, spikes → `QC_INTERPOLATED` | `QC_bound_action`, `QC_spike_action` |

!!! note "Fresh water"
    The 19 PSU lower limit reflects where a Seaglider can operate, but the
    CT can still sample a fresh surface cap from river runoff or heavy rain.
    Lower `QC_salin_min` for those missions, or that layer will be thrown
    away.

The raw values are never changed. All corrections are applied to **copies**
(`temperature`, `conductivity`, `salinity`), which get their own `_qc`
variables. In the corrected copies, `QC_BAD` points become NaN, and
`QC_INTERPOLATED` points are linearly interpolated between good neighbours.
If there aren't enough good neighbours, the point is left as it is and
marked `QC_PROBABLY_BAD`.

### Corrections applied to the copies

- **Thermistor lag.** Temperature is corrected for the thermistor's
  first-order response time.
- **Slow flow at apogee and trapped warm water.** From the start of the
  climb pump until the glider is flying again (moving at flight speed and
  rising at more than about 4 cm/s), there is little flow through an
  unpumped cell. Those points are marked `QC_BAD` in conductivity
  (`detect_slow_apogee_flow`, on by default except for the legato). This
  check only runs on gliders without a compressee, which is the normal
  Seaglider. The nose fairing can also carry warm surface water down and
  release it when the glider pitches up or stalls. That shows up as a fresh
  multi-point spike on a T-S diagram. The 2017 manual described flagging
  these temperatures automatically. Current code only **suggests**
  `bad_temperature` directives for such warm pulses on the dive, because
  flagging them automatically proved too aggressive.
- **VBD bleed at the start of the dive.** While the glider bleeds oil and
  starts to sink, flow through the cell is still building, so conductivity
  from the start of the bleed to the start of the dive is marked `QC_BAD`
  (`detect_vbd_bleed`, on by default except for the legato).
- **End of the climb.** Near the surface, where the glider is bobbing or
  bubbles may form, conductivity at the tail of the climb is marked
  `QC_BAD`. If the data stops well short of the surface, the dive is
  treated as truncated and the current is downgraded.
- **Stuck on the bottom.** If the glider didn't reach `$D_TGT` (or the
  altimeter bottom) and sat near its deepest point without moving, those
  points are left out of the current and displacement calculations. For an
  unpumped CT, their conductivity is marked `QC_BAD`.
- **Conductivity anomalies.** Bubbles near the surface and fouling or debris
  at depth make the cell read low, often over several points, which bounds
  and spike tests miss. The detector compares conductivity with what the
  temperature implies. Near-surface bubbles are marked `QC_BAD` (from the
  start of the dive to the deepest point where bubbles clear, and on the climb
  from where they start to the surface). Deeper anomalies produce
  **suggested directives** in the basestation output rather than automatic
  flags. As a rule of thumb, interpolate anomalies shorter than about 50 m and
  treat longer ones as bad. Anomalies that span more than one dive, or that
  start or end in a sharp thermocline, need manual attention.
- **Thermal inertia (salinity).** The conductivity cell's walls hold heat,
  so in a thermocline the water inside isn't at the measured temperature.
  For the **unpumped** CT sail the flow through the cell comes from the
  glider's own speed. The basestation therefore iterates between salinity →
  density → buoyancy → speed until speed and salinity are consistent.
  Points during rapid acceleration (flare, apogee, surface maneuver) are
  `QC_BAD` in conductivity. Stalled points are left out and can be
  interpolated. A heuristic suggests segments to interpolate and stable
  "anchor" points to trust. Both can be overridden.
- **GPCTD (pumped).** The pump gives a constant flow, so the
  thermal-inertia correction ignores vehicle speed and stalls. Points
  through the whole dive, apogee and climb are kept, and speed is computed
  once instead of iteratively. Anomaly detection still runs.
- **RBR legato.** The Sea-Bird thermal-inertia correction is never applied,
  even if requested. The legato gets its own corrections instead: a time
  lag, a thermal-mass correction and a pressure correction to conductivity
  (`legato_*` parameters). The VBD-bleed and slow-apogee checks are off by
  default.

The final corrected salinity is checked against the bounds again. The CTD as
a whole is trusted (`CTD_qc` good) only if more than **70 %** of the
corrected points are good. You can change that threshold with
`QC_overall_ctd_percentage`. Derived quantities (potential temperature,
density, sound speed) are computed from the corrected values.

Not checked at all: sensor drift over the deployment, density inversions,
turbulence, and anything **between** dives. Each profile is QC'd on its own.

### Speed and depth-averaged current

Two speed estimates are produced: a simple glide-slope model (`_gsm`
variables) from vertical speed and pitch, and the full hydrodynamic model
(`hdm`, the unsuffixed variables) from buoyancy and pitch. Speed is
**zero but `QC_GOOD`** during stalls. Speed is `QC_BAD`/NaN wherever
salinity is bad, because buoyancy can't be computed there. `hdm_qc` records
whether the speed/salinity iteration converged. The hdm speeds as a whole
are trusted only if at least 80 % of them are good.

The depth-averaged current (DAC) comes from the difference between the
flight-model dead-reckoned surfacing position and the actual GPS fix. It is
`QC_GOOD` only if the GPS fixes are trustworthy and the dive has data the
whole way. It is `QC_BAD` if a large part of the flight couldn't be modelled
(e.g. long stalls or time on the bottom). It is downgraded to
`QC_PROBABLY_BAD` when:

- the dive was truncated
- there was significant up- or down-welling: more than 10 % of points where
  the measured vertical speed differs from the model by more than 5 cm/s.
  This can also mean a poor flight model
- the glider loitered at the surface or at apogee for more than 10 % of the
  dive
- the expected error from GPS uncertainty exceeds the current itself

That GPS-based error estimate (`depth_avg_curr_error`) is a lower bound. It
assumes the flight model is right. Surface drift is computed separately
from GPS1 and GPS2. The current calculation isn't done for yo-yo dives (several
apogees without surfacing).

### Oxygen and optics

- **Oxygen** (SBE 43, Aanderaa optodes). Negative raw values are `QC_BAD`.
  Concentrations are recomputed with the **corrected** CT temperature and
  salinity. That's why a deck dive or a bad CTD leaves you with no corrected
  oxygen. Optode drift is corrected from the self-test in-air values when
  they're available.
- **WET Labs / ECO** channels are scaled with dark counts and scale factors
  when provided, but **no QC tests** are applied.

---

## The Flight Model System's part in QC

Everything above that depends on speed through water depends on the flight
model: the CT sail's thermal-inertia correction, the DAC, and the
dead-reckoned positions. The basestation's **Flight Model System** fits
lift/drag coefficients and a volume offset for every dive and uses those
values, not the `$HD_A/B/C` on the glider, for processing. The details are
in [Trim & Flight Model](../../piloting/seaglider/trim-and-flight-model.md#the-flight-model-system-fms).

Two QC consequences:

- **A wrong `mass` corrupts everything downstream.** FMS takes the mass from
  `sg_calib_constants.m` at dive 1. A large mismatch between dive and climb
  speeds is more often a mass error than a flight-model problem.
- **Bad conductivity corrupts the flight model.** Density feeds the buoyancy
  estimate. When something lodged in a CT cell partway through one mission,
  the step in conductivity showed up as a matching step in the `volmax` and
  `FM_vbdbias` plots. A sudden jump there can be the first sign of a CT
  problem.

---

## Manual QC: `sg_directives.txt`

When the automated result is wrong, the scientist corrects it with
one-line directives in `sg_directives.txt` in the mission directory.
`%` starts a comment. Each line is:

```
<dives> <function> [<location>]
```

where `<dives>` is a dive number (`149`), a range (`84:90`), or `*` for
all dives.

**Switches** (default in brackets; prefix `no_` to turn off):

| Directive | Effect |
|---|---|
| `skip_profile` [off] | Don't process the dive at all |
| `reviewed` [off] | Mark the dive as reviewed (comment who and when) |
| `detect_conductivity_anomalies` [on] | Run the anomaly detector |
| `correct_thermal_inertia_effects` [on] | Apply the thermal-inertia correction |
| `interp_suspect_thermal_inertia_salinities` [off] | Interpolate salinity where the correction is suspect |
| `interp_gc_temperatures` [off] | Interpolate temperatures during G&C actuator moves (for a glider showing warming whenever the actuators run) |
| `detect_vbd_bleed` [on; off for legato] | Mark conductivity bad during the dive-start bleed |
| `detect_slow_apogee_flow` [on; off for legato] | Mark conductivity bad while flow is slow at apogee. The QC manual calls it `detect_slow_apogee`, but the code uses `detect_slow_apogee_flow` |
| `bad_gps1` / `bad_gps2` / `bad_gps3` [off] | Don't trust that GPS fix. Pair a `bad_gps3` on one dive with `bad_gps1` on the next |

**Point flags** on the corrected values: `bad_temperature`,
`interp_temperature`, `bad_conductivity`, `interp_conductivity`,
`bad_salinity`, `interp_salinity`. Prefix any of them with `no_` to remove
points the automated QC flagged.

A location narrows the points affected. It can be `depth`, `dive_depth`,
`climb_depth`, `time`, `data_points` (CTD sample index from 1) or
`glider_data_points`, followed by `at`, `below`, `above`, `between`
(inclusive) or `in_between` (exclusive):

```
* bad_salinity depth below 10                    % every dive: drop salinity shallower than 10 m
346 interp_salinity data_points between 120 122  % dive 346 only
212 bad_gps2                                     % dive 212: GPS2 fix known to be wrong
```

When several directives target the same function, the included points are
combined first and the `no_` points removed afterwards, so **negation always
wins**. Order doesn't matter. All applied directives are saved in the `.nc`
file. A malformed dive number raises a `BAD_DIVE_SPEC` alert.

!!! tip "When the salinity/speed iteration won't converge"
    This typically happens when the glider is flying close to stall for
    much of the dive. Try `no_correct_thermal_inertia_effects` on that dive
    before resorting to `skip_profile`: you still get salinity and speeds,
    just without the iterated correction.

---

## QC settings in `sg_calib_constants.m`

Apart from the instrument calibrations, these are the values that most
affect QC:

| Group | Parameters |
|---|---|
| Vehicle | `mass` is the only one required. FMS estimates the rest (`volmax`, `hd_a`, `hd_b`, `vbdbias`). Hand-set `hd_*` values are ignored while FMS runs, with an `FM_IGNORE` alert |
| Biases | `pitchbias`, `depth_bias`, `vbdbias`, `temp_bias`, `cond_bias`, `GPS_position_error` |
| CT sail | `sbe_temp_freq_min`/`max`, `sbe_cond_freq_min`/`max`, frequency offsets, `sbe_cond_freq_C0`, `sbect_modes` (1, 3 or 5 modes for the thermal-inertia correction; default 1) |
| Pressure | `depth_slope_correction`, `smooth_truck_pressure` |
| QC thresholds | `QC_temp_*`, `QC_cond_spike_*`, `QC_salin_*`, `QC_overall_ctd_percentage`, `QC_overall_speed_percentage`, `QC_bound_action`, `QC_spike_action` |
| CTD type | `sg_ct_type` (e.g. `4` for a legato on a serial port), `legato_sealevel` |

---

## Reading the results

- **In the `.nc` file**, `*_raw` variables are the uncorrected values (Argo
  `TEMP`, `CNDC`, `PSAL`). The unsuffixed `temperature`, `conductivity` and
  `salinity` are the corrected ones (Argo `*_ADJUSTED`). Each has a `_qc`
  partner. Per-dive summaries: `CTD_qc`, `hdm_qc`, `depth_avg_curr_qc`,
  `surface_curr_qc`, `GPS1_qc`/`GPS2_qc`/`GPSE_qc`, plus `reviewed`,
  `directives` and `processing_history`.
- **In the basestation log**, QC lines say exactly what was flagged and why,
  e.g. "Changed (24/27) … to QC_BAD because raw … salinity below bound".
  Read these before assuming a sensor has failed.
- **The `time`, `latitude` and `longitude` variables** are estimated for every
  sample along the dive. The actual surfacing fixes are in the
  `log_gps_*` arrays.

---

## Pitfalls

- **Deck dives produce `QC_BAD` CTD data.** Only pressure is simulated, so a
  CTD in air fails the bounds. The result is no corrected CTD, no corrected
  oxygen and missing plots. Check the `.eng`/`.nc` files directly to confirm
  sensors are logging. See
  [Dive Cycle — deck dives](../../piloting/seaglider/dive-cycle-and-control-files.md).
- **Don't mix simulated and real dives in one mission directory.** It
  confuses vis and stops FMS from running (`FMS_DECK_DIVES` alert), which
  degrades the CTD corrections. Use `NewMission.py` (or `MoveData.py`
  afterwards), and move the `flight` directory along with the deck dives.
- **Get `mass` right before dive 1.** FMS uses the dive-1 value for its
  initial volmax estimate. If the mass turns out to be more than about 1 kg
  wrong and you change it mid-mission, restart FMS by renaming or deleting
  the mission's `flight` directory, then reprocess.
- **Don't rename the mission mid-mission.** It confuses the processing.
- **Downstream toolboxes may run their own QC.** Generic glider toolboxes
  sometimes apply QC set up for other platforms' variable names. Disable or
  adapt it, and pass the basestation's `_qc` variables on with the data.
- **Remember the limits.** The automated pass is real-time QC only. It doesn't
  look for drift or compare dives, so a slow biofouling trend or a
  calibration offset needs a delayed-mode review against bottle samples,
  ship CTD casts or climatology.

---

## See also

- [Trim & Flight Model](../../piloting/seaglider/trim-and-flight-model.md): FMS, mass and volmax, reprocessing
- [Sensor Configuration](../../glider-components/seaglider/sensors/index.md): getting sensors into the `.nc` files
- [Pressure Sensor](../../glider-components/seaglider/pressure-sensor/index.md): zeroing and depth errors
- [Compass Calibration](../../piloting/seaglider/compass-calibration.md): heading errors feed the DAC
- [Dive Cycle & Control Files](../../piloting/seaglider/dive-cycle-and-control-files.md): run phases, `$ERRORS`, deck dives
- [CTD Post-Processing](../shared/ctd-post-processing.md): checks and corrections beyond what the basestation does
- [Submitting to Data Centres](../shared/submitting-to-data-centres.md): the GliderDAC extension and uploads
