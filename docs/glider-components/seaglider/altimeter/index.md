---
title: Altimeter
description: The Seaglider altimeter/transponder — when to use the altimeter vs. bathymaps, the one-ping and multi-ping (linear fit) bottom-detection modes, $ALTIM_* tuning parameters and the false-hit/missed-bottom heuristics, plus the AAE LF transponder/altimeter hardware.
---

# Altimeter

The Seaglider's altimeter is an acoustic bottom detector: it pings downward
during the dive so the glider can start its apogee maneuver a safe margin off
the seafloor instead of trusting `$D_TGT` or a bathymetry map. The same board
is also a **transponder/pinger**, usable with ship tracking systems for
relocation. Unlike a dedicated downward altimeter, though, it is effectively
**omnidirectional** — a fact that drives most of its quirks.

!!! info "Source"
    Paraphrased from the APL-UW IOP office-hours material ("How to properly
    use the altimeter", April 2026), the APL-UW *SGX Documentation*, and the
    Applied Acoustic Engineering *LF Transponder/Altimeter Board Set
    Operation Manual* (SPC-5414). Check parameter definitions against the
    [Parameter Reference Manual](https://iop-apl-uw.github.io/basestation3/html/Parameter_Reference_Manual.html)
    for your firmware.

---

## First question: do you actually need it?

IOP's advice starts a step earlier than configuration — the altimeter is not
always the right tool:

- It uses **power** that could go to science or endurance.
- **Bathymetry maps are often more consistent**: a good `bathymap` on the
  compact flash lets the glider choose dive depth without pinging at all, and
  `$D_OFFGRID` (the depth assumed when off the map) is another option.
- **False positives cost energy**: every phantom bottom means a short dive,
  and short dives spend proportionally more energy per distance.
- **Missed detections cost more**: a non-responding altimeter on an
  altimeter-dependent mission ends with the glider on the bottom.
- It is **omnidirectional** — the nearest big reflector *becomes* the range,
  whether that is the seabed, a wall, or the surface (see the
  `$ALTIM_PING_DEPTH` notes at [seaglider.pub/parms](https://seaglider.pub/parms)
  for how the surface return is ignored).

## Bottom-detection modes

### One ping per dive

Set `$ALTIM_BOTTOM_PING_RANGE` (with `$ALTIM_BOTTOM_TURN_MARGIN`): the glider
pings once, at the given range above the *presumed* apogee depth, and adjusts
the turn depth from that single measurement. Cheapest and simplest — fine
when the bathymetry is gentle and roughly known.

### Repeated pings with a linear fit

For real bottom-following, the glider pings continuously and fits a line to
the returns to decide whether the bottom is genuinely approaching:

| Parameter | Meaning |
|-----------|---------|
| `$ALTIM_PING_DEPTH` | Depth at which pinging starts |
| `$ALTIM_PING_DELTA` | Ping every this many metres of descent |
| `$ALTIM_PING_FIT` | Packed three-digit control of the fit (below) |

`$ALTIM_PING_FIT` packs three settings into its decimal digits:

- **Ones** — number of pings used in the fit (one every `$ALTIM_PING_DELTA` m).
- **Tens** — the R² threshold the fit must exceed (default 0.8).
- **Hundreds** — slope threshold: |fitted slope| must be greater than this
  value and less than its reciprocal.

A good starting value is **873**. The fit output appears in the `$PING` lines
of the GC table: `$PING, depth, x1, x2, m, rsq` — current depth, first and
most recent fitted bottom depths, fitted slope (**negative = bottom
approaching**), and fitted R². Current firmware has real limitations here —
notably no separate up/down control of the ping schedule.

## Tuning the detector

| Parameter | Range [default] | Effect |
|-----------|-----------------|--------|
| `$ALTIM_FREQUENCY` | 10–25 kHz [15] | Ping frequency; also the escape hatch when another acoustic source is interfering |
| `$ALTIM_SENSITIVITY` | 0–5 [1] | Envelope-detector threshold; 0 disables the envelope detector and triggers on *any* return at the right frequency |
| `$ALTIM_PULSE` | 1–9 ms [5] | Transmitted pulse width; a valid return must exceed the sensitivity voltage for a full pulse width |

The defaults are good. The field heuristics:

!!! tip "False hits vs. missed bottom"
    - **False altimeter hits** (phantom bottoms, short dives): alternately
      *increase* `$ALTIM_PULSE` and `$ALTIM_SENSITIVITY` one unit at a time.
    - **Unable to detect the bottom**: alternately *decrease* them,
      incrementally.

## The hardware

The board set is an Applied Acoustic Engineering **LF transponder / pinger /
altimeter** (SPC-5414 family), mounted with the transducer in the vehicle and
run from the glider's 24 V (transmit) and 10 V (receive) supplies. Points that
matter operationally:

- It **defaults to transponder mode** at power-up and quietly reverts to
  transponder mode after ~2 minutes without serial activity; the glider wakes
  it over a 9600-baud serial link when it wants altimetry.
- The receiver uses a variable-gain amplifier (compensating attenuation with
  range) feeding an envelope detector — this is what `$ALTIM_SENSITIVITY`
  and `$ALTIM_PULSE` are tuning.
- Maximum altimeter range is **500 m** (1000 m round trip, ~667 ms).
- As a transponder it supports well over a hundred channel combinations for
  Simrad HPR/ORE Trackpoint-class tracking systems — useful for relocating a
  glider from a ship.
- Never operate transponder or altimeter with the **transducer disconnected**.

For bench checks, the glider menu tree has an `altim` section (`ping` to fire
a test ping, `config` to upload configuration, `direct` for pass-through
serial comms with the board). Verify altimeter behavior on the first dives of
a mission before relying on it: watch the `$PING` records and the apogee
depths against known bathymetry.

## When it goes wrong at sea

Two abort/recovery codes tie back to this system: `BOTTOM_OBSTACLE_DETECTED`
(bottom or obstacle seen when the altimeter is in use for bottom detection)
and `SURFACE_OBSTACLE_DETECTED` (surface detection — relevant under ice).
Repeated short dives with plausible-looking `$PING` returns usually mean the
sensitivity/pulse combination is too eager — see the tuning heuristics above —
or that another acoustic instrument on board is stepping on
`$ALTIM_FREQUENCY`.

---

## See also

- [Dive Cycle & Control Files](../../../piloting/seaglider/dive-cycle-and-control-files.md) —
  where the apogee decision fits in the dive, and the bathymap file format.
- [Mission Planning](../../../mission-planning/index.md) — preparing
  bathymetry maps before deployment.
