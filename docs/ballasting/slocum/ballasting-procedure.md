---
title: Slocum Ballasting Procedure
description: Tank ballasting procedure for the Slocum G3 glider — vacuum prerequisite, ballast mode, tank immersion, weight adjustment, tank-to-target correction, and H-moment.
---

# Slocum Ballasting Procedure

Ballasting adjusts the glider's mass and mass distribution so it is neutrally
buoyant and correctly trimmed in the water it will actually be deployed into
— not the tank it's ballasted in. Get it wrong and the glider flies
asymmetric dive/climb profiles, wastes buoyancy-pump energy fighting an
unwanted heaviness or lightness, or in a bad case just sits on the bottom or
can't submerge.

!!! info "Source"
    Paraphrased from the *Slocum G3 Glider Maintenance Manual* (Chapter 3,
    "Ballasting"), the *Slocum G3 Glider Operators Manual*, and the Teledyne
    Webb Research operator training course. Always defer to the official
    Teledyne documentation, and use TWR's **Ballast Adjustment Spreadsheet**
    (contact `glidersupport@teledyne.com` for a copy) for the actual
    tank-to-target weight calculation rather than hand-deriving it.

---

## Before you start: vacuum

The glider must be closed with a proper vacuum **before** it is powered up —
see the [one-pager](../../lab-test/guides/slocum-one-pager.md). Evacuate to
at least **6 in Hg (shallow glider)** or **7 in Hg (deep glider)**; pulling a
higher vacuum than the minimum is better practice, since some air bleeds in
once the glider is powered. Seal with the 7/16-20 PEEK MS plug torqued to
**15 in-lb** — PEEK is delicate, so use the correct tools and torque.

---

## The goal

Ballasting is done with the glider in a defined reference state:

| Component | Reference position |
|---|---|
| Displacement (buoyancy) pump | 0 cc |
| Pitch vernier | 0 in |
| Static roll | 0° |
| Air bladder | Deflated |

The `ballast` command (from `lab_mode`) drives all of these to that reference
state in one step.

!!! danger "Never deploy a glider in `ballast`."
    Exit `ballast`/`lab_mode` and confirm the glider is back on a normal
    mission before it goes in the water.

---

## Setting the glider to ballast mode

1. Power the glider — external power cable (15 VDC) or the green go-plug.
2. If in PicoDOS, type `app` to start GliderDOS.
3. `Ctrl-C` (when prompted) to get control of the glider.
4. `callback 30`
5. `lab_mode on`
6. `ballast` — deflates the air bladder and zeroes the buoyancy pump and
   pitch vernier.
7. On external power: `exit`, wait for the glider to confirm it's OK to
   remove power, then pull the plug and fit the **red** dummy plug. On
   internal (battery) power the glider can stay on.

---

## Reading tank density in real time

To compare the tank to the target deployment water you need live science
data. Either drive the sensors directly:

```
put c_science_all_on 0     (all sensors, fastest sample rate; -1 = off)
put c_science_on 3         (display to screen; 1 = off)
put c_science_send_all 1   (send to the flight Persistor; 0 = off)
```

or use the shortcut mission files: `loadmission sci_on.mi` /
`loadmission sci_off.mi`. Use the CTD's temperature and conductivity to
compute the tank's salinity and density, and enter them — along with the
target water's temperature and density — into TWR's Ballast Adjustment
spreadsheet.

---

## Immersing the glider

1. Lower the glider into the test tank. **Purge every trapped air bubble**
   from the nose cone and aft cover — bump the nose gently against the tank
   wall and tap the aft cover until nothing comes loose. HD (deep) pumps have
   a much larger internal volume to clear, so take extra care.
2. Fit the wings into the wing rails. If the tank isn't large enough to fly
   the wings, lay them stacked on the aft hull section, aligned with the
   wing-rail holes, and hold them with a wrap of electrical tape.

!!! warning "Care during ballasting with HD pumps"
    Incomplete air removal from an HD (deep) buoyancy pump is a common cause
    of a badly ballasted glider — the trapped air itself has buoyancy that
    throws off every measurement taken afterward.

---

## Adjusting the glider's weight

**If the glider is too light**, add weight. Two families of options:

- **External hull weight** (fast, no need to open the glider) — at the
  fore/aft end-cap joints, and at the fore/aft ends of the payload bay. This
  weight displaces water, so before converting it into an *internal*
  equivalent, correct for displacement: external **stainless steel** weight
  × **0.875**, or external **lead** weight × **0.912**, gives the internal
  weight it corresponds to.
- **Internal weight and balance** — stainless weights or lead shot in the
  two forward **ballast bottles** (60 mL each); factory steel weights in the
  unused battery brackets on 200 m gliders running lithium packs;
  pie-shaped stainless roll weights at the fore/aft ends of the payload bay;
  shifting payload or batteries; weight bars with tapped holes in the
  payload bay for bolt-on plates or ballast bottles.

**If the glider is too heavy**, hang spring scales from the fore and aft
end-cap attachment points to read off the imbalance and total excess weight
before removing anything.

---

## Correcting tank weight to target water

The glider is ballasted neutral **in the tank**, but it needs to be neutral
in the **target deployment water**, which almost never has the same density
or temperature. The correction depends on the glider's displaced volume, a
thermal expansion coefficient (β ≈ 535 × 10⁻⁶), and the density/temperature
difference between tank and target water — use the Ballast Adjustment
Spreadsheet rather than computing it by hand.

| Glider type | Displacement (L) |
|---|---|
| G1 (200 m) | 52.0 |
| G1 (1000 m) | 55.2 |
| G3 (200 m and 1000 m) | 56.3 |
| Additional science bay | +9.0 |

Confirm the exact figure for your specific hull/payload configuration with
Teledyne — these are starting points, not a substitute for the spreadsheet.

---

## H-moment

H-moment is the distance — **5–6 mm is ideal, 4–7 mm acceptable** (bias
toward 7 mm for heavy thruster use) — between the glider's center of
buoyancy and center of gravity. It's the glider's equivalent of a boat's
righting moment.

- **Too large (stiff):** the pitch battery has to travel further on every
  inflection, burning more energy; in a bad case the glider can't dive and
  climb at all and just "pancakes" through the water.
- **Too small (twitchy):** the glider makes constant small pitch
  corrections to stay stable, burning energy; in a bad case it can flip over
  and stay flipped.

Measure it with the glider powered and neutral in the tank: `report ++
m_pitch m_battpos` streams pitch (radians) and battery position (inches)
every cycle — feed the readings into the Ballast/H-moment spreadsheet.
Adjust with the pie-shaped roll weights at the payload bay ends: moving mass
**low increases** H-moment (stiffer), moving mass **high decreases** it
(twitchier). Measure H-moment **before** the final mass adjustment, and
re-measure it any time you change the glider's configuration (new sensor,
different battery, added payload) — you don't need to re-measure it on every
routine ballast.

---

## Equipment

| Item | Notes |
|---|---|
| Ballast tank | Minimum 8 ft × 4 ft × 3 ft (2.5 × 1.2 × 1 m), plus a way to get the glider in and out (winch, low side wall, hoist) |
| Vacuum pump | e.g. Thomas 2688CE44 or equivalent |
| Gram scale (0–2 kg) | For weighing internal ballast pieces |
| Hanging gram scale | For weighing the glider in the tank |
| Lead shot / ballast material | — |

---

!!! tip "Ballasting is iterative"
    Expect to open and close the glider several times (three to six is
    common) before the ballast is right. Treat these working opens
    differently from a final pre-deployment seal — take more care with
    O-rings and sealing surfaces on the seal that's actually going in the
    water. See [Autoballast](../../piloting/slocum/autoballast.md) for how
    the glider fine-tunes its buoyancy drive once it's already in the
    water.
