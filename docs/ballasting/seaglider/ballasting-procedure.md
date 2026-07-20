---
title: Seaglider Ballasting Procedure
description: Tank ballasting procedure for the Seaglider — weighing in air and in water, estimating volmax, and converting it into a lead adjustment before sea trial.
---

# Seaglider Ballasting Procedure

Before a sea trial, a Seaglider needs enough lead trimmed out (or in) that
its maximum internal volume (`volmax`) gives the right thrust in the density
of the water it's actually deploying into. This page covers the tank
procedure for estimating `volmax` and turning it into a weight change. Once
the glider is in the water, trim is refined dynamically from flight data —
see [Trim & Flight Model](../../piloting/seaglider/trim-and-flight-model.md).

!!! info "Source"
    Paraphrased from the APL-UW IOP office-hours session on ballasting and
    volmax estimation (June 2026) and the APL-UW IOP *SGX Documentation*.
    The tank method is deliberately simple — IOP's own philosophy is to
    nail down `volmax` in the tank and let the sea trial work out pitch/roll
    trim dynamically, rather than trying to model static centers precisely
    on paper. Numbers quoted here are IOP starting points — confirm against
    the [Parameter Reference Manual](https://iop-apl-uw.github.io/basestation3/html/Parameter_Reference_Manual.html)
    and defer to APL-UW IOP guidance.

---

## Equipment

- A freshwater tank large enough to fully submerge the glider **vertically**
  (deep enough that it can hang without touching bottom or breaking the
  surface).
- A hanging scale or load cell suspended over the tank, to weigh the glider
  in water.
- A line to suspend the glider from — tied off at the rudder, since it hangs
  vertically.
- The glider's comms cable, connected and slack — you need a live link to
  read/set VBD position while the glider hangs in the tank. Leave the
  antenna disconnected and simply let it dangle; nothing should be
  expressing at the surface.

---

## Procedure

1. **Weigh the whole glider dry** — wings, rudder, everything — on a scale
   in air. This is the mass **M**.
2. **Soak it overnight**, fully submerged and vertical, in the freshwater
   tank. This clears trapped air bubbles and fully saturates the fairings so
   the next day's in-water weight is real.
3. **Compute the tank water density.** In a freshwater tank, temperature
   alone gives you density; a saltwater tank also needs salinity.
4. **Weigh the glider in water** at an intermediate VBD position (e.g. 2000
   A/D counts) — this is **W<sub>i</sub>**. Hang it from the rudder by a
   light line with the comms cable attached and slack, nothing touching the
   tank bottom or breaking the surface.
5. **Compute `volmax`:**

    ```
    volmax = (M − Wi) / ρtank + ($VBD_MIN − VBDi) × VBD_CNV
    ```

    where `VBD_CNV = −0.2453 cc/AD count` (the old rule of thumb is roughly
    **4 A/D counts per cc**), `$VBD_MIN` (~400 counts) is bladder **full**,
    and `$VBD_MAX` (~3960 counts) is bladder **empty** — note the
    counter-intuitive naming: *smaller counts mean more volume*.

6. **Repeat at several VBD positions** — IOP uses five, e.g. 2000, 2250,
   2500, 2750, 3000 counts — and average. They should agree to within about
   ±5–10 cc; if one is a clear outlier, re-check that measurement before
   trusting the average.
7. **Convert to a weight change** using the **Ballast worksheet** in vis:
   feed it the tank `volmax`, plus your target thrust and target deployment
   density, and it returns how much lead to add or remove.

---

!!! warning "This estimate is not precise — plan around it"
    IOP's own tank estimate is only accurate to roughly **±100 cc**. Always
    deploy a glider that has only been tank-ballasted **on a line**, and
    prefer a shallow, enclosed, local first dive over an open-ocean or deep
    first mission — the tank number is a starting point for a sea trial, not
    a guarantee of neutral buoyancy in the field.

---

## After the tank: dynamic trim

The tank only gets `volmax` roughly right. Everything else — pitch trim,
roll trim, and refining `volmax` itself — is worked out **dynamically** from
the first dives, using the FMS regressions described on the
[Trim & Flight Model](../../piloting/seaglider/trim-and-flight-model.md#the-trimming-workflow)
page. Expect the physical process (cutting foam, moving lead) to take
several iterations before the glider floats the way you want, the same way
a Slocum typically needs [several tank opens](../slocum/ballasting-procedure.md)
before its ballast is right.
