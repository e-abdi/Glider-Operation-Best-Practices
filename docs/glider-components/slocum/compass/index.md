---
title: Compass / Attitude Sensor
description: The Slocum compass and attitude sensor (True North TNT Revolution / legacy TCM3, the attitude_rev device): what it measures, magnetic variation, when and how to calibrate it on shore with RevolutionTest, the in-situ at-sea calibration, the post-cal compass check, and field troubleshooting for heading errors and interference.
---

# Compass / Attitude Sensor

A precision navigation **compass and attitude sensor** continuously measures the
glider's **heading, pitch, and roll**. These are the inputs the glider uses to
**dead-reckon** its position underwater between GPS fixes, so a compass that is
off by a few degrees turns directly into navigation error — the glider thinks it
is flying one way while the water carries it another.

On modern G2/G3/G3S gliders the device is a **True North Technologies "TNT"
Revolution** attitude module, addressed in the flight code as the
**`attitude_rev`** device. Very early gliders (roughly serial numbers below ~200,
G1-era) instead carried a **PNI TCM3** compass with its own `tcm3 cal` routine.
This page focuses on the TNT/`attitude_rev` device that the vast majority of the
fleet uses.

!!! info "Source"
    Paraphrased from the *Slocum Glider Operators Manual* (Rev. 1, "Attitude
    Sensor") and the *Slocum G3 Glider Maintenance Manual* (Rev. A, "Calibrating
    the True North Compass"), `masterdata.txt`, the Teledyne Webb Research user
    forum, and the UG2 community Slack (including in-situ calibration user notes
    contributed by NorGliders). For the calibration software itself, refer to
    True North Technologies' *Revolution Compass User's Guide*. This is a
    condensed field reference — always defer to the official Teledyne
    documentation and the `readme.txt` shipped with the calibration tool for
    your specific glider.

---

## When to calibrate

The compass should read true within a few degrees in **the configuration you
will deploy in**. Recalibrate (or at least re-check) whenever that magnetic
environment changes or the readings drift:

- **New or swapped battery packs.** Battery packs — especially **aft alkaline
  packs**, which sit closest to the compass — carry residual magnetism that
  shifts the calibration. Teledyne has shipped alkaline sets that needed
  **degaussing** before they would calibrate. Pitch and nose packs sit far
  enough away to matter much less.
- **After adding, moving, or removing hardware** near the aft section (sensors,
  hydrophones, recovery hardware, anything ferrous).
- **Heading errors in the water** — the glider not tracking to waypoints, or the
  classic **spiral** signature (see [Symptoms of a bad
  calibration](#symptoms-of-a-bad-calibration)).
- **Moving to high magnetic latitudes** (Arctic, high-latitude deployments),
  where the horizontal field is weak and a cal done elsewhere may not hold (see
  [High-latitude operations](#high-latitude-operations)).
- As a routine **pre-deployment check** — Teledyne suggests a quick heading check
  before every deployment and recalibration as required.

!!! tip "Calibrate, then verify"
    A calibration is only as good as the **compass check** that follows it. Don't
    treat "the software applied new coefficients" as success — always spin the
    glider against a hand compass afterward and confirm the error is within
    tolerance for your battery chemistry. See [The compass
    check](#the-compass-check).

---

## What it measures

The attitude sensor publishes the glider's orientation. The headline sensors:

| Sensor | Units | Meaning |
|---|---|---|
| `m_heading` | rad | Measured heading. **Magnetic**, not true (see below). |
| `m_heading_deg` | deg | `m_heading` converted to degrees. |
| `m_pitch` | rad | Measured pitch; **> 0 is nose up**. |
| `m_pitch_deg` | deg | `m_pitch` in degrees. |
| `m_roll` | rad | Measured roll; **> 0 is port wing up**. |
| `m_roll_deg` | deg | `m_roll` in degrees. |
| `m_hdg_error` | rad | `m_heading − c_heading` (how far off the commanded heading the glider is). |
| `m_gps_mag_var` | rad | Magnetic variation (declination) read from the GPS at the surface. |
| `m_attitude_rev_mode` | nodim | Command state of the `attitude_rev` device. |
| `m_attitude_rev_measure_state` | nodim | What the device is doing with its output (streaming vs. sample mode). |

!!! note "Heading is magnetic, not true"
    `m_heading` is the **magnetic** heading. When you fly to a commanded heading
    with `c_heading`, that is also **magnetic**. The glider only converts to true
    heading when it works in **LMC** (local mission coordinates) for waypoint
    navigation, using the magnetic variation.

---

## Magnetic variation (declination)

The glider corrects between magnetic and true heading using **`m_gps_mag_var`**:

```
mag_heading = true_heading + mag_var
mag_var > 0  ==>  variation is West (like on Cape Cod)
```

- `m_gps_mag_var` is **read from the GPS receiver at the surface and published
  automatically** — for normal operations you do not set it yourself. A typical
  value might be, e.g., `−16.7°` without you ever touching it.
- The on-board **Garmin GPS carries a magnetic-variation lookup table in its
  own firmware.** That table is static: it is only as current as the GPS
  firmware. If the GPS firmware is years out of date, its declination values can
  be stale — a consideration for high-precision work and for regions where
  declination is changing fast.
- There is also a default `s_mag_var` in `masterdata` used before a GPS fix is
  available.

!!! warning "Arctic declination changes fast"
    Near the magnetic poles, magnetic variation changes quickly with position and
    over time, and published models (and the GPS lookup table) have had to be
    revised for the Arctic. At high latitude, declination error compounds with
    the weak-horizontal-field problem below.

---

## Standard (shore) calibration with RevolutionTest

The standard calibration is done on shore with the glider physically rotated
through 3-D space while the **TNT RevolutionTest** Windows application records
the magnetic field and computes new hard-iron/soft-iron coefficients, which it
stores **on the compass itself**.

!!! danger "Get away from magnetic interference"
    The compass is **very** susceptible to ferrous material and magnetic fields
    from electronics, vehicles, rebar, and buildings. Calibrate **outdoors, away
    from any of these**, suspended from a **non-ferrous** structure. A cal done in
    a steel-framed building or next to a metal cart can be worse than no cal at
    all. (Calibration *can* be done from the cart in a pinch — see the note on
    coverage below — but a clean hang is the gold standard.)

### Equipment

- The glider, hung so it can **spin, pitch, and roll** freely (a bridle under a
  non-ferrous hoist; some teams manage from the cart with extra strapping).
- A laptop running **TNT RevolutionTest** (`RevolutionTest.msi`).
- A **Freewave** modem programmed to your glider, plus power supply — most teams
  do the cal over Freewave so no cable tethers the hanging glider. (See the
  [Freewave](../freewave/index.md) page.)
- A serial terminal program (to issue the `talk` command and then release the
  port).

### Procedure

??? note "Step-by-step: shore calibration"
    1. Set up Freewave comms to the glider (CD light green) and escape the
       startup into the console.
    2. Drop to the device shell and start streaming attitude data:
       - G3 / G3S: `talk attitude`
       - G2: `exit pico` then `talk att`

       This streams the raw attitude data **and**, in TWR code from roughly the
       last several years, **closes the air-pump solenoid valve** to put the
       glider in the same magnetic state it is in while diving/climbing (see the
       solenoid note below).
    3. **Close / disconnect your serial terminal** so the COM port is free —
       RevolutionTest needs that same port.
    4. Start **RevolutionTest**. When prompted, choose the wireless/serial
       connection, the **same COM port**, and baud **9600** (the `attitude_rev`
       comms rate). Optionally open the compass display (top-left icon) just to
       confirm you are connected.
    5. *(Two-step / vertical reference — recommended.)* In **Tools →
       Capture Vertical Reference**, hold the glider **level and steady**, click
       **Start**, then **Use New**. This captures a vertical reference outside the
       worst of the vehicle's influence so the subsequent 2-D rotation can solve
       all three hard-iron components.
    6. **Tools → Calibrate Magnetics.** Set the number of samples to the
       **maximum (3000)** and click **Start/Begin**. After a ~20 s countdown the
       software begins acquiring samples.
    7. **Exercise the glider through every reachable orientation in 3-D** until
       it reaches ~3000 samples — flat spins through N-E-S-W, then repeated with
       the nose pitched up, pitched down, rolled to port, rolled to starboard,
       and combinations of those. The **bar graphs** show coverage; the goal is
       to fill in **all** the bins. The roll/`z` bins are the hardest to fill and
       need lots of rolling (the far ends fill only at extreme roll — even
       inverting the glider). Have someone call out the sample count so the people
       turning the glider can pace it. It stops on its own at ~2999.
    8. The screen switches to a **Results** page. The **New** column's
       **"Mag Total 3 sigma"** should be **lower than the Old** — aim for **< 1%**
       for a solid cal. Click **Use New / Apply** to write the coefficients to the
       compass.
    9. Close RevolutionTest, reopen your terminal, and confirm the glider is back
       at the console.

!!! tip "Take Iridium out of service during the cal"
    An Iridium call mid-calibration can inject a magnetic transient and corrupt
    the data. Many teams `use - iridium` (and avoid Freewave/Argos keying where
    possible) while running the cal. This is the same RF/electrical coupling
    family that causes false digifin leak detects — see [Fin /
    Digifin](../digifin/index.md).

!!! note "Why the solenoid matters"
    The air-pump solenoid is a strong, **switchable** magnetic source right in the
    glider. During diving and climbing it is **closed**, and `talk att`/`talk
    attitude` closes it so the cal is done in the flight state. If you later do a
    **compass check from GliderDOS** (`report ++ m_heading`) instead of from the
    `talk` state, the solenoid is **open** unless you **inflate the air bladder
    and wait for the air pump to shut off** — otherwise the check can read up to
    ~**12°** off versus the actual flight calibration.

---

## The compass check

After applying new coefficients, **verify** before you trust them:

1. Open the compass display in RevolutionTest (or `report ++ m_heading` from
   GliderLAB/GliderDOS — but if you do it that way, **inflate the air bladder
   first** so the solenoid is closed, as above).
2. Using a **hand compass**, sight the direction the glider is actually pointing
   and compare it to what the glider reports.
3. Take readings around the full circle — **every 30° (or 45° if short on
   time)** — and repeat at roughly **26° nose-up (climb) and 26° nose-down
   (dive)** pitch, since the error varies with pitch.
4. Record the glider-vs-hand-compass error at each point (a spreadsheet helps).
   The errors typically trace out a rough **sine wave** around the circle, often
   with one bearing (frequently west) worse than the rest.

**Target error by battery chemistry** (community rules of thumb):

| Battery chemistry | "Good" heading error |
|---|---|
| Lithium-ion (rechargeable) | < ~5° |
| Lithium primary | ~3–5° |
| Alkaline | < ~8–10° |

With the solenoid correctly closed (air bladder inflated), well-covered
calibrations have reached ~2–3° peak-to-peak precision and ~1.5° accuracy across
all headings on all chemistries. If the solenoid is **not** locked, 5–10°
peak-to-peak is more typical, most of it an uncorrected hard-iron offset.

---

## In-situ (at-sea) calibration

If the glider is already deployed — or headed somewhere remote where a clean
shore cal isn't possible — there is an **in-situ** calibration that runs entirely
from a mission, collecting cal data while the glider yos in the water. It uses
the factory **`attcal.mi`** mission (and a community-tuned **`attcal2.mi`**
variant) plus the **GliderCal.exe** desktop tool.

!!! warning "In-situ is a fallback, not a replacement"
    Teledyne's guidance: an in-situ cal is **not** a substitute for a proper
    shore calibration. It is genuinely valuable when you have no other option —
    notably **high-latitude deployments** where it has rescued badly behaving
    compasses — but results are mixed, and some gliders still fly with a
    significant heading offset afterward. Treat it as "better than nothing."

How it works, in outline:

- The mission puts the `attitude_rev` device into **CCD sample mode** via the
  `compass_cal` behavior and collects field data over a long surfacing window
  (the community `attcal2.mi` raises `when_secs` to ~7200 s, sets a longer
  `overtime` abort, deepens the yo to ~50 m, and **disables low-power settings**
  so they don't trigger a different abort). It needs **at least 300 lines** of
  data for GliderCal to compute an accurate offset.
- It generates a **`*.cal`** file on the glider. You **send that file off**
  (`send *.cal`), open it in **GliderCal.exe**, and **Calculate Results**; as with
  the shore cal, the new **Mag Total 3 sigma** should be much lower than the old.
- You apply the result with **`compass_cal set_offsets X Y Z`** (X/Y/Z offsets —
  **include negative signs!**), and confirm with **`compass_cal get_offsets`**.
  `compass_cal ?` lists the available sub-commands.

??? note "The attitude_rev-stays-offline / abort caveat"
    A known quirk: once the `compass_cal` behavior has put `attitude_rev` into CCD
    sample mode, **it stays there after the surfacing condition is met** and
    simply appears offline — which trips a **device abort**. The mission collects
    a valid `*.cal` file regardless, but the glider needs to be **`exit reset`**
    to bring `attitude_rev` back online (the `use` commands generally won't
    recover it). Plan for that abort: set the mission's `overtime` and
    `num_samples` so you know roughly when to be on console, turn off the
    GliderTerminal xml script, and have a `sensors.mi` ready to reload your flight
    settings (`c_dive_bpump`, `c_climb_bpump`, `u_alt_min_depth`, low-power
    sensors, …) after the reset. This same flow has been confirmed to work on
    **G3S** as well, despite the abort.

!!! example "Why it matters at high latitude — a field result"
    One Arctic G2 (software 8.4, ~69° N) was flying north on dives and south on
    climbs while trying to make headway south. An in-situ cal moved the offsets
    from `(−1676, 1720, 3207)` to `(1023, 1950, 117)` and dropped Mag Total 3
    sigma from **55.9% to 0.67%**, restoring normal flight. Operators in Baffin
    Bay have had less luck — at the most extreme latitudes even the in-situ cal
    can struggle.

---

## Avoiding and managing magnetic interference

- **Degauss suspect battery packs.** A magnetized aft pack can make a clean
  calibration impossible and can throw the compass off in the water. Teams
  degauss aft alkaline packs (CRT/tape degaussers, bulk degaussers) — pass the
  pack slowly over the degausser, starting and ending well clear of it. You can
  gauge magnetization before and after by running a **hand/hiking compass** along
  the pack and watching the needle deflect.
- **Soften the attitude warning levels** if the compass keeps going out of
  service. The factory `attitude_rev` warning thresholds were found to be overly
  stringent; **Glider Service Bulletin 011** reduces them so the compass drops
  out of service (and aborts the mission) far less often near magnetic fields.
  Make sure that bulletin's settings have been applied — an unusually high rate
  of `attitude_rev` errors often means they haven't.
- **The compass goes out of service near strong fields by design** — steel
  buildings, electronics, high-iron ground. That is expected on the bench; it is
  a problem when it persists in the water.

!!! note "attitude_rev errors and aborts"
    When the compass cannot produce a heading, the glider raises
    `attitude_rev` device errors and can ultimately abort with
    **`MS_ABORT_NO_HEADING_MEASUREMENT`** (compass busted). There is no good
    in-water fix for a genuinely bad compass — the durable answer is to
    recalibrate after recovery. See the [Aborts](../../../piloting/slocum/aborts.md)
    page for handling device errors at sea.

---

## High-latitude operations

Near the magnetic poles the **horizontal** component of Earth's field gets weak
while the vertical component dominates, so the compass is increasingly "looking
at" the vertical field instead of the horizontal field it needs to find heading.
The practical threshold the community has converged on: as the **horizontal field
strength drops below ~10,000 nT**, compass performance degrades. Symptoms include
the glider reading wildly different headings on dive vs. climb and spiraling.
Mitigations:

- Calibrate **in situ at the deployment latitude** rather than relying on a cal
  done further south.
- Keep the **GPS firmware current** so its declination table isn't stale.
- Expect larger residual errors and design the mission to tolerate them.

---

## Symptoms of a bad calibration

The hallmark of a compass problem in flight is the glider **spiraling** —
`m_heading` sweeping through full circles, often on the climb but sometimes the
dive, while `c_fin`/`m_fin` slam from hard port to hard starboard as the
autopilot keeps flipping which way it thinks it must turn. Commanded heading
looks fine; the glider just can't hold it.

!!! warning "Not every spiral is the compass"
    Spiraling and dive/climb roll asymmetry have several causes that mimic a bad
    compass — confirm the compass before tearing into a recovery:

    - **Biofouling on the rudder / hull seams** disrupting flow (often shows up
      1–2 months in, near shore/warm water) → see [Fin /
      Digifin](../digifin/index.md).
    - **A lost or pivoting wing / broken wing rail** — imbalanced roll on
      dive/climb, sometimes without an obvious mass change.
    - **Center of gravity too close to center of buoyancy** — small transverse
      imbalances produce large, variable roll (a stable glider holds roll
      standard deviation < ~0.25°).
    - **A loose internal component** (e.g., a shifted nose hydrophone) changing
      the roll between dive and climb.

    A useful tell that the compass itself is **good**: run the in-situ cal and
    confirm it agrees with the shore cal — if it does, look mechanical.

---

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| **"Mag out of range"** (red) in RevolutionTest, no points collected | Too much magnetic interference at the location, or the attitude sensor's serial stream isn't really getting to the software. Move well away from metal/electronics; confirm `talk att`/`talk attitude` is actually streaming; take the sensor in/out of service and retry. |
| RevolutionTest **won't connect** / icons don't change color | Another program still holds the **COM port** — fully close your serial terminal so the port is free, then start RevolutionTest on that same port at 9600 baud. |
| `talk attitude` shows **only one line** of output (often G3S) | The compass is stuck in TNT **sample mode**, so it isn't streaming continuously. From GliderDOS confirm `m_attitude_rev_mode = 0` and `m_attitude_rev_measure_state = 0` (defaults), then re-issue the compass command to return it to continuous output. |
| Calibration **"inadequate data points"** / won't finish | Coverage is incomplete — rotate **much** more aggressively through pitch and roll extremes (the roll/`z` bins need the most). Also check for a magnetized battery pack (degauss it). |
| Compass good on bench, **~12° off in a post-cal check** | The **solenoid is open** during your GliderDOS check — inflate the air bladder and wait for the air pump to stop so the solenoid closes, then re-check. |
| RevolutionTest won't run / "no permissions" / fails to launch | Historically version- and Java-sensitive — some users only succeeded on Windows XP (ideally with a real serial port) and struggled on Windows 7. Run as administrator; try a known-good machine. |
| Compass keeps going **out of service** near fields, frequent `attitude_rev` aborts | Expected near strong fields; if persistent, verify **Service Bulletin 011** warning-level settings are applied. Recalibrate after recovery. |

---

## Quick reference

| Command | What it does |
|---|---|
| `talk attitude` / `talk att` | Stream raw attitude data (and close the solenoid); G3/G3S use `attitude`, G2 uses `att` after `exit pico`. |
| `report ++ m_heading m_pitch m_roll` | Watch heading/pitch/roll from the console while rotating the glider (inflate air bladder first for a valid check). |
| `report clearall` | Stop the live reports. |
| `compass_cal ?` | List the `compass_cal` sub-commands. |
| `compass_cal get_offsets` | Read the current X/Y/Z hard-iron offsets. |
| `compass_cal set_offsets X Y Z` | Write new X/Y/Z offsets (**keep the negative signs!**). |
| `use` / `use - iridium` | Check device status / take Iridium out of service during a cal. |
| `exit reset` | Reset the glider to bring `attitude_rev` back online after an in-situ cal. |
| `run attcal2.mi` | Run the (community-tuned) in-situ calibration mission. |
| `send *.cal -num=1` | Send the generated calibration file off the glider. |

---

## See also

- [Fin / Digifin](../digifin/index.md) — steering, the spiral signature, and
  RF-coupling false leak detects (same interference family as Iridium-during-cal).
- [Freewave](../freewave/index.md) — the RF link most teams use to run the
  calibration on a hanging glider.
- [Pitch Vernier](../pitch/index.md) — pitch/roll behavior and re-trimming after
  moving internal mass.
- [Aborts](../../../piloting/slocum/aborts.md) — handling `attitude_rev` device
  errors and `MS_ABORT_NO_HEADING_MEASUREMENT` at sea.
