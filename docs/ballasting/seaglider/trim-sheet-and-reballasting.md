---
title: Trim Sheet & Re-ballasting
description: Keeping a Seaglider's trim sheet true to the vehicle, calibrating it against observed centers with a "mystery mass", and re-ballasting for a new target density — with worked examples and the mistakes that most often strand gliders light or heavy.
---

# Trim Sheet & Re-ballasting

The [tank procedure](ballasting-procedure.md) tells you what the glider weighs
and displaces *today*. Most real ballasting work, though, is about **change**:
a new sensor bolted on, a battery or VBD swapped at refurbishment, a fairing
upgrade, or simply a mission in water that is heavier or lighter than the last
one. This page covers the bookkeeping tool that handles those changes — the
trim sheet — and how to move a glider from one target density to another
without guessing.

!!! info "Source"
    Distilled from several years of service and support correspondence between
    Seaglider operators, refurbishment teams, and the vehicle's original
    designers (2016–2024), cross-checked against the
    [Ballasting Procedure](ballasting-procedure.md) and
    [Trim & Flight Model](../../piloting/seaglider/trim-and-flight-model.md)
    pages. Numbers are worked examples from real gliders, not specifications —
    your vehicle's own sheet and tank results always win.

---

## The trim sheet

Every Seaglider is normally delivered (and returned from service) with a
**trim sheet**: a per-vehicle spreadsheet that lists every part on the glider
with its mass, volume, and position along the hull, and from those sums
predicts how the vehicle will sit in water of a given density. Layouts vary
between versions, but the useful pieces are the same:

| Part of the sheet | What it holds | What you use it for |
|---|---|---|
| **Weight sheet** | Every component: quantity, mass, volume, longitudinal position. Includes the variable items — lead strips, foam, nose weights | The single source of truth for *what is on the glider* |
| **Trim** | Totals and predictions for one water density: net buoyancy, internal oil stroke (→ `$C_VBD`), pitch-mass stroke (→ `$C_PITCH`), predicted pitch angle, centers of gravity and buoyancy | Goal-seeking a configuration that is neutral and level |
| **Ballast worksheet** | Tank density, measured mass, neutral VBD in the tank, and a "new environment" block: new density + desired thrust → mass change | Turning a tank result into a lead change |
| **Lead worksheet** | Where each lead strip and foam piece sits, with weights | The physical install plan |
| **Tank / sea-trial notes, log** | Free-text history | Recording what was actually done |

!!! tip "Enter data only in the input cells"
    Most sheets colour-code input cells (typically red text) and compute the
    rest. If a cell that should be a formula holds a typed number — a removed
    item still carrying its mass, say — the whole prediction quietly drifts.
    One sheet reviewed by the designers had a single line stuck at 191 g where
    the formula should have given 0. Comparing the summed mass with a scale
    weight of the whole glider is what catches this kind of error.

### Keep it true to the vehicle

The sheet is only as good as its last update. Anything that changes mass,
volume, or position belongs in it **before** you go near the tank:

- **New or moved sensors** — mass, *volume* (including brackets and cable
  assemblies, which are easy to under-estimate), and position. A volume figure
  that looks suspiciously small compared to similar parts usually is.
- **Batteries** — weigh replacements; primary packs of the same type still
  differ by tens of grams.
- **VBD replacement** — the hydraulic drive, reservoir, and the oil added to
  the system. Upgraded VBDs can be noticeably heavier than the ones they
  replace, so a sheet carried over from the old engine will mispredict.
- **Fairings** — older fairings were solid fibreglass; later ones have a
  syntactic-foam core with a much lower effective density. Swapping one for
  the other without updating the sheet can produce errors of hundreds of cc.
- **Wings and rudder** — weigh them. Early on, wing sets were kept with their
  own vehicle because pairs could differ noticeably; modern sets are closer,
  but a borrowed set on one glider still differed by ~30 g. Record which set
  is fitted.
- **Lead and foam** — every piece, by weight and position (see
  [inventory](#inventory-the-lead-and-foam-every-time) below).

Then **weigh the whole glider dry** and compare it with the sheet's summed
mass. The difference is the sheet's error budget: within a few tens of grams
(scale accuracy) is good; hundreds of grams means a missing or stale line
somewhere, and it is far cheaper to find on the bench than at sea.

---

## Goal-seeking a configuration

With the sheet up to date, the routine is the same whether you are adding a
sensor or changing water density:

1. **Set the target density** in the Trim tab (see
   [choosing a target density](#choosing-the-target-density)).
2. **Goal-seek net buoyancy = 0** by changing the internal oil stroke. The
   result is where the VBD will sit at neutral — your predicted `$C_VBD`.
3. **Goal-seek pitch angle = 0** by changing the pitch-mass stroke. The
   result is the predicted `$C_PITCH`.
4. **Check the margins**:
    - *Oil stroke* — leaves the thrust you want on both sides of neutral (see
      [thrust margin](#thrust-margin)).
    - *Pitch-mass stroke* — around **70 %** is the nominal design point. Much
      lower or higher eats into the pitch authority you need to dive steeply
      in one direction.
5. **If a margin is off, move lead, don't just add it.** One team fitting a
   heavier aft sensor first tried compensating with extra lead; the better
   fix was to move existing lead strips from aft of the joint ring to forward
   of it, which corrected pitch while keeping total mass (and therefore
   `$C_VBD`) where it was. Re-run steps 2–4 after each change.

!!! note "Adding lead also adds volume"
    Lead is ~11.3 g/cc, so every gram of lead added also displaces a little
    water. In seawater, 100 g of lead adds only about **91 g** of net
    weight-in-water. The ballast worksheet accounts for this; back-of-envelope
    sums often don't.

---

## Calibrating the sheet: the "mystery mass"

Sooner or later the sheet and the real vehicle disagree. Classic case: a
glider upgraded to a new fairing type had every row of its sheet carefully
updated, and the scale weight matched the sheet to within 20 g — yet in the
sea it came out roughly **1 kg too light**. Foam came off, lead went on, and it
flew fine, but the sheet no longer described the vehicle.

The fix is to stop trying to find the error by inspection and instead
**calibrate** the sheet against what the glider actually does:

1. Take **observed centers** — the neutral `$C_VBD` and level `$C_PITCH`
   either from a [tank trim test](ballasting-procedure.md#alternative-the-neutral-point-tank-trim-test)
   or from well-trimmed dives of a real mission — plus the density they were
   observed at.
2. Add a line to the weight sheet for a fictitious item (call it
   "mystery mass" or "ghost volume").
3. Goal-seek that item's **mass/volume and position** until the sheet
   reproduces the observed `$C_VBD` and `$C_PITCH` at the observed density.
4. Now change the density, lead, or sensors you actually want, and read off
   the new predicted centers.

The mystery line absorbs whatever the sheet doesn't know — fairing density, a
mis-measured bracket, a heavier engine — so changes *relative* to the
calibrated state come out right even when the absolute numbers didn't. One
team re-used the same calibrated ghost item for a later mission with a
different sensor suite and water density, and the glider flew well first
time.

!!! tip "Calibrated sheets travel"
    When a glider goes to a new operator or back from refurbishment, send the
    calibrated sheet *and* the observed centers it was fitted to. Without those,
    the next person starts over.

---

## Re-ballasting for a new density

### Choosing the target density

`$C_VBD` matters most where the glider is **neutral** — in practice the
density near the bottom of the dive (apogee), and to a lesser degree the
surface layer where it has to recover the antenna. Sources, best first:

- **CTD casts or glider data from the same area and season.**
- **Climatology** — Argo float profiles are excellent. One team preparing an
  open-Atlantic mission pulled ten years of Argo profiles around the track:
  surface density varied seasonally between about 1025 and 1027 kg/m³, while
  density at 1000 m sat in a narrow band around 1032. That spread tells you
  the surface is the uncertain end and the deep value is reliable.
- **The last mission's numbers** — only if the area and season really match.

Write the density down **in the sheet** and in any work order. Two gliders in
one fleet came back from service ballasted for 1027.5 kg/m³ when the operator
had requested 1029.2 for a polar mission. The first was only discovered at
sea: it sat light and flat at the surface with a poor antenna position,
Iridium sessions kept dropping, and the team struggled to trim it through
repeated no-comm dives (a damaged antenna cable found after recovery probably
made things worse). Reducing `$SM_CC` helped a little but cannot make up 1.7
density units. The second was caught by reading its trim sheet before
deployment.

!!! warning "Check the density cell when a glider comes back"
    Whenever a glider returns from refurbishment, open the trim sheet and look
    at the density it was ballasted for before anything else. It takes ten
    seconds and avoids the scenario above.

### How big is a density change?

The arithmetic is simple. A Seaglider displaces roughly **52 litres**, so

> buoyancy change (cc, or g) ≈ glider volume (L) × Δρ (kg/m³)

| Density change | Buoyancy change | ≈ VBD counts (at ~4 counts/cc) | Lead equivalent (seawater) |
|---|---|---|---|
| 0.5 kg/m³ | ~26 cc | ~105 | ~29 g |
| 1.0 kg/m³ | ~52 cc | ~210 | ~57 g |
| 1.7 kg/m³ (1027.5 → 1029.2) | ~88 cc | ~360 | ~97 g |
| 2.0 kg/m³ | ~104 cc | ~420 | ~114 g |

Going into **denser** water makes the glider lighter: it either needs more
lead, or a higher `$C_VBD` (neutral reached with more oil inside), which costs
you buoyancy margin at the surface. Going into **lighter** water is the
reverse.

**Example — absorbing it in `$C_VBD`.** A glider last flown with `$C_VBD`
2557 at 1027.5 kg/m³ is going somewhere ~1 unit denser at its working depth.
52 cc × 4 counts/cc ≈ +210 counts, so start the mission near `$C_VBD` ≈ 2770
and let the first dives' regressions refine it. Cross-check with the trim
sheet: put in the new density and the stroke the glider actually flew at last
time — it should give a very similar answer. If the two disagree, trust
neither until you know why. Then check that the remaining thrust is still
enough (next section); if not, add lead instead.

**Example — rebalancing with lead.** A glider ballasted for 1027.5 kg/m³
needs to fly at 1029.2 — about 88 cc lighter in the new water, so roughly
**100 g of lead** once the lead's own volume is accounted for. Before
changing anything, take the fairing off, photograph and weigh every existing
lead strip (in the case this is drawn from, five strips of 111–129 g plus
eleven foam pieces) and confirm the sheet matches what's on the hull. Then set
the new density in the sheet, let it compute the mass change, and split the
added lead forward and aft of the joint ring so that the pitch-mass stroke
stays near its old value.

### Thrust margin

**Thrust** is how much buoyancy the VBD can still produce beyond neutral —
it's what drives the climb and what lifts the antenna clear at the surface.

- Designers set gliders up for roughly **250–300 cc** of maximum thrust in the
  target water. One refitted glider (two new sensors added, sheet showing
  ~1.3 kg *less* mass than before) came out with neutral at ~87 % oil stroke
  and only ~114 cc of thrust — flagged as "not much" before it left the
  bench, and a hint that the new sensor volumes in the sheet needed
  re-checking.
- **~210 cc** is on the light side; operators flying shallow, calm missions
  can live with it, but in strong currents or rough seas you will want more.
- Mission settings like `$MAX_BUOY` are then a choice *within* that range —
  the [Trim & Flight Model](../../piloting/seaglider/trim-and-flight-model.md#tactics-strong-currents-and-making-progress)
  page covers when to use it.

### How much density range can one ballast cover?

The VBD's usable range divided by the glider's volume gives the span of water
densities one ballast setting can handle. For a ~52 L Seaglider with a few
hundred cc of usable stroke on each side of neutral, that's a handful of
kg/m³ — enough for most open-ocean missions, but **not** for plunging from a
fresh river plume into full-salinity water, or for crossing a front with a
large density jump without re-ballasting. If the mission spans more than about
±3 kg/m³ (leaving some margin), plan to ballast for the critical end and
accept less efficiency at the other, or split the mission.

!!! warning "Large foam volumes amplify small density errors"
    A payload that forces a lot of syntactic foam onto the hull makes the
    vehicle more sensitive: one heavily foamed glider, ballasted in one sea
    and deployed in a slightly different one, developed a roll instability
    that could not be trimmed out at sea. If an integration needs a lot of
    foam, do the final ballasting **in water from the deployment region** (or
    with its density in the tank) rather than relying on the sheet to
    extrapolate.

---

## Inventory the lead and foam every time

Whenever the fairing comes off, record the variable ballast before touching
it:

- **Count and weigh** every lead strip and every foam piece. Foam strips are
  typically ~15 g each, lead bars from ~60 g to ~180 g.
- **Photograph** each face of the hull (bottom, sides, top) with the ballast
  in place.
- **Note positions** relative to the joint ring / bulkhead — forward or aft
  matters as much as mass.
- Put the numbers in the sheet's lead worksheet and the log.

Why it matters: a glider that behaved differently on two consecutive missions,
in a way the water densities couldn't explain, turned out to be consistent
with **foam having gone missing** between them. Without a before/after
inventory there was no way to prove it either way.

---

## After launch: when the numbers say the sheet was wrong

The first dives are the real ballast test. Signs that the tank or sheet
missed:

- **The glider is clearly heavy or light** — the vertical-velocity regression
  wants a large `$C_VBD` change, the glider struggles to climb, or sits low at
  the surface. See
  [Buoyancy trim](../../piloting/seaglider/trim-and-flight-model.md#buoyancy-trim-c_vbd).
- **FMS / regression fails to converge** with an implausible `vbdbias` and a
  suggestion to reprocess with a different volmax. That almost always means
  the `mass` or `volmax` in `sg_calib_constants.m` is wrong — see
  [When the volume regression blows up](../../piloting/seaglider/trim-and-flight-model.md#when-the-volume-regression-blows-up).

In both cases, back-calculate: once `$C_VBD` is well tuned, the known mass and
the density at apogee give the true volmax. Put that (and the correct `$MASS`)
on the glider and in `sg_calib_constants.m`, reprocess the dives, and then
feed the observed centers back into the trim sheet as a
[mystery mass](#calibrating-the-sheet-the-mystery-mass) so the next ballast
starts from reality.

---

## See also

- [Seaglider Ballasting Procedure](ballasting-procedure.md) — tank methods.
- [Seaglider Ballasting Checklist](checklists/seaglider-ballasting-checklist.md)
- [Trim & Flight Model](../../piloting/seaglider/trim-and-flight-model.md) —
  dynamic trim once the glider is flying.
- [Seaglider VBD](../../glider-components/seaglider/vbds/index.md) — counts,
  `VBD_CNV`, and why smaller counts mean more volume.
