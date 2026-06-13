---
title: Slocum Altimeter One-Pager
description: Quick-reference guide for testing and configuring the Slocum glider altimeter.
---

# Slocum Altimeter One-Pager

---

## Hardware

| Spec | Value |
|---|---|
| Frequency | 170 kHz |
| TVR | 156 dB |
| Max SPL | 204.3 dB |
| Beam pattern (−3 dB) | 18° |
| Operating interval | Every 4 seconds (downcast only) |

---

## Handling

!!! danger "Protect the nose."
    The altimeter is sensitive even when potted in urethane. Avoid putting pressure on the glider nose — altimeters can be damaged if the glider is dragged or dropped on a lab floor or boat deck during ballasting or deployment.

---

## Installation

!!! tip "Connector lubrication"
    When mating the altimeter to the glider nose, spray both male and female connectors with **3M silicone spray** (3M I.D. 62-8703-1398-7).

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

**Altimeter min depth (`u_alt_min_depth`)**

- In deep water, set >100 m to avoid false returns from the surface or thermocline.
- If the bottom will always be deeper than the glider's operational dive depth, consider disabling the altimeter entirely to save energy.

**Reduced usage mode (`u_alt_reduced_usage_mode`)**

- Default: **ON** (`1`). After a good hit, the glider calculates the halfway point to the bottom and powers the altimeter off until then — saving energy.
- Disable with `put u_alt_reduced_usage_mode 0` when operating in areas with unknown or highly variable depth. Note: this increases energy use.

**Water depth lifetime (`u_max_water_depth_lifetime`)**

- Sets how many yos the glider will use the last known `m_water_depth` when no new altimeter fix is acquired.
- If set to `1` and a false hit is recorded, the next dive will turn around at the false depth — but by dive 3 the value is discarded and normal dive behaviour resumes.

---

## Relevant Sensors

| Sensor | Units | Description |
|---|---|---|
| `m_altitude` | m | Height above the bottom |
| `m_raw_altitude` | m | Height above bottom, unfiltered |
| `m_raw_altitude_rejected` | bool | True if the altimeter did not supply a reading |
| `m_water_depth` | m | `m_depth` + `m_altitude` |
| `c_alt_time` | sec | Time between altimeter pings (`0` = as fast as possible, `<0` = off) |
| `u_alt_min_depth` | m | How deep the vehicle must be before the altimeter turns on. Increase to avoid thermocline reflections or save energy in deep water. |
| `u_alt_reqd_good_in_a_row` | nodim | How many `m_raw_altitude` readings are averaged to produce `m_altitude` |
| `u_alt_filter_enabled` | bool | Enable median filter for altitude |
| `u_alt_reduced_usage_mode` | bool | Glider powers altimeter only when needed. Saves energy; may underperform in shallow water. |
| `u_max_water_depth_lifetime` | yos | How many yos to use last known `m_water_depth` in the absence of new altimeter fixes |
| `u_alt_min_post_inflection_time` | sec | Seconds after inflection before altimeter data is accepted |
| `u_sound_speed` | m/s | Nominal sound speed used to scale altitude output. Default 1500 m/s. |
