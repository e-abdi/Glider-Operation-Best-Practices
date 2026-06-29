---
title: O-Rings
description: The Slocum hull and component O-rings: G2 single-seal vs G3 double-seal part numbers and sizes, the full spares kit, approved lubricants (Parker O-Lube vs Molykote and the community debate), inspection and replacement, sealing-surface scratches and the sanding controversy, lubricant dry-out, vacuum loss, and assembly tips.
---

# O-Rings

O-rings are the glider's primary defense against flooding. Every hull joint,
plug, and through-hull fitting relies on a correctly sized, clean, lightly
lubricated O-ring seated in an undamaged groove against an undamaged sealing
surface. Most Slocum leaks are **not** main-hull O-ring failures — they're
bulkhead connectors, instrument seals installed with the wrong O-ring, or loose
through-hull fittings — but the main-hull O-rings are what you inspect and
replace most often, so getting their part numbers, lubricant, and handling right
is foundational.

!!! info "Source"
    Paraphrased from the *Slocum G3 Glider Maintenance Manual* (Rev. A, "O-ring
    Maintenance", "Main Hull Double O-ring Seals", "Main Hull O-Rings"), the
    *Slocum Glider Operators Manual*, the Teledyne Webb Research user forum, and
    the UG2 community Slack. Part numbers and prices change — always confirm the
    current part numbers with `glidersupport@teledyne.com` and defer to the
    official Teledyne documentation for your specific glider.

---

## Single seal (G2) vs. double seal (G3)

A defining hardware difference between the platforms:

| | G1 / G2 | G3 (and late/upgraded G2 with stiffening rings) |
|---|---|---|
| Hull sealing surfaces | **One** O-ring | **Two** O-rings (dual seal) |
| Main hull O-ring P/N | **G-024** (`2-265-N674-70`) | **304697** (`2-264`, BUNA) |
| O-ring size | 2-265, nitrile (NBR), 70 durometer | 2-264, BUNA, ~60–65 durometer |
| Why | Standard single seal | More sealing-surface area → reduced leak probability |

- The double seal lengthened the carbon-fiber hulls by **0.5"** versus the G2,
  raising standard-config G3 displacement to **~57.7 L** and lengthening the
  internal [tie rod](../tie-rod/index.md) — **G2 hulls will not fit a G3.**
- **Early G3s shipped with the G2-size ring** (`2-265`) and were notoriously hard
  to open and close; TWR later issued the correct smaller **`2-264`** double-seal
  ring. If a G3 is a "fight for your life" to assemble, **check you're on the
  right O-ring** first.
- The G2 main hull O-ring (`2-265`/N674-70) is **nitrile, 70 durometer**, ID
  7.734", width 0.139". The vacuum/evacuation boss plug O-ring is also nitrile
  70-durometer: **`3-904`** (G-030), ID 0.351", width 0.072".

!!! note "Teledyne won't publish full seal specs"
    Operators have repeatedly asked TWR for G3 groove dimensions/tolerances (e.g.
    to build their own pressure-test end caps) and been declined. Identify the
    seal by **part number**, not by trying to reverse-measure the groove with
    shop calipers.

---

## Part numbers — full spares kit

The complete O-ring spares kit is **ASSY 4424** (a smaller kit, **ASSY 4423**,
covers just the two most-used seals). Contents (part numbers are stable; prices
are illustrative, ~2012):

| TWR P/N | Size / material | Where used |
|---|---|---|
| **G-024** | `2-265` N674-70 | **Main hull** (G2 single seal) |
| **304697** | `2-264`, BUNA, ~65D | **Main hull** (G3 double seal) |
| **G-030** | `3-904` N674-70 | MS vacuum / evacuation boss plug (also G1 unpumped CTD piston seal) |
| **B1-132** | `2-007` N674-70 | B1 |
| **G-022** | `2-018` N674-70 | 7/8" |
| **G-027** | `2-115` N674-70 | 7/8" tail tube |
| **G-1214** | Parker `5-712` | — |
| **G-1331** | `2-141` N674-70, NBR | — |
| **G-1508** | `2-161` N674-70, NBR | — |
| **G-607** | `5-105` N674-70 | — |

!!! tip "Order by part number and keep a kit aboard"
    Wing-rail weight O-rings (~size 010) and the small vacuum-plug / bullet-weight
    O-rings are the ones that **dry out and crumble** first — keep spares. A full
    O-ring spares kit is a standard item on deployment-spares lists.

---

## Lubricant: what's approved, what the field actually uses

The **official** lubricant for main-hull O-rings and sealing surfaces is
**Parker O-Lube 884-4** (`3135-LUBE` / `3M-LUBE`, "Parker Fibrous O-Lube 884-4",
a petroleum naphthenic oil + barium soap), available from the TWR forum or by
request from glider support. The maintenance manual procedure is simply: inspect,
lubricate with Parker O-Lube, install, seat properly.

For **electrical connectors** the rules differ — don't cross them:

| Surface | Approved lubricant | Avoid |
|---|---|---|
| Main hull O-rings & sealing surfaces | **Parker O-Lube 884-4** | — |
| Impulse connectors | Silicone lubricant | **Any silicone spray containing acetone** (breaks down the connector) |
| Subcon(n) connectors | **Molykote 44** (Dow Corning) | — |
| Dummy / green plugs | O-Lube or silicone spray | — |
| Bellofram / pump rubber | **Molykote 316** or 3M Silicone Lubricant | Silicone spray with acetone |

!!! warning "The Parker O-Lube dry-out problem (well known in the fleet)"
    A recurring community complaint: **Parker O-Lube dries out** — after a long
    mission, or even just sitting in a dry/air-conditioned shop, it turns into a
    **crusty white gunk** in the O-ring grooves that has to be scraped out, and is
    "completely non-lubricating." Notes from the community:

    - Several operators prefer **Molykote / Dow Corning High-Vacuum Grease**
      (silicone) and report TWR has been "OK with it" — but it is silicone, which
      **migrates onto everything** and **must never get on acoustic transducers**.
    - Some report Parker's **basic** O-Lube is hydrocarbon-based and **not
      technically compatible** with the glider O-ring material (slightly degrades
      it); they suggest Parker **Super O-Lube** (silicone) instead — though it's
      "so runny."
    - Many stay on the standard Parker O-Lube purely to **avoid doing anything
      non-standard** that could be blamed for a leak, and simply **replace dried
      O-rings** rather than chase a better grease. A reasonable default.

---

## Inspection & replacement

- **Inspect every O-ring** for cleanliness, nicks, slices, dents, and cracks
  before each deployment; inspect the **sealing surfaces** for scratches and
  defects under good light (a **flashlight** raking across the surface reveals
  scratches a fingertip misses).
- **Replace as needed before every deployment.** Many teams running single-use
  primary batteries **replace all hull O-rings every time they open the glider**
  (i.e., every mission). With **rechargeable** G3s that can recharge/download
  without opening, a common plan is to open **once a year** to inspect, replace
  hull O-rings, and test batteries.
- **Cleanliness is everything.** Foreign particles in the gland cause leaks and
  shorten O-ring life. Be "paranoid": gloves, hair retained, clean bench. The
  vast majority of well-handled hull O-rings simply don't leak.
- **Assembly** (from the Parker handbook): keep installed ID stretch **under 5%**,
  don't exceed ~25–50% elongation reaching the groove, and **never twist** the
  O-ring into place. Seat it fully before drawing the joint closed.

!!! danger "Small O-rings dry out and fall apart in storage"
    The smaller O-rings — vacuum plug, bullet weights, wing-rail weights — are
    prone to **drying out, cracking, and crumbling** while a glider sits on the
    shelf in a dry shop. Check them as part of every pre-deployment workup; some
    teams have moved wing-rail-weight O-rings to **silicone** to resist
    drying/cracking.

---

## Sealing-surface scratches — the sanding debate

Carbon-fiber hull sealing surfaces do pick up fine scratches (from sharp edges
around ballast bottles, sliding batteries in/out, corner bumpers on the
mainboard). What to do about a scratch that crosses the O-ring band is **genuinely
contested** in the community — present both views and decide deliberately:

=== "The case for polishing them out"

    Several experienced groups (e.g. Rutgers) **wet-sand minor scratches out**
    semi-regularly:

    - Use **fine paper, ~1500–2000 grit**, wet.
    - Sand a **large area** (roughly half the hull, scratch centered) to preserve
      roundness — don't just spot-sand.
    - The "**fingernail catch**" test: if a dragged fingernail catches in it and
      it sits near the sealing surface, sand it; a few minutes to a few sessions
      per scratch.
    - Prevention: wipe a **thin layer of O-Lube on the hull** when sliding
      batteries in/out as a protective film.

=== "The case against sanding by hand"

    Pressure-seal practice says sanding an O-ring sealing surface **by hand is a
    big risk**:

    - O-ring standards allow only **~0.003"** of depression tolerance — and 0.003"
      is **nearly invisible** to the eye, so it's easy to remove too much and put
      the hull **out of round**.
    - The advice: **don't sand a hull yourself** unless you have a lathe/mill that
      can hold the hull diameter and remove controlled tolerances.
    - The "fingernail catchiness" test is **subjective** (depends on pressure,
      nail length, sensitivity).

!!! note "Webb's position and a reality check"
    TWR's guidance: **replace a hull if carbon fibers are exposed**; minor paint/
    finish chips (no damage felt in the grey/white material) just need touch-up
    (epoxy/siloxane paint, or even nail polish in a pinch). Teledyne has also
    provided some users written instructions on how to "**polish**" a sealing
    surface. Reality check from the field: one glider that had scratches polished
    per those instructions **still wouldn't hold vacuum in the shop** — so a
    visible scratch is **not always the actual leak path**. Diagnose before you
    sand.

---

## Vacuum, leaks & testing

The internal vacuum is your standing leak indicator — **always monitor it before
launch** (less vacuum than expected = a leak; **positive** pressure can mean
dangerous gas accumulation). It **fluctuates with temperature**, so log
temperature alongside vacuum.

- **Never power a shallow glider without a vacuum.**
- A reasonable "sealed" bar: vacuum **stable for 1–2 weeks** (recording
  temperature). Deploy a glider sealed only ~24 h **only in an emergency**.
- **Slow loss over months** is common even on a well-sealed glider on the shelf —
  not necessarily a real leak. But re-verify, and **inspect/replace O-rings**
  before redeploying after long storage. A brand-new factory-sealed, helium-tested
  G3 can still slowly bleed down on the bench; common real culprits found include
  **loose through-hull fittings** (e.g., a nose altimeter cable pass-through that
  needed a ¼ turn) as much as the hull O-rings themselves.
- **Don't over-pull the vacuum** to mask a marginal seal — excessively high
  vacuum can pull bubbles out of the ballast-engine oil.
- **Leak testing** is hard: vacuum-and-wait can take months to reveal a slow leak,
  and gliders that hold vacuum for months on the shelf sometimes leak as soon as
  they're in the water. Teams use sectional pressure monitors, pressure chambers
  (commercial or DIY McMaster-fitting builds), or helium leak detectors (accurate
  but expensive). No method is foolproof — **cleanliness and inspection** remain
  the best defense.

---

## Assembling the double-seal G3

A practical pain point worth its own note — closing a G3 against two O-rings:

- Make sure you're on the **correct `2-264` G3 ring**, not the larger G2 `2-265`.
- **Manually push the hull sections fully over the O-ring seals** before relying
  on the [tie rod](../tie-rod/index.md) to draw them together — tie-rod lengths
  vary (especially with stack-on bays like an AD2CP), and short ones won't "catch"
  until the sections are nearly home.
- **Pulling a light vacuum during assembly** helps seat the joint the last bit
  (many teams do this).
- Keep good **PEEK hull-opening tools** (they outlast the soft black ones but
  still round off); some teams make thin plastic wedges to crack a stubborn,
  long-stored hull — **wedge away from the O-ring sealing surface**, never into
  it.

---

## Quick reference

| Item | Value |
|---|---|
| Main hull O-ring — **G2 single seal** | **G-024** (`2-265-N674-70`, nitrile 70D) |
| Main hull O-ring — **G3 double seal** | **304697** (`2-264`, BUNA ~65D) |
| Vacuum / boss plug O-ring | **G-030** (`3-904` N674-70) |
| Full spares kit | **ASSY 4424** (small: **ASSY 4423**) |
| Hull O-ring lubricant | **Parker O-Lube 884-4** (`3135-LUBE`) |
| Impulse connectors | Silicone lubricant — **no acetone** |
| Subcon connectors | **Molykote 44** |
| Bellofram / pump rubber | **Molykote 316** / 3M Silicone — no acetone |
| Scratch sanding (if you must) | Wet, **1500–2000 grit**, large area for roundness |
| "Sealed" criterion | Vacuum stable **1–2 weeks**, temperature logged |

---

## See also

- [Tie Rod](../tie-rod/index.md) — what draws the O-ring joints closed, and why
  G3s can be hard to assemble.
- [Pumps](../pumps/index.md) — Bellofram/oil-bladder rubber care and storage
  (related lubricant rules).
- [Maintenance overview](../../../maintenance/guides/overview.md) — where O-ring
  inspection fits in the service schedule.
