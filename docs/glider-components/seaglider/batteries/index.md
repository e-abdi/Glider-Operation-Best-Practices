---
title: Batteries
description: Seaglider lithium primary battery packs — the 24 V / 10 V and univolt 15 V architectures, the battery pack as pitch/roll trim mass, capacity and fuel-gauge parameters, how the fuel gauge estimates rather than measures, voltage cutoffs and spurious low-voltage readings, pack fuses, stretching a low battery, why battery changes force re-ballasting and compass checks, and lithium-primary safe handling.
---

# Batteries

Seaglider's main battery pack is
not just an energy store — it **is the trim mechanism**. The large main
battery, with a brass weight bolted to its underside, is the mass that the
mass shifter slides fore/aft for pitch and rotates for roll. That double duty
means every battery change touches almost everything else: vehicle mass,
ballast, pitch/roll trim, and even the compass calibration.

!!! info "Source"
    Paraphrased from the APL-UW IOP *SGX Documentation* (v1.0, 2024), the
    Electrochem primary-lithium *Safety and Handling Guidelines*, and the
    battery MSDS/SDS sheets (UN3090/UN3091), and 2017–2024 correspondence
    between Seaglider operators, APL-UW IOP, the manufacturer and service
    providers (launch refusals, voltage cutoffs at sea, early pack
    exhaustion, battery changes). Pack configurations vary by vehicle
    generation and build — defer to APL-UW IOP and your battery vendor's
    documentation.

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
  Flight Model System bakes it in at the start of the mission. **Weigh every
  pack** and write the weight, serial number and installation date on it.
  Packs of the same type differ: in one change the new main pack was 158 g
  heavier than the old one (10.28 vs 10.12 kg) and the new secondary pack
  16 g lighter.
- **Pitch trim** — `$C_PITCH` established on the old packs is unlikely to
  survive a battery change; expect to re-trim, and consider starting the
  mission with the Pitch Adjuster enabled (see
  [Trim & Flight Model](../../../piloting/seaglider/trim-and-flight-model.md)).
- **Compass** — the steel in battery cells carries its own local magnetic
  field, so swapping or even re-seating packs can shift the compass hard-iron
  calibration. Check the compass after battery work — see
  [Compass Calibration](../../../piloting/seaglider/compass-calibration.md).
  Steel parts can also pick up magnetisation from handling. Some teams have
  looked at checking packs with a gaussmeter, and degaussing them if needed,
  before they go in.
- **Gauges and capacity** — reset the fuel gauges and set the new capacity
  (see [below](#after-a-battery-change)).

A self-test right after a battery change may warn about **roll current**
("motor ran … measured … mA – problem with motor or ammeter?"). APL-UW
describes this as an out-of-date check based on an arbitrary current
threshold, and it can be ignored if the roll moves themselves are normal.

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

### The fuel gauge is an estimate, not a meter

There is no coulomb counter on the battery. The glider keeps a running total
for each subsystem and sensor: the time it was powered, multiplied by a
**preset current** from the `CURRENTS` file (values measured in the lab).
These totals are summed per battery and compared with `$AH0_24V` and
`$AH0_10V`. The *Batteries and fuel gauges* menu shows the breakdown, device
by device (pitch, roll, VBD at apogee and at the surface, Iridium, GPS,
processor, each sensor), with a total for each bus and the percentage of
capacity used.

That has two consequences:

- **Anything that draws more than its preset current is invisible.** A
  failing VBD pump that takes much longer than normal at apogee, or oil
  thickened by cold water, uses more energy than the gauge counts. So can a
  faulty component. The gauge then shows plenty left while the pack is
  running out.
- **Pack age isn't counted.** Lithium primary cells lose capacity in storage.
  The manufacturer quoted about **3% per year**, and operators have assumed
  up to 5%. A pack built from old stock, or moved from another glider with
  an unknown history, can have much less than its label says.

In one case a glider hit its 24 V cutoff with the gauge showing more than
half the pack left. Its 10 V pack was also falling quickly with a third
supposedly remaining, and energy use per dive looked normal. The most likely
explanation was an over-optimistic capacity: the 10 V pack had come from
another glider and its age was unknown. The follow-up was to measure real
current draw on the bench during simulated dives, compare it with
`CURRENTS`, and start **recording every pack's manufacture date**.

For endurance estimates, use energy-per-dive figures from dives when
everything was known to be healthy. For example, one team used only the
dives before a pump anomaly, not the whole mission.

### After a battery change

- **Reset the fuel gauges** (*Batteries and fuel gauges → Reset*). If you
  forget, the new pack inherits the old one's consumption. You can't recover
  the amp-hours used on the new pack before the reset, so estimate them from
  the bench and test time.
- **Set the declared capacity.** Set `$AH0_24V` (and `$AH0_10V` on 10/24 V
  gliders) to the new pack's capacity, less any margin you want to hold
  back. For example, one team set 310 Ah on a univolt glider rather than the
  quoted ~350 Ah. A value left over from the last mission may carry a
  different margin.
- On **univolt** gliders the packs are paralleled onto one bus. In one
  example the log reported all consumption on the 24 V line and 0 Ah on the
  10 V line. The aggregate percentage is the number to watch.
- A self-test warning **"no BATTERY file"** has been seen once, as a
  transient, just before a GPS fix. The file was present afterwards, and the
  gauges logged consumption normally after the pump was run. Check the gauge
  output after the self-test rather than assuming it is working.

## Pack voltage: what's normal

Lithium primary packs hold a nearly flat voltage for most of their life and
then drop quickly near the end. A slow, steady decline is therefore not the
normal pattern, and a sudden fall is the warning sign.

| Pack | Typical reading in service |
|---|---|
| 24 V (10/24 V gliders) | ~23–24.7 V between moves |
| 10 V (10/24 V gliders) | ~10.2–10.3 V |
| 15 V univolt | ~15.2 V fresh; 13.5–14 V after a long spell of testing and trials |

Where the voltage was measured matters. Readings dip during motor moves,
especially VBD pumps. **Dips under load matter less than a steady or sharp
fall in the unloaded value.** Each dive's log records the lowest voltage
seen and the amp-hours used, in the `$24V_AH` and `$10V_AH` lines. Plot them
over the mission rather than reading single values. Cold water also lowers
the current a pack can deliver.

## Voltage cutoffs and launch refusals

`$MINV_24V` and `$MINV_10V` are the lowest acceptable voltages. If a pack
goes below its value during a dive, the glider goes into recovery with a
code such as `VOLTAGE_CUTOFF_24V`.

The glider also **refuses to launch** if the minimum voltage seen since boot
is below the cutoff ("minimum 24V voltage … is below cutoff value…",
"Battery pack voltage too low; unable to launch!"). One short, meaningless
dip during bench testing is enough. In one case a very short pump at
16.4 V, probably a relay or FET operating, was recorded as the minimum.
**Rebooting the glider clears the recorded minimum.** Alternatively, lower
`$MINV_24V` for the launch and raise it again straight after.

### Spurious low readings

Several gliders have reported impossible values, such as a 24 V pack at
**0.5–2 V**, at random: during a motor move, or during a sampling period with
no motor moving at all. The next reading was normal again. The pattern that
identifies a measurement glitch rather than a failing pack:

- the values cluster at the normal voltage and around 1 V, with nothing in
  between;
- `comm.log` voltages and the other readings in the same dive look normal;
- there is no link to depth, motor current or pump rate.

The 10 V and 24 V measurements share a battery-monitoring relay, a buffer
amplifier and the ADC. An intermittent contact or glitch in any of these can
cause it. A fault on the high-voltage side of the main relay would be more
serious, so check the dive data for any link to pump rate or current.

The only workaround at sea is to **disable the check** (`$MINV_24V,0` is
allowed) and watch the voltages yourself in every dive's log and in
occasional capture files. Operators have kept gliders flying this way when
help was far away. When a glider is sitting at the surface in recovery because of a
spurious cutoff, `$RESUME` alone won't get it diving again. Disable the
check for that dive, then turn it back on in the next `cmdfile`. Fix it
properly at the next service.

## Fuses and paralleled packs

Each pack is fused. **Once packs are paralleled on the main board, there is
no way to tell from the glider's readings that one of them has a blown
fuse.** The bus voltage looks fine, but capacity is quietly missing. The
only check is to measure each pack **on its own, at its connector**, before
connecting them. Do this after any electrical fault that could have
overloaded the packs, such as a shorted main board. Never replace a pack
fuse yourself (see [safety](#lithium-primary-safety)).

## Stretching a low battery

When the numbers say the pack is running out before the mission is over,
the aim is to cut pumping first, since the VBD is where most energy goes:

- **Fly slower.** Lower `$MAX_BUOY` and lengthen `$T_DIVE`. The saving is
  larger than the loss of speed.
- **Accept slower climbs without extra pumps.** Widen `$W_ADJ_DBAND` and
  pump less when correcting (`$DBDW`).
- **Fix a heavy trim.** If the glider pumps on every climb, shifting
  `$C_VBD` a little toward buoyant saves those pumps.
- **Use the boost pump only near the surface.** Raise `$D_BOOST`, dive
  shallower (e.g. 100 m), and consider boost-only dives. See
  [Energy](../vbds/index.md#energy-why-the-vbd-dominates) on the VBD page.
- **Turn off what isn't essential.** Switch off PAM and optical sensors, or
  sample every other profile. Keep the CTD.

If the glider is to wait at the surface for a pickup, send fewer dive files
(`UPLOAD_DIVES_MAX,0`) and call less often. Lengthen `$T_RSLEEP`, but check
its units in your parameter reference first: operators have got this wrong.

When the glider stops because the **gauge** says the pack is exhausted, the
cause is the declared capacity, not the voltage. One team raised the
threshold to leave a 5% margin, flew energy-saving shallow dives toward the
pickup point, and let the glider drift at the surface when the current was
going the right way. They booked the recovery boat early.

## Conversions and payload voltage

- **10 V to 24 V.** Nothing stops a 10 V pack being rebuilt as 24 V to give
  more high-voltage capacity, but the pack loses amp-hours. One estimate for
  an aft pack was about 110 Ah down to 81 Ah. Such a pack is custom-built,
  not a stock part.
- **Payload supply.** Spare endcap ports can be powered from either the
  10 V or the 24 V bus. This is chosen by a **jumper on the main board**,
  not by the `.cnf` file. The voltage in the `.cnf` only tells the fuel
  gauge which capacity (`$AH0_10V` or `$AH0_24V`) to charge the sensor's
  consumption to. Ask APL-UW or your service provider for the jumper
  positions.
- **Minimum voltage for a payload.** Check what the payload needs against
  the pack's *end-of-life* voltage, not its fresh one. For example, a
  pCO₂/CH₄ sensor that stops working below 11–12 V can't run from a 10 V
  pack at all.

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
[Slocum primary batteries page](../../slocum/batteries/primary/index.md#shipping-transport)
rather than duplicating it here.

---

## See also

- [Trim & Flight Model](../../../piloting/seaglider/trim-and-flight-model.md) —
  re-ballasting and re-trimming after battery work.
- [VBD](../vbds/index.md) — where most of those amp-hours actually go.
