---
title: Pitch Vernier (battery movement)
description: How the Slocum sets pitch by sliding its ~10 kg forward battery pack fore and aft on a lead screw — the c_use_pitch battpos/setonce/servo modes, the m_battpos/c_battpos sensors, securing the pitch battery with blue Loctite so the screw can't back out mid-mission, and field troubleshooting for a loose, stuck, or non-moving pitch battery.
---

# Pitch Vernier (battery movement)

The Slocum doesn't have elevators or a moving tail to set its dive angle — it
**slides its heaviest internal mass back and forth.** A **lead screw drives the
forward ~10 kg battery pack fore or aft**, shifting the centre of gravity to trim
the vehicle's pitch. The manual calls this the **Pitch Vernier**: the
[ballast pump](../pumps/index.md) supplies the *buoyancy* that makes the glider
dive or climb, and the moving battery is the **fine adjustment** that sets *at what
angle* it does so.

- Moving the battery **forward** makes the nose **heavy → the glider pitches down
  (dive)**.
- Moving the battery **aft** lifts the nose **→ the glider pitches up (climb)**.
- On the surface the battery is driven **all the way forward** to raise the tail
  (and its antennas) out of the water for comms.

The vehicle is designed to dive and climb at about **26°**. This only works if the
glider is properly trimmed — the **H-moment must be 6 mm ±1** (see *H Moment
Calculation* / *Adjusting the H Moment* in the Maintenance Manual) — otherwise the
ballast pump's moment won't pitch the glider as expected and the battery vernier
has to fight it.

!!! info "Source"
    Paraphrased from the *Slocum G3 Glider Operators Manual* (Rev. 1, "Pitch
    Vernier" and the sample mission appendix), the *Slocum G3 Maintenance Manual*
    (forward-section assembly), the UG2 community Slack, and the Teledyne Webb
    Research user forum. Condensed field reference — always defer to the official
    Teledyne documentation, and contact `glidersupport@teledyne.com` before
    changing pitch or trim configuration.

---

## Relevant sensors

| Sensor | Meaning |
|---|---|
| `m_battpos` | **Measured** battery position, in **inches** |
| `c_battpos` | **Commanded** battery position, in inches |
| `m_pitch` | **Measured** vehicle pitch (radians) |
| `c_pitch` | **Commanded** vehicle pitch (radians) |

Sign convention (with a properly ballasted glider): **positive/forward** battery
movement brings the **nose down**; **aft** movement **lifts the nose**. As a
practical example from the forum, an operator flying with fixed positions used
**~0.45 in for dives** and **~0.25 in for climbs**.

!!! note "Full travel depends on the build"
    The length of a full battery extension/retraction depends on the **pump type**
    (shallow vs. [deep](../pumps/deep-pump/index.md)) and the **battery type**
    (alkaline vs. lithium). The hard limit, **`f_battpos_safety_max`**, is set per
    glider in its **`autoexec.mi`** — don't assume a number; read it from the
    vehicle.

---

## Three ways to command pitch: `c_use_pitch` / `d_use_pitch`

Dive (`d_…`) and climb (`c_…`) behaviours in the `yo*.ma` file each choose a pitch
**mode** plus a value:

| `…_use_pitch` | Mode | `…_pitch_value` is in | Behaviour |
|---|---|---|---|
| **1** | `battpos` | **inches** | Drive the battery to a **fixed position** and leave it. |
| **2** | `setonce` | **radians** | Move **once** to hit the target angle, then stop adjusting. |
| **3** | `servo` (default) | **radians** | **Continuously** adjust the battery to *hold* the commanded angle. |

- **Servo** flies the most accurate angle but works the motor the hardest. **Fixed
  `battpos`** (mode 1) and **`setonce`** (mode 2) move the motor far less, which is
  why they show up in [power-saving](../../../piloting/slocum/power-saving.md#fly-the-buoyancy-and-pitch-motors-gently)
  and [quiet-mission / acoustic](../../../piloting/slocum/passive-acoustic-monitoring.md)
  setups.
- **`setonce` can miss the target angle** — it commits to one move based on current
  trim, so if trim is off it can settle well short of what you asked (operators
  have asked for 26° and gotten ~18°). Use servo if the exact angle matters.
- **Firmware note:** before release **7.9**, servo mode **hunts continually** and
  restarts each dive/climb from whatever position it was last left at, so the
  battery is mis-placed at the start of every inflection. **7.9 and later remember
  the last good dive and climb `battpos`** and start the servo from there.

!!! tip "Switching to fixed battery position"
    To pin the battery instead of servoing, set the mode to `1` and give the value
    in **inches**, e.g. `d_pitch_value 0.45` (dive) / `c_pitch_value 0.25` (climb).
    If a fixed position doesn't seem to take effect, the **deadzone** may be wider
    than the gap between your dive and climb positions — see troubleshooting below.

---

## Securing the pitch battery — always use blue Loctite

This is the single most common, most preventable pitch problem in the field:
**the pitch battery's mounting screw can vibrate loose during a mission, letting
the battery detach from the lead screw.** The fix is a build-step discipline.

During forward-section assembly the Maintenance Manual is explicit:

> Place a drop of **Loctite 243 (blue)** on the **pitch battery mounting screw**,
> insert the pitch battery (feeding the cable harness through the centre opening),
> then secure it by tightening the mounting screw with the **5/32" × 12" red
> T-handle hex wrench**.

!!! danger "Don't skip the blue Loctite — and confirm the battery is secured"
    Multiple operators have **deployed gliders with a loose or fully disconnected
    pitch battery** — it is easy to overlook when distracted in the lab. Without
    the blue threadlocker the mounting screw can **back out over a mission** and the
    battery works free. Teams specifically call out blue Loctite on this screw to
    put emphasis on the attachment point. Use **blue (243)** — a removable grade —
    not red, so the screw can still be serviced.

**How a loose pitch battery looks in the data (and why it fools you):** the
position pot reads the **motor / lead screw**, not the battery itself, so
`m_battpos` and `c_battpos` can look **completely normal** even after the battery
has come free. But once detached, the battery **slides toward the tail under
gravity** — worst on the climb — so you see **wild pitch, commonly pinned near
~60° nose-up** (the pitch sensor's limit) and poor dives. If pitch is misbehaving
but the battpos numbers look fine, **suspect a loose battery** and open the glider
to check.

!!! warning "Two more assembly gotchas"
    - The **e-bay** and **pitch** battery cable **harnesses look identical but are
      not interchangeable** — a swapped harness can leave you unable to talk to the
      pitch battery (`talk battery` returns nothing/garbled). Confirm the right
      harness and that the connector is fully mated (pins are delicate).
    - Make sure the **battery cable can flex freely** — it has to move as the
      battery travels. Pinched or snagged cable binds the pack.
    - **Re-ballast / re-check trim after moving *any* internal mass** (even a
      desiccant pack). Shifting internal weight changes the H-moment and therefore
      how the vernier flies.

---

## Testing the pitch motor (lab_mode)

From `lab_mode on`:

1. `wiggle on`
2. `report ++ m_battpos`
3. Confirm the battery completes a **full extension and retraction without errors**.
4. `wiggle off`, then `report clearall`.

The `ballast` command sets the **pitch motor and ballast pump to 0** (and deflates
the air bladder) for ballasting — **never deploy a glider left in `ballast` or in
`lab_mode`.**

!!! note "The `pitch_motor … (#/min/mn/max/sd)` message is benign"
    A line like `pitch_motor 1800 -0.023 0.001 0.038 0.015 in` during a wiggle or
    mission is just a **diagnostic** comparing measured vs. commanded position when
    the motor is idle. It's controlled by `f_motor_analyze_deadband` (default 1800,
    so it prints only about every ~7200 s) and is **nothing to worry about**.

---

## When the pitch battery won't move — or you must fly without it

**Pitch battery not moving fast enough?** The usual causes are **mechanical** —
the pack is **bound or its travel is obstructed** so it can't slide freely — or the
**wiring to the position pot or motor is damaged/unplugged**.

**Fixed `battpos` not changing between dive and climb?** Check the **deadzone**:
`f_battpos_deadzone_width` (sets the `x_` limit) and `f_battpos_db_frac_dz`
(deadband as a fraction of the dead zone). If the deadzone (e.g. 0.2 in) is as
large as the gap between your dive and climb positions, the battery never bothers
to move. Narrow `f_battpos_deadzone_width` for that deployment so it always
repositions.

**Flying with a failing pot or a stuck pack:** if the glider is intermittently
aborting for "pitch battery not moving," or the pot is failing, you can fly
**without the pitch motor** entirely:

1. If the battery still moves, **`put c_battpos`** to position it where you want
   (a good dive/climb compromise), then leave it.
2. `use - pitch_motor` to take it out of service.
3. Wait for callback, then in the mission add a `nop_cmds` behavior with
   `nop_pitch(bool) 1` (commands pitch to `_IGNORE` to keep the behavior stack
   busy).
4. In the `yo` behavior, change `start_when(enum)` to **4** (start when the
   buoyancy engine is idle) instead of the usual pitch-idle trigger, so the yo
   still cycles without a pitch command.

---

## Field troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| Glider pitches **~60° nose-up** on climb, dives poorly, but `m_battpos`/`c_battpos` look normal | **Pitch battery has come loose / unscrewed** from the lead screw (pot reads the motor, not the battery). Open up, re-secure with **blue Loctite 243** on the mounting screw. |
| `talk battery` can't reach the pitch pack | Wrong/identical-looking **harness swapped** with the e-bay battery, or connector not fully mated. |
| **Pitch battery not moving fast enough** | Pack **mechanically bound/obstructed**, or **pot/motor wiring** damaged or unplugged. |
| Servo keeps **pushing the battery to its limit** and never reaches the angle | Trim/**H-moment off** (needs 6 mm ±1), or battery loose; verify ballast and trim. |
| **Fixed battpos** won't change between dive and climb | **Deadzone too wide** — reduce `f_battpos_deadzone_width`. |
| Intermittent **"pitch battery not moving" aborts** / failing pot | **Fly without the pitch motor** (recipe above): `use - pitch_motor` + `nop_pitch` + `start_when 4`. |
| `pitch_motor (#/min/mn/max/sd)` line in the log | **Benign diagnostic**, not an error. |

!!! tip "Quick reference"
    | Item | Command / sensor |
    |---|---|
    | Measured / commanded battery position | `m_battpos` / `c_battpos` (inches) |
    | Measured / commanded pitch | `m_pitch` / `c_pitch` (radians) |
    | Pitch mode (dive / climb) | `d_use_pitch` / `c_use_pitch` — `1`=battpos `2`=setonce `3`=servo |
    | Pitch value | `d_pitch_value` / `c_pitch_value` (inches if mode 1, radians if 2/3) |
    | Travel limit | `f_battpos_safety_max` (in `autoexec.mi`) |
    | Deadzone width | `f_battpos_deadzone_width` |
    | Move the battery directly | `put c_battpos <inches>` |
    | Take the motor out of service | `use - pitch_motor` |
    | Bench test | `lab_mode on` → `wiggle on` → `report ++ m_battpos` |
    | Securing screw threadlock | **Loctite 243 (blue)** |

!!! note "Coming later"
    A separate **Autoballast** page (under *Piloting*) will cover how the glider
    automatically tunes its dive depth and buoyancy — pitch trim and autoballast
    interact, but they're documented separately.
