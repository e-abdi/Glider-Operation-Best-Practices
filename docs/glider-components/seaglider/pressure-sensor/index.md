---
title: Pressure Sensor
description: The Seaglider external depth sensor (Kistler, older Paine) and the internal hull pressure sensor — $PRESSURE_SLOPE from the cal sheet, amplifier gain on Rev E, the sea-level zero and $PRESSURE_YINT, pegged or zero counts, cable and termination faults, and zeroing the internal pressure before pulling vacuum.
---

# Pressure Sensor

Seaglider knows its depth from one analog pressure sensor in the aft
section. It is a strain-gauge bridge: current builds use a **Kistler**
piezoresistive sensor, and older gliders a **Paine**. The main board amplifies
the bridge output and reads it with a 24-bit ADC. Two parameters turn the raw
A/D counts into pressure, and from that the depth. Almost everything the
glider does in a dive hangs on that number: apogee, flare, the surface
decision, `$D_TGT`, `$D_NO_BLEED`, the flight model. A pressure fault
therefore rarely shows up as "bad data". It shows up as a glider that dives,
climbs or aborts at the wrong time.

A second, unrelated sensor on the electronics measures the **internal** hull
pressure (plus humidity and temperature). It is covered at the
[end of this page](#internal-pressure-sensor).

!!! info "Source"
    Paraphrased from 2022–2024 correspondence between Seaglider operators,
    APL-UW IOP and service providers (Rev E upgrades, Kistler integration,
    a pressure-cable failure), a Kistler calibration certificate, the
    manufacturer's support correspondence (2022), and operator notes on the
    internal pressure sensor. Board revisions and factory configurations
    vary — defer to APL-UW IOP and your glider's documentation.

---

## From counts to depth

The glider computes gauge pressure as

    pressure (psig) = counts × $PRESSURE_SLOPE + $PRESSURE_YINT

and depth from pressure.

| Parameter | What it is | Where it comes from |
|---|---|---|
| `$PRESSURE_SLOPE` | psig per A/D count | The sensor's calibration sheet, the excitation voltage, the amplifier gain and the ADC resolution (below) |
| `$PRESSURE_YINT` | Offset in psig | The **sea-level zero** routine, run with the glider at atmospheric pressure |

The two are not independent: **the Y-intercept is only right once the slope
is right.** Set the slope first, then zero.

For a sense of scale, one Kistler sensor wired directly to a Rev E board ran
with a slope of about `1.09e-4` and a Y-intercept between about **−156 and
−167 psig**. The firmware flags a `$PRESSURE_YINT` outside **−200 to 0** as
out of the recommended range. Treat that warning as a sign that the slope,
gain or wiring is wrong. It is not something to "fix" by accepting the new
value.

### Computing the slope from the cal sheet

The manufacturer's trim spreadsheet computes the slope as:

    $PRESSURE_SLOPE = (sensitivity, psi per mV/V)
                      × (1 / excitation voltage)
                      × (1 / amplifier gain)
                      × (volts per A/D count)
                      × 1000

- **Sensitivity** — full-scale pressure divided by the span on the
  calibration sheet. A 0–1500 psi Kistler with a span of 9.94 mV/V gives
  about 151 psi per mV/V.
- **Excitation** — the bridge supply from the board (5 V).
- **Gain** — the *total* gain between the sensor and the ADC (see below).
- **Volts per count** — the ADC reference over its resolution, about
  1.49 × 10⁻⁷ V (2.5 V over 2²⁴ counts).

For that sensor at a gain of 41.16: 151 ÷ 5 ÷ 41.16 × 1.49e-7 × 1000 ≈
**1.093e-4**, which is what APL-UW supplied for it.

!!! tip "Get the cal sheet with the sensor"
    New and spare sensors have arrived without calibration data. Kistler can
    supply the certificate for a given serial number. Request it before you
    need the glider, not on the launch day.

## Amplifier gain on Rev E

On Rev E main boards the pressure amplifier gain is set in the
**supervisor** (`hw/super`), in steps from 1 to 128. That is only part of
the total gain. Some boards also carry **fixed hardware gain**:

- A glider whose pressure sensor goes through an **aux board**, or a Rev E
  main board built with the gain in hardware, typically has a fixed gain of
  about **41.16**. Set the supervisor gain to **1** and compute the slope
  with the hardware value.
- A sensor wired straight to a Rev E board with no hardware gain uses the
  supervisor gain alone.

Stacking the two is a known trap. In one launch, a new Kistler on a
factory-built Rev E board had the supervisor gain set to 32 on top of a
fixed hardware gain. The sea-level reading was pegged at the ADC maximum and
the glider reported itself at ~1467 m on the surface.

To find out which case you have, set the supervisor gain to 1 and repeat the
sea-level test. Counts that stay pegged mean a wiring or electrical fault.
Counts that become sensible mean the board has hardware gain. Confirm with a
one-point check using compressed air or a hand pump on the pressure port. A
technician can also look for the gain resistor on the underside of the
board.

### Paine sensors on Rev E

Rev E came after Seaglider moved to Kistler sensors, and **a Paine does not
work on a Rev E board out of the box**. The Rev E amplifier cannot swing all
the way to 0 V. The Kistler has a small positive output at zero pressure, so
this doesn't matter. The Paine outputs almost nothing at zero pressure, so the
ADC sees nothing until about **100 psi**. That leaves roughly **60 m of
dead band** at the shallow end, where the glider needs depth most. Trying
different supervisor gains on such a glider did not give readings that
agreed with a hand pump.

When a 10/24 V glider with a Paine is upgraded to Rev E, the practical fix
is to **fit a Kistler as part of the upgrade**. Hardware workarounds exist,
but they are board-level modifications to be done with APL-UW.

## Sea-level zero

The sea-level routine (`hw/pressure/sealevel` in the menus, also runnable
from `pdoscmds.bat`) samples the sensor at atmospheric pressure. It prints
the mean, RMS, min, max and peak-to-peak A/D counts, and proposes the
Y-intercept that would make the mean read zero.

A healthy result looks like this:

- counts well inside the ADC range (neither 0 nor 16,777,215),
- peak-to-peak noise of a few hundred to about a thousand counts, which is a
  few centimetres,
- a proposed Y-intercept inside the recommended range, and close to the
  last good value for that sensor.

At launch the glider runs a similar check ("20 samples mean depth … noise …
threshold"). On a healthy glider that shows a mean within a few tens of
centimetres of zero and noise of about 3 cm, against a 7 cm threshold.

!!! danger "The zero routine will happily zero garbage"
    The routine computes a Y-intercept from whatever it reads, and in some
    contexts (self-test, launch) the new value is **accepted
    automatically**. Two real examples:

    - With counts **pegged at maximum**, it proposed −2358 psig. The glider
      then read "0 m" while sitting at the surface with a dead depth
      channel.
    - With a disconnected sensor reading **zero counts**, it set the
      Y-intercept to essentially 0. Every later boot showed a perfect 0.00 m.

    Always look at the **A/D counts** before believing the metres. If the
    proposed Y-intercept is far from the last good value, stop and find out
    why.

After a **main board replacement**, the pressure calibration does not come
across on the SD card. Settings live in the board's non-volatile memory.
Re-enter `$PRESSURE_SLOPE` (from the old parameter dump or the trim sheet),
check the gain, then redo the sea-level zero.

## When depth goes wrong

| Symptom | Likely cause |
|---|---|
| Counts pegged at 16,777,215 at the surface | Too much total gain (supervisor gain on top of hardware gain), or a wiring or electrical fault |
| Counts at 0; "pressure sensor got zero", "10 consecutive bad pressure reads – sensor dead" | Sensor not connected, a broken conductor or a bad crimp |
| Depth fine on the bench and on the descent, then wild values on the climb or after apogee | Intermittent connection that moves with pitch or attitude — check the cable and connector |
| Readings that jump (e.g. between ~0 m and ~100 m) when the cable is touched | Poor joint or crimp in the sensor cable |
| Hand-pump readings that don't match the gauge, or no response in the first tens of metres | Wrong slope or gain, or a Paine on Rev E (dead band) |

**Case: a failed deployment.** After a refurbishment and a VBD swap, a glider behaved
normally in shallow trials but failed a deployment. It flew wrong dive and
climb patterns with bad pressure readings, and aborted after three dives. The
motor controller has its own ADC for pressure, and its records agreed with
the main board's bad values. That pointed away from the main ADC and toward
the sensor side. When the glider was opened:

- A conductor in the Kistler adapter cable had come loose. The solder
  joint between the cable shield and a 30 AWG wire had never bonded
  properly (dull, dirty solder).
- Another 30 AWG conductor had a poor crimp, and a pin had a retaining tab
  bent the wrong way.
- A main board had also been damaged while the glider was being opened
  and inspected.

After re-terminating every pin and adding heat-shrink strain relief where
the fine wires leave the shielded cable, the sensor read steadily at sea
level while the cable and connector were wiggled.

Lessons:

- **Run a self-test after every reassembly and read the pressure section
  critically.** In this case the fault was visible in a self-test weeks
  before the failed launch, but nobody caught it.
- The Kistler cable uses **30 AWG** conductors, which are fragile. APL-UW
  crimps them with pins designed for 30 AWG. The 0.1-inch MTA connectors on
  the main board are insulation-displacement types, so the wire goes in
  unstripped. Stripping the ends first makes an unreliable joint. Support
  the point where the fine wires leave the jacket.
- Wiggle-test the cable and connector while logging pressure before you
  close the hull.
- Disconnect the battery before unplugging or probing cables on the main
  board.

## Internal pressure sensor

The internal sensor (`hw/intpress`) reports hull pressure in **psia**, plus
relative humidity and temperature. It is how you set and monitor the hull
vacuum, and a slow rise during a mission is an early sign of a leak.

The usual sequence at close-up:

1. With the hull sealed but not yet evacuated, the reading should be
   atmospheric, about **14.5 psia**.
2. Pull the vacuum down to about **9–9.5 psia** (some teams stop at
   8.5–9).

New sensors rarely read exactly 14.5 psia at atmospheric. The refurbishment
procedure sets a nominal slope and then adjusts `$INT_PRESSURE_YINT` until
the unevacuated reading is 14.5 psia, **before** pulling vacuum. On one
Rev E glider the slope stored on the board was not the manual's value.
Keeping the stored slope and adjusting only the Y-intercept gave the right
result.

!!! note "A dropped digit is not a leak"
    One operator saw readings of about 9.1 psia with an occasional
    "near-zero" value while pulling vacuum. In the log, those values were
    printed with the **leading digit missing** (".12 psia" for 9.12). It
    was a display glitch, not a sensor or vacuum fault. Read the raw log
    before chasing a leak.

---

## See also

- [VBD](../vbds/index.md) — the other half of the pumping decision; apogee
  and surface pumps are triggered by depth.
- [Dive Cycle & Control Files](../../../piloting/seaglider/dive-cycle-and-control-files.md) —
  where `$D_TGT`, `$D_NO_BLEED` and the surface depth thresholds act on the
  pressure reading, and how to run menu commands from `pdoscmds.bat`.
- [Batteries](../batteries/index.md) — a main board that is shorted while
  diagnosing a sensor can also take a pack fuse with it.
