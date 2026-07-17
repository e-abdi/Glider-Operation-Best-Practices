---
title: VBD
description: The Seaglider Variable Buoyancy Device — internal reservoir (bellofram), external bladder, boost and main pumps, and the Skinner valve; A/D counts, $C_VBD and the VBD budget; energy cost of pumping; and lab procedures for bleeding air and cycling the pumps.
---

# VBD (Variable Buoyancy Device)

The VBD is the Seaglider's buoyancy engine and the reason it moves at all: a
hydraulic system in the aft endcap that moves low-viscosity oil between an
**internal reservoir** inside the pressure hull and an **external bladder**
outside the hull (but inside the fairing). Pumping oil out increases the
glider's displaced volume without changing its mass — it gets lighter than the
water and climbs; bleeding oil back in shrinks it and it sinks. It is also the
single largest energy consumer on the vehicle, so most piloting-for-endurance
decisions are ultimately VBD decisions.

!!! info "Source"
    Paraphrased from the APL-UW IOP *SGX Documentation* (v1.0, 2024), the
    Kongsberg air-bleed procedure (support correspondence, 2018), the
    community "Cycletron in Pupa" pump-cycling notes, and IOP webinar/office
    hours material. Hardware details vary between SG, SGX, and Deepglider
    variants and build years — defer to APL-UW IOP and your glider's
    documentation.

---

## What's in the system

| Element | Role |
|---------|------|
| **Internal reservoir ("bellofram")** | A rolling-diaphragm oil reservoir inside the pressure hull; its piston position *is* the VBD position |
| **External bladder** | Holds the oil that increases displacement; sits outside the hull under the aft fairing |
| **Boost pump** | Low-pressure pump that feeds the main pump; runs only at depth, on the ascent side (older SGs used a *high*-pressure boost pump with different plumbing) |
| **Main pump** | High-pressure axial-piston pump that pushes oil out to the bladder against sea pressure |
| **Skinner valve** | Magnetically latching solenoid valve that meters oil (bleeds) from bladder back to reservoir |
| **Check valves (×3)** | 1–5 psi valves that fix flow direction and rate within the circuit |
| **Two linear potentiometers** | Report the reservoir piston position; the two readings can differ by up to a few hundred counts from piston wobble, so their **average** is used |

### Positions are A/D counts — and the names are backwards

Like pitch and roll, the VBD position is read on a 0–4095 A/D count scale, with
hardware limits found at assembly and tighter software limits inside them.
The conversion is `$VBD_CNV = −0.2453 cc per count` (same for SG and SGX) —
note the **negative** sign:

| | Hardware limit | Software limit | Volume vs. `$C_VBD` |
|---|---|---|---|
| Maximum volume (bladder full) | ~105 | ~370 = `$VBD_MIN` | +600 cc |
| Minimum volume (bladder empty) | ~4060 | ~3960 = `$VBD_MAX` | −260 cc |
| Neutral | | `$C_VBD` ≈ 2900 | 0 |

!!! warning "`$VBD_MIN` is the *full* bladder"
    Because of the negative conversion factor, **small A/D counts mean large
    volume**: `$VBD_MIN` (~370 counts) is maximum displacement and `$VBD_MAX`
    (~3960) is minimum. Every volmax and `$SM_CC` calculation trips over this
    at least once.

`$C_VBD` — the neutral position — is set for the **densest water of the
mission** (the deepest part of the dive), and is one of the first things
trimmed at sea: see [Trim & Flight Model](../../../piloting/seaglider/trim-and-flight-model.md).

## The VBD budget

A Seaglider has roughly **800–860 cc** of usable volume change, and a mission
spends it three ways:

| | |
|---|---:|
| Total VBD available | 800 cc |
| Positive buoyancy to expose the antenna at the surface | −150 cc |
| Negative thrust in the densest water | −250 cc |
| **Left over to compensate stratification** | **400 cc** |

The rule of thumb for what that remainder buys: about **70 cc per σ<sub>T</sub>
unit** of density change for SGX (~50 cc for SG), so the 400 cc above absorbs
≈5.5 σ<sub>T</sub> of stratification (SGX). If the mission's density range
exceeds that, something has to give — shallower dives or less thrust at
apogee. Driven flat out (−350 cc thrust, ~18 cm/s, full-range pumping every
dive) a Seaglider can stem ~40 cm/s of depth-averaged current, but burns
energy at roughly **ten times** the rate of a gentle mission where the VBD
stays within half its range.

## Energy: why the VBD dominates

Pumping at depth means pushing oil against full sea pressure — the pump
accounts for **about half the total energy budget** of a Seaglider. The
control scheme is built around this (no bleeding on descent, pumping only on
the climb where the oil must be moved anyway), and the pump itself is
optimized for efficiency near 1000 m — at shallow-water pressures it moves
only ~2 cc/s, which is part of why shallow missions are hard on Seagliders.
The most expensive single act is the big **surface-maneuver pump to
`$SM_CC`**; reducing `$SM_CC` (where safe) and avoiding unnecessary deep
pumping (`$W_ADJ_DBAND`, pitch-over-VBD) are the standard savings — see
[Trim & Flight Model](../../../piloting/seaglider/trim-and-flight-model.md).

---

## Lab: bleeding air out of the VBD

Air in the hydraulics makes VBD moves spongy and position readings
untrustworthy. The system is bled in three stages, pushing air along the path
**lines → bladder → reservoir → out**. The procedure below uses the glider's
own electronics (a *jog box* — a Kongsberg tool that drives the motors and
Skinner valve directly — makes it easier, but is optional). Setup: connect
main/boost motors and both potentiometer leads to the tailboard, tailboard to
mainboard (bench alongside the endcap is fine), bench supply at 10 V and 24 V,
comms cable on port A, power on, wand the glider on, and go to the `hw/vbd`
menu.

1. **Lines** — orient the endcap so the reservoir's "T" fitting (the pump
   supply line) is at the *bottom*: air in the reservoir floats away from the
   supply so the pump doesn't re-ingest it. Use the `ad` option to pump to a
   value ~200 counts *lower* than currently reported (pumping pushes any line
   air into the bladder). Confirm the lines look clear.
2. **Bladder** — reorient so the Skinner valve (silver cylinder with the blue
   coil pack) is at the *top* — it is the bleed port back to the reservoir.
   Shake/rattle the bladder gently to walk bubbles up to it. Use `open` to
   open the Skinner valve while squeezing the bladder by hand, driving air
   and oil back to the reservoir, then `close` **while still applying
   pressure**. Repeat a few times.
3. **Reservoir** — reorient with the Phillips **bleed screw** on top. Back the
   screw out *slowly, a couple of turns only* — the linear-potentiometer
   springs keep the reservoir pressurized, and trapped air is forced out.
   When oil (not air) starts to emerge, re-seat the screw fully.

!!! danger "Don't remove the bleed screw"
    The reservoir is under spring pressure. If the bleed screw comes out too
    far — or all the way — oil squirts out with no way to stop it except
    plugging the hole. A couple of turns is all it takes.

Repeat any stage as needed; one full pass removes virtually all the air.

## Lab: cycling the pumps ("cycletron")

Exercising the VBD through full-range cycles on the bench — main pump alone,
main + boost, and boost alone — verifies pump health and produces a logged
dataset (currents, rates) to compare against previous services. The community
procedure runs from the glider's `hw/vbd/pump` menu with a terminal log
capturing everything:

1. Start a terminal log (e.g. `sgXXX_cycle_main_only_YYYYMMDD`), wand on, and
   enter `hw/vbd/pump`.
2. Answer the prompts: specify **A/D counts** (not pressure); accept the
   software min; 5 s rest; accept the software max; 5 s rest; then the
   `D_BOOST` / "use boost to prime main" questions per the variant you are
   testing (both **N** for main-only; prime **Y** for main+boost).
3. Sample interval 1 s, display readings **Y**, **10 cycles**, 900 s pump
   time. Close the log when done.
4. For **boost-only**, first set `$D_BOOST,25` (saved to NVRAM) and re-zero
   the pressure sensor at sea level (`hw/pressure/sealevel`) so the glider
   believes it is deep enough to run the boost pump, then run the same cycle
   dialog answering **Y** to `D_BOOST`.

!!! note "If the cycle refuses to start"
    If the current VBD position sits slightly *above* the default software
    max, the cycle won't start — either enter the current position as the max,
    or first move the VBD by A/D counts to below the max.

The logged `HVBD` lines can be bookmarked (e.g. in Notepad++), extracted, and
pasted into a spreadsheet to trend pump rate and current draw over time.

---

## See also

- [Trim & Flight Model](../../../piloting/seaglider/trim-and-flight-model.md) —
  `$C_VBD` trimming, volmax estimation in the tank, and the FMS `vbdbias`
  estimates that track volume through a mission.
- [Dive Cycle & Control Files](../../../piloting/seaglider/dive-cycle-and-control-files.md) —
  where pumps and bleeds happen in the dive, and the parameters that bound them.
