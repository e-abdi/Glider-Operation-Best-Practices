---
title: CTD Post-Processing
description: Turning glider CTD temperature, conductivity and pressure into trustworthy salinity and density on any glider — pumped vs unpumped CTDs, units, pressure and depth, sensor timing and alignment, thermal lag correction and how to judge it, dive/climb comparisons, checks against reference data, TEOS-10 quantities, and documenting what you did.
---

# CTD Post-Processing

Temperature, conductivity and pressure are the core of almost every glider
dataset, and salinity and density are only as good as the processing
behind them. This page covers the steps that apply on any glider. The
platform pages say what is already done for you:

- On a **Seaglider**, the basestation applies most corrections to every
  dive automatically ([Seaglider Data Quality Control](../seaglider/data-qc.md)).
- On a **Slocum**, nothing is applied; you start from raw values
  ([Slocum Data Processing & QC](../slocum/data-processing-qc.md)).

!!! info "Source"
    Paraphrased from the UG2 Slack #data channel (thermal lag, units, depth
    and density threads, 2024–2026), the basestation3 code and QC manual,
    Garau et al. (2011), the SOCIB glider toolbox paper (Troupin et al.,
    2016), TEOS-10 documentation, and operator correspondence. Correction
    methods and their parameters depend on the sensor; check the
    manufacturer's notes for yours.

---

## Know your CTD

| | Pumped (e.g. Sea-Bird GPCTD on Slocum) | Unpumped (e.g. Seaglider CT sail) |
|---|---|---|
| Flow through the cell | Constant, set by the pump | Set by the glider's speed; near zero at stalls and apogee |
| Thermal lag correction | Fixed flow, simpler | Needs the glider's speed through the water |
| Typical trouble | Pump failure, blocked cell | Low flow at apogee and surface, bubbles |

Fast-response CTDs from other makers (for example RBR) have their own
corrections; use the manufacturer's method rather than a Sea-Bird one.

---

## 1. Get units and pressure right

- **Conductivity.** Many glider CTDs log S/m. The TEOS-10 routine
  `gsw_SP_from_C` expects **mS/cm**: multiply S/m by 10. Getting this wrong
  gives salinities of about 3 instead of 35, or values that are wrong in
  less obvious ways after other processing. Check the numbers: seawater
  conductivity is about 3–6 S/m, or 30–60 mS/cm.
- **Pressure.** Some gliders log pressure in **bar** (Slocum
  `sci_water_pressure`); TEOS-10 wants **dbar** (×10). 1 dbar is roughly
  1 m of depth, but not exactly.
- **Depth.** Compute it from pressure and latitude (`gsw.z_from_p`), and use
  the **CTD's own pressure** for science, not the glider's flight pressure
  sensor. The two sit in different places on the hull: with pitch they
  differ by up to about a metre, and they may run on different clocks.

!!! tip "When the two pressure sensors disagree more and more with depth"
    A difference that grows with depth and shrinks again on the climb is a
    sensor problem, not geometry or clock drift. Something stuck in or over
    a pressure port (silicone grease has done it), a sensor out of
    calibration, or a wrong calibration for the flight sensor are the usual
    causes. Comparing the two **pressures** (corrected for pitch, roll and
    sensor positions) over a whole mission is a good way to calibrate the
    flight sensor against the CTD. One team found the corrected comparison
    stable over years.

---

## 2. Align the sensors in time

- **Use the CTD's own timestamp** where there is one, not the time the
  logging computer woke up. On a Slocum, for example, the CTD timestamp
  variable records when the reading was taken; the science computer's time
  only records when it was logged. The difference matters for time
  derivatives (dT/dt, dP/dt) in the thermal lag correction.
- **Check for dropped samples.** If the CTD samples faster than the logging
  computer reads it, some samples are never recorded.
- **Response times.** The thermistor, conductivity cell and pressure sensor
  respond at different speeds. A first-order lag correction to temperature,
  or a time shift between temperature and conductivity, is often the first
  step. For pumped CTDs the manufacturer usually gives a timing offset to
  start from.

---

## 3. Correct thermal lag

The conductivity cell's walls store heat. In a sharp thermocline the water
inside the cell is not at the temperature the thermistor reports, so
salinity is biased: in opposite directions on dives and climbs. Before
correction, the pycnocline commonly sits 0.5–2 m (sometimes about 3 m)
apart between a dive and the following climb.

**The standard method** (Garau et al., 2011, building on Lueck and Picklo,
and Morison et al.):

- Treat temperature and salinity as a fingerprint of a water parcel, which
  should look the same on the dive and the climb.
- Find the correction parameters that **minimise the area between the dive
  and climb T–S (or T–depth) curves**.
- Apply the correction to the **temperature used to compute salinity**, not
  to the measured temperature itself. The thermistor's own thermal mass is
  small; it only matters in extreme gradients (around 10 °C/m or more).

Points to watch:

- The curves cross themselves, so the usual polygon-area formula fails;
  use a method that handles self-crossing polygons.
- The method was developed for unpumped CTDs, where the correction depends
  on flow speed. For a pumped CTD the flow is nearly constant.
- Fits can be per profile pair, per segment or per deployment. Per-pair
  fits react to internal waves; per-deployment fits are more stable.
- Implementations exist in the SOCIB glider toolbox (MATLAB), GliderTools
  (Python), several open-source Python ports, and the Seaglider basestation
  (which iterates between salinity, buoyancy and speed for its unpumped
  CT).

### Judging whether the correction worked

Internal waves move the pycnocline between profiles (1–3 m was typical in
one coastal area), so no correction makes every dive/climb pair match.
Judge it statistically:

1. Compute the pycnocline depth difference for every dive/climb **and**
   climb/dive pair.
2. At a fixed location the true mean difference is zero.
3. The error of the mean tells you how good the correction is. On a long
   virtual mooring (two months or more), a good correction left a mean
   within about ±0.2–0.3 m.

Transects show more spread because the glider isn't sampling the same
water twice. Trying to improve a sub-metre offset beyond this at typical
glider sampling rates is usually not worth the effort.

Even with the same glider in the same area, re-check the constants each
deployment; they can drift. Deciding whether corrected data is actually
better takes an experienced eye.

---

## 4. Look for sensor problems

Corrections can't fix a sensor that isn't measuring properly. Look at
raw conductivity, especially around inflections and at the surface:

- **Growing dive/climb salinity differences mid-mission** usually mean
  something in the cell (biology, debris) or a failing pump, not a
  processing problem. It sometimes clears by itself.
- **Low conductivity near the surface** points to bubbles.
- **Low conductivity over several points at depth** points to fouling or
  debris; spike tests often miss it.
- **Density inversions through a whole water column for days** are not
  real. The ocean has short-lived inversions, not persistent ones. Suspect
  conductivity units or a broken sensor.

Flag questionable data rather than deleting it, and keep the raw values in
the file.

---

## 5. Check against reference data

- **Before deployment**: a tank or dock comparison with a calibrated
  instrument (for example a moored CTD logger in the same tank). Plan this
  in advance: record the glider CTD over the same period, and note the
  times and how the glider was configured. Comparisons fail when no one
  logged the glider data during the reference period.
- **At deployment and recovery**: a ship CTD cast next to the glider is the
  best reference. A cast at a nearby station a few hours apart is still
  useful.
- **During the mission**: compare deep, stable water against climatology or
  previous deployments in the same area, and look for drift over time.
- **For quick sanity checks**: nearby moorings and buoys with surface
  temperature and salinity, and satellite products.

---

## 6. Compute derived quantities

Use **TEOS-10** (the `gsw` library in Python, MATLAB and other languages,
or a web calculator for spot checks):

| Quantity | From | Note |
|---|---|---|
| Practical salinity (SP) | C, T, p | What most data centres expect as "salinity" |
| Absolute salinity (SA) | SP, p, position | TEOS-10's salinity |
| Conservative temperature (CT) | SA, T, p | TEOS-10's temperature for heat content |
| In-situ density | SA, CT, p | CF `sea_water_density` |
| Potential density / sigma-theta | SA, CT, reference pressure 0 | CF `sea_water_potential_density` / `sea_water_sigma_theta` |

Always say which density you report, in both the `standard_name` and the
`long_name`. Data centres have received both under the same name, and the
difference (several kg/m³ at depth) can lead users to the wrong conclusion,
for example when using DAC density to ballast a glider.

---

## 7. Document it

Record, with the data:

- the CTD model, serial number and calibration date;
- every correction applied and its parameters;
- the reference data used and the offsets found;
- the processing software and its version.

This is what turns a corrected dataset into a delayed-mode product someone
else can trust.

---

## See also

- [Data Formats & Standards](formats-and-standards.md)
- [Seaglider Data Quality Control](../seaglider/data-qc.md)
- [Slocum Data Processing & QC](../slocum/data-processing-qc.md)
