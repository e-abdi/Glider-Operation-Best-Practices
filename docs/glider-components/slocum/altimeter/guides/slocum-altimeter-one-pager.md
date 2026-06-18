---
title: Slocum Altimeter One-Pager
description: Quick-reference guide for testing, configuring, and troubleshooting the Slocum glider altimeter, including analog vs. digital boards and false-hit mitigation.
---

# Slocum Altimeter One-Pager

!!! info "Source"
    Paraphrased and consolidated from the *Slocum G3 Glider Maintenance Manual*,
    the Teledyne Webb Research (TWR) user forum, and the UG2 community Slack.
    This is a condensed field reference — always defer to official Teledyne
    documentation and contact Glider Support before changing altimeter behaviour
    on a deployed vehicle.

---

## Hardware

| Spec | Value |
|---|---|
| Frequency | 170 kHz (same on G1, G2, and G3) |
| TVR | 156 dB |
| Max SPL | 204.3 dB (max PCB output ≈ 260 V rms) |
| Beam pattern (−3 dB) | 18° |
| Operating interval | Every 4 seconds (downcast only) |

The transducer is a **custom AIRMAR design built for Teledyne Webb** — it is not
a catalogue part you can source directly from AIRMAR. The externally mounted
transducer is the **same across board generations**; what changed over time is
the control board inside the forward section (see below).

---

## Handling

!!! danger "Protect the nose."
    The altimeter is sensitive even when potted in urethane. Avoid putting pressure on the glider nose — altimeters can be damaged if the glider is dragged or dropped on a lab floor or boat deck during ballasting or deployment.

---

## Installation

!!! tip "Connector lubrication"
    When mating the altimeter to the glider nose, spray both male and female connectors with **3M silicone spray** (3M I.D. 62-8703-1398-7).

If an altimeter reads nothing at all, suspect the wiring before the sensor:
remove the nose cone and confirm the altimeter wire harnesses are **fully
seated**, then re-run the Functional Checkout procedure.

---

## Analog vs. digital control board (`altimeter` vs `altimeter_232`)

Two control boards exist, and **knowing which one your glider has is essential** —
the wrong device name in `autoexec.mi` is a common reason an altimeter "doesn't
work."

| Board | Device name in `autoexec.mi` | Notes |
|---|---|---|
| Analog (AD) board | `altimeter` | Original board |
| Digital RS-232 board | `altimeter_232` | Newer board on some G3S gliders |

- The two boards are **not interchangeable by name**: if the device listed in
  `autoexec.mi` doesn't match the installed board, the glider may not recognise
  the altimeter or will fail to find the bottom. (A real case: a glider that
  couldn't find bottom was listed as `altimeter_232` but actually had the analog
  board — switching the device to `altimeter` fixed it.)
- The switchover happened around certain serial numbers but is **not strictly
  chronological** — some later gliders shipped with the analog board, so verify
  per vehicle with the `use` command rather than assuming by age.
- The **digital `altimeter_232` board is not compatible with older Persistor
  processors** (e.g. OS 8.5). A nose-section swap between a Persistor glider and
  a newer-processor glider requires changing the control board, which involves
  de-soldering/re-soldering (doable and reversible, but take lots of photos).
- Newer `altimeter_232` units often need **more tuning** to get consistent
  bottom detection and inflections at the target altitude.
- TWR publishes a *Slocum Glider RS-232 Altimeter Guide* describing the digital
  board — request it from Glider Support if you operate `altimeter_232` vehicles.

---

## How to Test

**In the lab:**

1. Remove the sonar dome.
2. Type `put c_alt_time 0` to set the altimeter to update as fast as possible.
3. Type `report ++ m_altimeter_voltage m_raw_altitude`.
4. Place your ear against the face of the altimeter — listen for a faint, regular tick no louder than a watch.
5. Type `report clearall`.

!!! note "m_altimeter_voltage = 2.5V"
    This means the altimeter is not seeing an echo within its 100 m range. Try tapping the transducer face with a finger to simulate an echo.

---

## Key Settings

!!! note "`c_alt_time` is not user-settable"
    Despite earlier belief that it could be set when reduced-usage mode is off,
    TWR confirmed `c_alt_time` is **glider-controlled in all modes**. Use it as a
    test knob (`0` = ping as fast as possible) but don't rely on setting a fixed
    ping interval in a mission.

**Valid reading window (`u_min_altimeter` / `u_max_altimeter`)**

- A `m_raw_altitude` reading is only accepted if it falls **between these two
  values (inclusive)**; anything outside is rejected.
- On G3S gliders the autoexec defaults are typically **`u_min_altimeter` 2 m**
  and **`u_max_altimeter` 200 m**. Adjust to suit your terrain (see false-hit
  mitigation below).

**Altimeter min depth (`u_alt_min_depth`)**

- In deep water, set >100 m to avoid false returns from the surface or thermocline.
- If the bottom will always be deeper than the glider's operational dive depth, consider disabling the altimeter entirely to save energy.
- The altimeter will **kick the glider out of low-power mode**. In stable-depth
  water, raise `u_alt_min_depth` so the glider spends more time in low-power mode.

**Reduced usage mode (`u_alt_reduced_usage_mode`)**

- Default: **ON** (`1`). After a good hit, the glider calculates the halfway point to the bottom and powers the altimeter off until then — saving energy.
- Disable with `put u_alt_reduced_usage_mode 0` when operating in areas with unknown or highly variable depth. Note: this increases energy use.

**Water depth lifetime (`u_max_water_depth_lifetime`)**

- Sets how long the glider keeps using the last known `m_water_depth` when no new altimeter fix is acquired. In newer firmware: if `m_water_depth` is not updated within `u_max_water_depth_lifetime × m_avg_yo_time` seconds, it is set to `-1` (marked unusable).
- If set to `1` and a false hit is recorded, the next dive will turn around at the false depth — but by dive 3 the value is discarded and normal dive behaviour resumes.

---

## Reducing false bottom hits

Premature inflections from **false returns** — off the thermocline, scattering
layers, or zooplankton — are a common operational problem, especially over
complex bathymetry. (False returns are often worse in daylight, when zooplankton
are concentrated, and improve at night as the layer disperses.)

!!! warning "Firmware 11.00 changed altimeter handling"
    Some gliders that performed well on v10.08 began reflecting off false layers
    far too often after upgrading to v11.00 — suspected sub-par boards/components
    on a range of serial numbers. If you see frequent false inflections after a
    firmware upgrade, report it to TWR.

Mitigations operators have used:

- **Increase `u_alt_reqd_good_in_a_row`** — how many good readings in a row are
  required before the glider acts. Default is `3`; operators have raised it to
  `10` or even `25` to suppress false layers.
- **Raise `u_min_altimeter`** (e.g. to ~20 m) so intermediate scattering layers
  close to the vehicle don't trigger a turn.
- **Lower `u_max_altimeter`** — in one case dropping the max range from `100` to
  `65` eliminated periodic full-range false hits late in a long mission, behaving
  as if the detection threshold had drifted with sensitivity.
- **Median filter** (`u_alt_filter_enabled 1`) helps smooth noisy readings.

!!! note "There is no user gain/sensitivity adjustment on the Slocum altimeter"
    A recurring question — the Slocum altimeter's **gain/sensitivity cannot be
    tuned by the operator**. The levers above (valid window, good-in-a-row,
    min depth) are the practical way to manage false hits.

!!! tip "Raw vs. acted-upon values"
    `m_raw_altitude` is **not** what the glider flies on. Firmware filtering and
    logic convert raw readings into `m_altitude`, and only `m_altitude` (after
    `u_alt_reqd_good_in_a_row` good fixes) drives inflection. Use the raw values
    for diagnosis, not for predicting flight behaviour.

---

## `m_altimeter_status` codes

`m_altimeter_status` reports why a reading was or wasn't used:

| Value | Meaning |
|---|---|
| 0 | Good — altimeter reading is valid |
| 1 | Buoyancy pump is moving |
| 2 | Not diving |
| 3 | Inflecting now |
| 4 | Within `u_alt_min_post_inflection_time` of inflection |
| 5 | Too shallow — depth above `u_alt_min_depth` |
| 6 | Short reading — below `u_min_altimeter` |
| 7 | Long reading — above `u_max_altimeter` |
| 8 | Resulting water depth below `u_min_water_depth` |
| 9 | Resulting water depth above `u_max_water_depth` |
| 10 | Bottom changed too fast (vs. `u_max_bottom_slope`) |
| 11 | Water-depth problem, reason unknown |
| 12 | Not enough good readings in a row yet |

---

## Acoustic signature (for passive-acoustic users)

For passive-acoustic monitoring, the Slocum altimeter pings at **170 kHz on the
downcast only**, roughly every 4 seconds. Because the pulse is very sharp, it
**smears across the full spectrum** of a spectrogram rather than appearing only
at 170 kHz, and the contamination is worse the closer the glider is to the
bottom. (For contrast, a Seaglider altimeter pings near 12 kHz.)

---

## Relevant Sensors

| Sensor | Units | Description |
|---|---|---|
| `m_altitude` | m | Height above the bottom |
| `m_raw_altitude` | m | Height above bottom, unfiltered |
| `m_raw_altitude_rejected` | bool | True if the altimeter did not supply a reading |
| `m_altimeter_voltage` | volts | Voltage read from the A/D (2.5 V = no echo in range) |
| `m_altimeter_status` | enum | Why the reading was/wasn't used (see table above) |
| `m_water_depth` | m | `m_depth` + `m_altitude` |
| `c_alt_time` | sec | Time between pings (`0` = as fast as possible, `<0` = off). Glider-controlled. |
| `f_altimeter_model` | enum | Installed altimeter: `0` Benthos, `1` AirMar, `-1` experimental |
| `u_alt_min_depth` | m | How deep the vehicle must be before the altimeter turns on. Increase to avoid thermocline reflections or save energy in deep water. |
| `u_min_altimeter` | m | Minimum valid reading; below this is rejected |
| `u_max_altimeter` | m | Maximum valid reading; above this is rejected |
| `u_alt_reqd_good_in_a_row` | nodim | Good readings required in a row before acting; raise to suppress false hits |
| `u_alt_filter_enabled` | bool | Enable median filter for altitude |
| `u_alt_reduced_usage_mode` | bool | Glider powers altimeter only when needed. Saves energy; may underperform in shallow water. |
| `u_max_water_depth_lifetime` | yos | How long to use last known `m_water_depth` without a new fix |
| `u_alt_min_post_inflection_time` | sec | Seconds after inflection before altimeter data is accepted |
| `u_sound_speed` | m/s | Nominal sound speed used to scale altitude output. Default 1500 m/s. |
| `u_exp_alt_correction` | m | Fixed offset added to `m_raw_altitude` (experimental model only) |
