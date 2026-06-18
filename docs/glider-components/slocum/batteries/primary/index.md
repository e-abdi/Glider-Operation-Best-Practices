---
title: Primary Batteries
description: Slocum primary (non-rechargeable) battery packs — alkaline and lithium types, capacities and undervolts settings, derating, voltage shelves, switching battery types, and shipping.
---

# Primary Batteries

Slocum gliders run on one of several **primary (non-rechargeable)** pack types:
**alkaline**, **3S lithium primary**, and the newer **4S lithium primary** —
each available in standard and extended (energy-bay) configurations. Choosing a
type is a trade-off between cost, energy, and handling/shipping burden.

!!! info "Source"
    Paraphrased and consolidated from the *Slocum Glider Operators Manual*, the
    Teledyne Webb Research (TWR) user forum, and the UG2 community Slack. Capacity
    and derating figures evolved over the years and depend on configuration —
    treat the authoritative values as those in your glider's `autoexec.mi` and the
    current TWR specifications, and contact Glider Support before changing
    abort settings. See also the capacities figure on the
    [Batteries](../index.md) page.

---

## Pack types & chemistry

| Type | Configuration | Nominal voltage | Notes |
|---|---|---|---|
| **Alkaline** | C-cells | ~13 V | Lowest energy and cost; needs a Teflon slide sheet and aft bracket (see below) |
| **3S lithium primary** | 3 DD cells in series (78 DD + 3 C emergency, standard G2) | ~10.8 V | Lithium thionyl chloride (Electrochem). Stop diving and drift at the first shelf |
| **4S lithium primary** | 4 DD cells in series | ~15 V | Newer; can fly on the first (11.5 V) shelf toward recovery |
| **Emergency battery** | 3 C cells | — | Lithium: a standalone pack in the forward section. Alkaline: included in the aft pack |

!!! note "Lithium content (for paperwork)"
    Each **DD cell ≈ 10.2 g** lithium; each **C cell ≈ 2.2 g**. A standard pitch
    pack is 36 DD cells, the aft pack 42 DD, plus 3 C cells in the emergency pack.

---

## Capacity & undervolts settings

Set **`f_coulomb_battery_capacity`** and the mission **undervolts** abort to match
the installed pack — uncomment the matching line in `autoexec.mi` when you change
type. Representative values:

| Pack | `f_coulomb_battery_capacity` (Ah) | Undervolts abort (V) |
|---|---|---|
| Alkaline (nominal) | 120 (≈153 typical G2 estimate) | 10 |
| 4S lithium, standard | ~498–550 | 12 |
| 4S lithium, extended energy bay | ~800 | 12 |
| TWR rechargeable, standard | 215 | 12.5 |
| TWR rechargeable, extended | 300 | 12.5 |

!!! warning "Zero the coulomb counter on every battery change"
    Each time new batteries are installed (or rechargeables are charged), zero the
    counter or you risk spurious aborts:

    ```text
    put m_coulomb_amphr_total 0
    exit reset
    ```

    Confirm the value starts climbing from 0. With capacity and undervolts set
    correctly, `m_lithium_battery_relative_charge` then tracks how much of the
    pack has been used, and the glider aborts on `MS_ABORT_CHARGE_MIN` when
    `remaining_charge_min` (default 10 %) is reached.

!!! tip "Lithium + GliderDOS"
    Avoid running the glider on lithium batteries while sitting in GliderDOS — the
    coulomb meter does not record amp-hours consumed below that software level.
    Use AC/DC wall power for extended bench work.

---

## Derating & end-of-life behaviour

- **Storage age:** TWR recommends derating capacity by **~3 % per year of
  storage**. (Some operators have seen larger-than-expected losses on
  *partly-used* packs left in storage — derate conservatively and budget margin.)
- **Temperature/variability:** an additional ~10 % derate is commonly applied to
  cover temperature swings.

**Voltage shelves.** Lithium primary packs hold a fairly flat voltage, then drop
onto a **shelf** near end of life before a final steep decline to shutoff (~10 V):

- **3S:** stop diving and put the glider into a **drift** once the energy reaches
  the first shelf.
- **4S:** you *can* keep flying on the first (~11.5 V) shelf toward a recovery,
  but the **appearance of a second shelf drop may be the last time the glider
  communicates**. Never deplete either type to the second shelf operationally.
- Practical undervolts strategy for 4S: set the abort to **12 V** as an early
  alert that the glider is approaching the 11.5 V shelf; ~5 % or more of the
  pack's energy may remain on the shelf, so a lower abort (e.g. **9.5 V**) can be
  used deliberately to fly home.

---

## Switching between alkaline and lithium

Swapping chemistry is more than a battery change — several hardware and software
items must move together:

- **Mainboard connector / enable circuit.** TWR lithium packs have an *enable
  circuit*; the mainboard has separate connectors for each type, so switching
  types means moving the power connector to the matching one. (Non-TWR lithium
  packs, e.g. custom builds, generally wire to the **alkaline** connector.)
- **`battpos` calibration.** Uncomment the matching `f_battpos_safety_max`,
  `f_battpos_cal_m`, `f_battpos_cal_b` set in `autoexec.mi` for your pump and
  chemistry — the lithium pitch pack sits further forward, so the travel limits
  differ. (Field note: on a G2 with a 200 m / 800 cc pump, alkaline
  `f_battpos_safety_max` should be ≤ ~1.4 in so the forward battery doesn't hit
  the pump.)
- **Mechanical.** Alkaline needs a **Teflon sheet** on the forward hull for the
  pitch battery to slide against, and an **aft bracket** (with the two
  battery-securing pin holes). With lithium, roll adjustment is done with pie
  weights / added mass rather than the bracket.
- **Emergency battery.** The lithium emergency pack is a standalone forward
  pack and must **not** be used with alkaline (whose emergency cells live in the
  aft pack).

!!! warning "Re-check the compass after any battery change"
    Batteries carry a magnetic field that can affect compass calibration. At
    minimum, do a **four-point compass check** before each deployment after
    installing new batteries.

---

## Shipping & transport

Lithium primary packs are **Class 9 dangerous goods**. Ship/declare using the
correct UN number and have the **Safety Data Sheet** (available from TWR /
Electrochem) on hand.

| Item | Standard pack | Extended (energy bay) |
|---|---|---|
| UN number — batteries in boxes | **UN 3090** | UN 3090 |
| UN number — batteries installed in glider | **UN 3091** | UN 3091 |
| Cell count | 78 DD + 3 C | 114 DD + 3 C |
| Total lithium mass | ~803 g | ~1170 g |
| Total capacity | ~702 Ah | ~1026 Ah |
| Max battery weight | ~20 kg | ~30 kg |

!!! note "Ground transport exemptions vary by region"
    Some operators classify a glider-with-batteries as a **research vehicle**,
    which can fall under the same exemptions as e-scooters/hoverboards (e.g.
    "Marine Research Vehicles … Special Case 67" under certain national rules).
    This is region-specific — confirm with your dangerous-goods authority before
    relying on it, and note that vessel (at-sea) rules differ from road rules.

---

## Lithium safety on vessels

Operators increasingly need written procedures for carrying and charging lithium
batteries on ships. There is no single standard yet (a community/UG2 best-practice
effort is underway), but field-tested measures include:

- **Charge outside** the vehicle's accommodation spaces, and (on G3s that allow
  it) charge while the glider is **powered on** so you can monitor internal
  temperature; the rechargeable BMS reports per-sub-assembly thermistor data.
- **Thermal imaging camera** during charging and as a pre-deployment check.
- **Lithium-rated fire blankets / bags** sized for a full glider (spec them
  properly — consumer e-bike sizes are too small), and consider **PyroBubbles**
  in shipping containers.
- A practical **containment / ejection plan**: rather than an (impractical)
  explosion-proof cabinet, keep the glider on the back deck with a way to put it
  **over the side** if a pack goes into thermal runaway — e.g. a steel cable and
  crane, or a release ramp.

!!! danger "These hazards apply to rechargeable lithium-ion packs too"
    The same handling, charging, and shipping caution applies to the
    [rechargeable lithium-ion packs](../rechargeable/index.md) — they are a
    different chemistry/transport class but pose comparable fire risk.
