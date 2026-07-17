---
title: Batteries
description: Seaglider lithium primary battery packs — the 24 V / 10 V and univolt 15 V architectures, the battery pack as pitch/roll trim mass, capacity and fuel-gauge parameters, why battery changes force re-ballasting and compass checks, and lithium-primary safe handling.
---

# Batteries

Seaglider batteries are unusual among glider systems in that the main pack is
not just an energy store — it **is the trim mechanism**. The large main
battery, with a brass weight bolted to its underside, is the mass that the
mass shifter slides fore/aft for pitch and rotates for roll. That double duty
means every battery change touches almost everything else: vehicle mass,
ballast, pitch/roll trim, and even the compass calibration.

!!! info "Source"
    Paraphrased from the APL-UW IOP *SGX Documentation* (v1.0, 2024), the
    Electrochem primary-lithium *Safety and Handling Guidelines*, and the
    battery MSDS/SDS sheets (UN3090/UN3091). Pack configurations vary by
    vehicle generation and build — defer to APL-UW IOP and your battery
    vendor's documentation.

---

## Pack architectures by generation

| Generation | Packs | Notes |
|------------|-------|-------|
| Legacy SG (1KA era) | One **24 V** + one **10 V** lithium primary | 24 V pack drives the motors (VBD, mass shifter) and is the moving trim mass; 10 V pack lives under the main electronics board and powers electronics |
| SG (univolt) | 15 V packs, 12.0 kg total, 0.56 kg lithium | Effective capacity ~350 Ah; the 10 V/24 V distinction disappears (but voltage-select jumpers must still be installed) |
| SGX | Three 15 V packs, 19.6 kg total, 0.91 kg lithium | Effective capacity ~575 Ah; larger forward pack plus an additional aft pack behind the mass shifter |

On all generations the main pack carries an **1100 g brass weight** on its
bottom face — the axial asymmetry that makes roll control work when the pack
is rotated (±80° on SGX, ±40° on SG).

## A battery change is a trim change

Plan for the knock-on effects before swapping packs:

- **Mass and ballast** — new packs change vehicle mass and centre of gravity.
  Re-weigh the vehicle, redo the
  [tank ballast / volmax estimate](../../../piloting/seaglider/trim-and-flight-model.md#ballasting-before-the-mission-estimating-volmax-in-a-tank),
  and enter the new mass in `sg_calib_constants.m` **before dive 1** — the
  Flight Model System bakes it in at the start of the mission.
- **Pitch trim** — `$C_PITCH` established on the old packs is unlikely to
  survive a battery change; expect to re-trim, and consider starting the
  mission with the Pitch Adjuster enabled (see
  [Trim & Flight Model](../../../piloting/seaglider/trim-and-flight-model.md)).
- **Compass** — the steel in battery cells carries its own local magnetic
  field, so swapping or even re-seating packs can shift the compass hard-iron
  calibration. Check the compass after battery work.

## Capacity monitoring

Declared capacity and cutoffs live in glider parameters; consumption is
tracked by on-board fuel gauges and, mission-long, in the vis energy and
endurance plots (projected mission duration from the observed per-dive draw):

| Parameter | Meaning |
|-----------|---------|
| `$AH0_24V` / `$AH0_10V` | Declared amp-hour capacity of each pack (univolt gliders still carry both names) |
| `$FG_AHR_24V` / `$FG_AHR_10V` (+ `…o` variants) | Fuel-gauge amp-hours consumed |
| `$MINV_24V` / `$MINV_10V` | Minimum acceptable voltage under load before the glider considers the pack exhausted |

The quoted *effective* capacities (575 Ah SGX / 350 Ah SG) are already
practical numbers, not nameplate cell capacity — endurance planning should
still leave reserve for recovery operations at the end of a mission (a glider
in recovery keeps calling on `$T_RSLEEP` until someone picks it up).

---

## Lithium-primary safety

Seaglider packs are high-energy-density **lithium primary** (non-rechargeable)
cells. The label warnings are the whole story in miniature — never:

- short-circuit,
- charge,
- force over-discharge,
- overheat or incinerate (each cell is marked with a maximum temperature),
- crush, puncture, or disassemble (never open a pack or replace a blown fuse).

!!! danger "Hot cells are a delayed hazard"
    An abused lithium cell usually does **not** vent or explode at the moment
    of abuse. It heats over seconds to *hours* until a critical temperature is
    reached. Treat any dropped, shorted, or deformed cell or pack as a
    potential hot cell: isolate it, keep people away, and monitor it — don't
    put it back in the glider or the storage cupboard to "see how it goes".

Handling practices (the largest single cause of field failures is accidental
short circuit during handling):

- Insulate conductive work surfaces; keep sharp objects off them.
- No rings, watches, or other conductive jewelry while handling packs.
- Non-conductive (or covered) tools only; trim one lead or tab at a time.
- Move cells in trays on carts rather than carrying them by hand.
- Check open-circuit voltage against the label at incoming inspection.
- Never force a pack into or out of its housing.

Storage: original packaging, dry and ventilated, ideally ≤23 °C, segregated
from flammables, **fresh cells separated from depleted ones**, sprinklers and
suitable extinguishing means available.

## Shipping

Glider lithium-metal packs ship as dangerous goods: **UN3090** (cells/batteries
packed alone) or **UN3091** (contained in or packed with equipment — i.e. in
the glider), under ICAO/IATA air and IMDG sea rules. The regulatory details,
documentation, and vessel-carriage considerations are the same as for Slocum
lithium packs — see the shared write-up on the
[Slocum primary batteries page](../../slocum/batteries/primary/index.md#shipping--transport)
rather than duplicating it here.

---

## See also

- [Trim & Flight Model](../../../piloting/seaglider/trim-and-flight-model.md) —
  re-ballasting and re-trimming after battery work.
- [VBD](../vbds/index.md) — where most of those amp-hours actually go.
