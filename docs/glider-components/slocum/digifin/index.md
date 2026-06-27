---
title: Fin / Digifin
description: What the Slocum G3 tail fin (digifin) is, how the steering subsystem works and is tested, m_digifin_status bits and leak detect, rudder replacement and field calibration, and field workarounds for a stuck, faulted, or noisy fin.
---

# Fin / Digifin

The **tail fin** is the Slocum's steering assembly — and on modern gliders it is
a self-contained, self-calibrating **digital fin ("digifin")**. The fin houses
far more than the rudder: it integrates the vehicle's **antennas** (Argos 401
MHz, Freewave 900 MHz, and the combined GPS 1575 MHz / Iridium 1626 MHz quad-
helix), the **recovery strobe**, the **rudder and its motor**, and a **leak
detect** circuit. The whole assembly is rugged enough to be used as a handle to
manipulate the glider.

!!! info "Source"
    Paraphrased from the *Slocum G3 Glider Operators Manual* (Rev. 1, "Fin" /
    "Tail Fin" and "Steering Subsystem"), the UG2 community Slack, and the
    Teledyne Webb Research user forum. This is
    a condensed field reference — always defer to the official Teledyne
    documentation and the **4095-FCP Functional Checkout Procedure** for your
    specific glider.

---

## What's in the fin

The G3 fin is built around a **titanium boom**, a **motor housing**, an antenna
feed-through, and a plate bolted to a **PEEK mast** with a barrel-nut fastener
system. The rudder rides on a **magnetic coupling** (an external magnet drives
an internal one — there is no shaft seal at the rudder), and the strobe is
integrated into the leading edge of the mast in the orange Noryl housing shared
with the GPS/Iridium antenna.

Four independent subsystems live in the fin and should each be tested (per the
FCP):

| Subsystem | What it is |
|---|---|
| **Communications** | Argos, Freewave, and GPS/Iridium antennas |
| **Steering** | Rudder, motor, and position feedback |
| **Strobe illumination** | Recovery strobe |
| **Leak detect** | Water-in-fin A/D circuit |

!!! danger "Do not loosen the four titanium boom screws"
    The four titanium socket-head cap screws at the base of the fin boom must
    **not** be loosened or removed without explicit instruction from TWR. Also:
    the loop at the aft end of the boom (beneath the rudder) is a **tie-off /
    boat-hook point only** — it is **not** a lifting point and must never be used
    to suspend the vehicle.

---

## Steering: how it works and how to test it

- **`c_fin`** is the commanded rudder angle; **`m_fin`** is the measured angle
  (both in radians). The autopilot drives `c_fin` to steer toward `c_heading`,
  and `m_heading` / `m_roll` report the result.
- **Sign convention:** positive fin deflects the rudder to **starboard**;
  negative deflects to **port**. With a properly ballasted glider, **positive
  fin → increasing heading**.
- **Range** is roughly **±25°** (about ±0.45 rad).

**Bench / FCP test** (from LabMode):

```text
wiggle on
report ++ m_fin c_fin      # verify c_fin drives m_fin, no warnings/oddities
                            # m_fin > 0 → rudder to starboard; m_fin < 0 → port
wiggle off
```

A normal rudder sweeps only ~5–10° either side of center and stops a few
millimetres short of the **rudder keeper** at the top of the fin.

!!! tip "Rinse the fin after every recovery"
    Rinse the tail fin with fresh water after deployment so salt crystals don't
    inhibit rudder motion on the next power-up — a very common cause of
    first-power-up stiffness.

---

## m_digifin_status — reading the fin's health

`m_digifin_status` is updated every glider cycle and is a **bitwise OR** of event
flags. **Information bits** (≤ 2^20) clear themselves when read or when the
condition clears; **error bits** (> 2^20) stay set until the device is taken out
of service.

| Bit | Value | Meaning |
|---|---|---|
| POWERED_ON | 1 | Expected |
| POSITION_CHANGED | 2 | Expected |
| FACTORYCAL / STARTUPCAL / DEMANDCAL / ACTIVECAL | 4 / 8 / 16 / 32 | Cal events (in response to commands; the glider does **not** calibrate in flight) |
| RECAPTURE_PERFORMED | 64 | Fin had a position error and tried to free itself — not good, not necessarily failure |
| LEAK_DETECTED | 128 | Water currently in the fin (sets the LEAKDETECT error bit) |
| LEAKDETECT_READING_CHANGED | 256 | Leak-detect voltage changed (not necessarily an error) |
| MOTORFAULT_REGISTERED | 512 | Motor currently stalled (powered but not moving) |
| **LEAKDETECT** | **1,048,576** | (error) There has been a leak in the fin |
| **MOTOR_FAULT** | **2,097,152** | (error) The fin motor has stalled |
| **BAD_CHECKSUM** | **4,194,304** | (error) Fin firmware is corrupted |

For example, `m_digifin_status = 2097216` = `2097152 + 64` → a stalled motor
that tried (and failed) to recapture its position, i.e. a hard-over, faulted fin.

---

## Leak detect

The fin's leak-detect A/D is read via **`m_digifin_leakdetect_reading`**:

- It holds near **1025** (the manual cites ~1025; in practice readings sit in
  the low 1000s) when dry. **Lower values mean water.**
- A reading **below 1018** is considered a leak and should be reported to
  `glidersupport@teledyne.com`. Release **7.20+** aborts on a digifin leak; on
  older firmware, add `m_digifin_leakdetect_reading` to your `config.srf` so it's
  reported. An abort requires **`digifin_leakdetect_count` = 5** consecutive
  indications (it won't trip on a single dip).
- Occasional **single out-of-range samples (~885)** appear in many datasets and
  are not believed to be a concern; **sustained** low readings across multiple
  CPU cycles are.

!!! warning "False digifin leaks from comms line noise (G3/G3S)"
    A frequent G3/G3S failure mode is a **false** digifin leak abort triggered
    by RF/line noise — classically ~300 s after surfacing, **while Iridium is
    connected**. Tell-tales: the abort occurs at the surface during a call, and
    `m_digifin_leakdetect_reading` only dips during comms. Mitigations operators
    report: **physically separate** the Freewave/Iridium cabling from the
    leak-detect and pressure lines, add **ferrite beads**, and (on Teledyne's
    advice) lower `f_digifin_leakdetect_threshold` to match the glider's
    background noise — values from **~980 to ~1015** are glider-specific. See the
    [Freewave page](../freewave/index.md#antenna-placement-and-rf-interference)
    for the shared interference notes.

---

## Maintenance and field calibration

### Replacing the rudder

The rudder is a field-serviceable item (a common breakage — tangled lines snap
them, so carry spares):

1. Remove the **two Phillips-head screws** securing the mast top to the mast.
2. Hold the rudder and lift the **mast top** away from the fin.
3. Lift the rudder off the **magnetic coupling**.
4. Fit a new rudder and reassemble in reverse.

Replacing the **internal moving assembly** (beyond the rudder/magnet) is not a
documented field operation — contact glider support.

### Field calibration (set/check center)

From GliderDOS, manually command the fin to a centered position, then:

```text
digifin wr 119 2     # disable start-up calibration
digifin rr 112       # read previous centered cal value
digifin rr 100       # read current fin position
digifin wr 112 <value>   # write the read-back position as the new center
```

---

## Field troubleshooting

A digifin that throws warnings or takes itself out of service mid-mission is one
of the more common at-sea problems. The general strategy is to **limit the
fin's range to what still works**, **relax the abort criteria**, and keep
navigating — then fix it on recovery.

| Symptom | Likely cause | Field response |
|---|---|---|
| Fin stiff / won't move on first power-up | Salt crystals; debris lodged at the rudder base | Rinse with fresh water; clear debris between the moving fin and drive shaft |
| Warnings / aborts but fin mostly works | Debris partially blocking travel | Widen the deadband (`f_fin_deadzone_width`, and/or set `x_fin_deadband` directly); limit range; try dives to dislodge |
| Rudder turns one way but not the other | **Set screw on the coupling backing out**, or debris on one side | Narrow `m_fin_safety_max` / `f_fin_safety_max` toward the working side; keep flying; inspect/retighten on recovery |
| Hard-over + motor stalled (`MOTOR_FAULT`) | Mechanical jam / motor fault | May need to dive with digifin **out of service**, drift/spiral, and recover |
| Spiraling, `c_fin`/`m_fin` slamming port↔starboard | **Biofouling** on rudder/seams disrupting flow; static roll | Slow/steepen the relevant leg; reduce drive; run a couple of dives with fin fixed at zero to check default behavior |
| Rudder over-rotates, hits keeper, goes out of service | Damaged/torn **rudder keeper** (e.g. recovery damage) | Internal-assembly issue; field magnet swap + cal may not fix — contact support |

**Useful commands / sensors for limping a fin home:**

```text
put f_fin_safety_max 0.437       # clamp the usable range to measured limits
setdevlimit digifin -1 -1 -1     # set the error count that aborts to "infinite"
put f_digifin_movement_retry_max -1   # retry forever, never warn on a stuck fin
```

!!! note "Reducing range still navigates"
    Operators routinely complete missions on a **reduced fin range** — clamping
    to ~0.2 rad (instead of the full ~0.45) lets many fins comply and still
    steer well enough to reach waypoints. One 78-day / 1,300 km mission finished
    on a reduced-range fin whose set screw had backed out.

!!! warning "Deadband changes only take effect on `use` / `exit reset`"
    Setting `f_fin_deadzone_width` does **not** update the working deadband
    (`x_fin_deadband`) until the digifin is taken out of and put back into
    service (`use - digifin` / `use + digifin`) or an `exit reset`. This bit
    pilots trying to reduce surface "out-of-deadband" rudder slap. As a
    workaround some set `x_fin_deadband` directly. (A related steering "hardover"
    bug was fixed as Mantis #1615 in release 7.14.)

---

## Reducing rudder noise (and saving power)

Excess fin movement wastes energy and generates acoustic noise. A WHOI/TWR
experiment found that keeping **`u_hd_fin_ap_deadband_reset = 1`** is important
for navigation — with it at 0, heading variability rose and the glider was blown
off course; at 1, navigation and speed-over-water were normal while rudder
activity dropped. Reported settings that cut fin movement while still navigating:

```text
put u_hd_fin_ap_deadband_reset 1
put u_heading_deadband 0.261        # ~15°
put u_heading_rate_deadband 0.0261
put u_hd_fin_ap_run_time 120
```

In **low power mode**, the fin autopilot uses separate gains
(`u_low_power_hd_fin_ap_gain` / `_igain` / `_dgain`); in strong currents the
low-power gains can be too gentle to hold heading even though the fin reaches its
commanded position. See the [Power Saving page](../../../piloting/slocum/power-saving.md)
for the low-power context.

!!! tip "Widening heading deadbands also saves power"
    Less fin hunting means less motor work. Reducing steering effort (wider
    heading/rate deadbands, fixed fin angle where practical) is one of the levers
    on the power-saving page for stretching a mission.
