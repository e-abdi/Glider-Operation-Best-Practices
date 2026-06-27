---
title: Passive Acoustic Monitoring
description: Best practices for running passive acoustic monitoring (PAM) missions on Slocum gliders — common acoustic payloads (DMON, WISPR, VMT), integration realities, and how to fly the glider quietly to minimize self-noise from the buoyancy pump, altimeter, CTD, and fin.
---

# Passive Acoustic Monitoring (PAM)

This page collects field-tested practices for **flying a Slocum quietly** and for
the **mission design** PAM work needs. It is platform-focused on Slocum; some
underlying principles (reduce pump activity, silence the altimeter) apply to any
glider.

!!! info "Source"
    Paraphrased from the UG2 community Slack (which has a dedicated PAM channel)
    and the Teledyne Webb Research user forum. Reflects field experience from
    NOAA Fisheries, UVI, AMLR, Rutgers, WHOI, and others. This is a condensed community reference — it is
    **not** a manufacturer document. For sensor integration, work directly with
    Teledyne and your instrument vendor.

---







## Flying quietly: the self-noise budget

The biggest wins come from reducing the glider's own noise. In order of impact:

### 1. Buoyancy pump — the loudest thing on the glider

Every inflection runs the pump, which dominates the spectrogram (the piston shows
as bright broadband bars). To reduce it:

- **Minimize pump activity:** fewer, deeper, slower inflections; use the minimum
  buoyancy drive that still flies. The same levers as the
  [Power Saving page](power-saving.md) help here — quieter usually means lower
  power too.
- **Drift segments:** where the science allows, drift-at-depth (wide deadband)
  keeps the pump off for long quiet stretches.

### 2. Pitch control — prefer "set once" over constant servo

Constantly servoing the pitch battery makes noise. A common PAM approach:

- First let the glider **find trim** with **autoballast on servo** (optimal
  pitch and oil/ballast settings).
- Then switch to **`battpos` / "set once"** so the battery moves **once per
  half-yo** to reach the target and then holds — much quieter than continuous
  adjustment.

!!! warning "Set-once pitch can miss the target angle"
    Operators report set-once dives/climbs coming in **shallower than commanded**
    (e.g. ~18° when 26° was requested) while still reporting "autoballast
    achieved." Tune on a real dive: have servo+autoballast find the working
    pitch/oil values first, then commit them to a fixed battpos. A wider pitch
    deadband is the alternative if you stay on servo.

### 3. Altimeter — turn it off when you can

The Slocum altimeter pings at **~170 kHz**, but because the pulse is so sharp it
**smears across the whole spectrogram**; in person it sounds like continuous
quiet ticking. It is worst in **shallow water near the bottom**.

- **Turn the altimeter off** when you don't need it for flying (deep water, known
  bathymetry), or restrict it to the **dive only** (not the climb), and push
  `u_alt_min_depth` deep. See the
  [altimeter one-pager](../../glider-components/slocum/altimeter/guides/slocum-altimeter-one-pager.md).
- Keeping the altimeter off **also** helps the glider stay in low power mode (it's
  one of the things that blocks it).

### 4. Fin / rudder — reduce hunting (and roll)

Excess rudder movement and roll add noise. Reduce fin hunting with
`u_hd_fin_ap_deadband_reset 1` and wider heading deadbands (see the
[Fin / Digifin page](../../glider-components/slocum/digifin/index.md#reducing-rudder-noise-and-saving-power)).
Excess **roll** also makes noise and muddies the data — trim it out where you can.

### 5. Pinger / transponder — weigh noise vs. recovery risk

A pinger or transponder adds periodic pings to your recordings. Disabling it
cuts noise but removes an acoustic means of relocating a lost glider (and may
violate insurance requirements). Decide deliberately.

!!! note "Know your own acoustic signatures"
    For analysis, expect to see the **piston (pump)**, **altimeter pings**, and
    any **pinger** in your spectrograms. Documenting these self-noise signatures
    up front makes the biological signal much easier to pick out later.

---

## Mission design for PAM

- **Station-keeping near a mooring or slow feature:** running **yo's looping
  around a single waypoint** with a **tight waypoint distance** works well for
  holding near a PAM mooring. To follow a drifting feature (e.g. a float),
  run an **SFMC script** that issues new commanded waypoints based on expected
  drift speed and direction.
- **Sampling strategy:** consider **downcast-only** sampling and turning off
  instruments whose noise competes with PAM (notably a pumped CTD). Fewer active
  instruments also reduces the abort risk below.

!!! warning "The \"timed out waiting for science to stop logging\" abort"
    Complex PAM payloads push gliders toward the **~5-instrument** threshold
    where a long-standing bug surfaces: at the surface the glider can hang
    stopping/starting science logging and aborts with
    **`MS_ABORT_BEH_ERROR`** (`surface_x` behavior → B_ERROR). It dates to 7.x,
    was *mostly* fixed by **8.0**, and **reappeared on G3S** due to different CPU
    timing; newer **11.x** releases claim a fix. Field mitigations:
    - **Sequence the same mission 5–6 times** (and set waypoints to continue past
      the last achieved one) so an overnight abort just **resumes** the mission.
    - Add a **surface script** that puts the glider back on mission on this abort.
    - **Stagger sampling timing/states** for the most complex instrument first
      (the DMON or a DVL is often the culprit) — e.g. sample on the dive but stop
      a few metres below the surface on the climb.
    - Review **low power mode** interactions, and **report it to TWR** (more
      reports raise its priority).

---

## Quick checklist

- [ ] Recorder integrated and powered correctly (proglet / backseat / external logger); time sync confirmed
- [ ] Hydrophone port and mount rated for your depth (PETG/PC, 100% infill if printed)
- [ ] CTD silent (RBR) or turned off if its pump competes with PAM
- [ ] Buoyancy pump minimized: deep/slow inflections, minimum drive, drift where possible
- [ ] Pitch on fixed **battpos / set-once** after trimming on servo+autoballast
- [ ] Altimeter off (or dive-only, deep `u_alt_min_depth`) when bathymetry allows
- [ ] Fin hunting and roll reduced (`u_hd_fin_ap_deadband_reset 1`, wider heading deadbands)
- [ ] Pinger/transponder decision made (noise vs. recovery risk)
- [ ] Mission **sequenced** several times + surface re-launch script for `MS_ABORT_BEH_ERROR`
- [ ] Self-noise signatures (pump/altimeter/pinger) documented for the analysts
