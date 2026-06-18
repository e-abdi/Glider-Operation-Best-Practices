---
title: Deep Pump
description: Slocum deep (hydraulic) buoyancy pump — rotary oil-displacement design, the G3 HD pump and 3-way valve, vacuum requirement, storage, testing, and field troubleshooting of oil leaks and faults.
---

# Deep Pump

The deep buoyancy pump (350 m and 1000 m, ~900 cc) is a **rotary displacement
(hydraulic)** design. Instead of moving seawater, it moves **oil** from an
**internal reservoir** to an **external bladder** to change the vehicle's
buoyancy. A rotary valve controls the flow of oil from the bladder back into the
reservoir.

!!! info "Source"
    Paraphrased and consolidated from the *Slocum G3 Glider Operators Manual*, the
    TWR user forum, and the UG2 community Slack. Pumps are **factory configured** —
    contact `glidersupport@teledyne.com` before changing pump settings. See also
    the [Shallow Pump](../shallow-pump/index.md).

---

## Vacuum requirement

!!! warning "Operate under vacuum"
    The glider must be **under vacuum** while running the deep pump — the internal
    vacuum is what draws oil from the external bladder back into the body. Running
    it without vacuum won't *damage* the pump, but the oil won't retract properly.

The deep pump can **retract at any depth** (unlike the shallow pump, which is
limited to its rated range). Even so, deep gliders are rarely inflected at the
top for sustained operation below ~75 m.

---

## The G3 HD pump & 3-way valve

The deep pump was redesigned for the G3 to be more robust and easier to maintain.
It uses the device name **`hd_pump`** (must be in the installed-devices list in
`autoexec.mi`) and adds a **3-way ball valve** controlling oil flow from the
external bladder back into the reservoir.

- In normal operation the valve **opens at the surface** to retract oil and begin
  the dive, then stays **closed for the whole dive** (including the bottom
  inflection, where oil is pushed out from the reservoir to become positively
  buoyant). It typically never has to open against high pressure.
- A **drift-at-depth** mission (becoming positively then negatively buoyant at
  depth) can push higher pressure on the valve. The 3-way valve offers a
  **restricted** and an **unrestricted** port: the unrestricted port allows much
  **faster inflections**, making deep gliders far more efficient in shallow water.

!!! danger "Don't touch `u_valve_open_max_depth`"
    The depth at which the glider switches between the restricted and unrestricted
    valve positions is set by `u_valve_open_max_depth`. **Do not change it from the
    default without specific instructions from Teledyne** — the restrictor exists
    to keep the internal plumbing from seeing damaging pressure.

---

## Storage & shipping

!!! tip "Retract the oil fully before storing or shipping"
    TWR advises **fully retracting the oil volume** when storing or shipping deep
    systems (350 m and 1000 m). Reasons:

    - **Reduces gas transfer** across the bladder membrane — with little oil left
      in the external bladder, even at saturation equilibrium the total dissolved
      gas is much lower. (In water there's no saturation gradient, so this isn't an
      issue underway.)
    - **Keeps the bladder in its molded shape** rather than wrinkled or creased —
      these repurposed rolling diaphragms are happier without sharp creases.
    - **Reduces oil-slosh forces** on the bladder during transport.

**Bladder care:** store clean and free of foreign matter using clean water and a
clean cotton cloth. **Do not** use solvent-based cleaners (acetone, alcohol) —
they dry out the bladder and shorten its life. No storage lubrication is required,
but a thin layer of **silicone oil or silicone spray (e.g. Molykote 316)** is
recommended.

---

## How to test

From `lab_mode`:

1. `wiggle on`
2. `report ++ m_de_oil_vol`
3. Confirm the pump completes a full extension (`m_de_oil_vol = +430 cc`) and full
   retraction (`-430 cc`) without errors.
4. `wiggle off`

To confirm the pump is active: on every power-up the pump extends buoyancy to full
displacement; `report ++ m_de_oil_vol` shows the position moving. With a properly
ballasted glider, **positive cc → climb**, **negative cc → dive**.

| Sensor | Description |
|---|---|
| `m_de_oil_vol` | Measured oil volume / buoyancy (cc) |
| `c_de_oil_vol` | Commanded oil volume / buoyancy (cc) |
| `m_is_de_pump_moving` | Whether the displacement pump is currently moving |

---

## Field troubleshooting

### Small oil leaks in the forward section

A recurring G3 issue: a **small amount of oil** (a few mL / about a teaspoon)
appears in the forward section after a mission, often smeared by the pitch
battery, and frequently **cannot be reproduced in the lab**.

- TWR traced many cases to the **ribbed oil tubing** developing slow leaks over
  time and has moved to an upgraded tubing — have it replaced at service.
- A leaking pump often shows up as a **reduced total available oil volume** (one
  operator saw it down to about −311 cc). In reported cases up to ~9-month
  deployments it didn't degrade performance or compromise the O-rings, but you
  should not knowingly deploy a glider in that state.
- TWR strongly recommends letting them re-seal/re-service the oil system. If you
  do inspect it yourself (e.g. before sending it back anyway), don't over-torque
  hose clamps/fittings, and photo-document the teardown.
- A bench check some operators use: with the glider open but electrically
  connected, attach a vacuum pump to the open barb on the oil reservoir, clean up
  all old oil, lay shop towels around the pump, then manually command
  `c_de_oil_vol` out to +500 and use the vacuum to pull it back to −500, watching
  for where fresh oil appears. (Running the oil pump without vacuum is acceptable
  only in this limited way.)

### Pump fault / stuck

- **`DRIVER_ODDITY: ... Buoyancy Pump is FAULTED!`** with `MOVE ERROR Error
  reading position` and the pump repeatedly taking itself out of service usually
  points to a **failed position potentiometer** (the board reading pump volume) —
  typically a TWR rebuild, not fixable at sea.
- A pump fault closely followed by a **dropping leak-detect voltage** can mean
  water intrusion shorting the pump electronics (e.g. a torn/perforated bladder
  weeping into the nose). Plan a recovery.
- Field stopgap when the pump is stuck at a fixed volume: setting
  `f_ballast_pumped_safety_max` to the stuck value can let you re-enable the pump
  (held in place) and limp toward recovery on the thruster.
