---
title: Electronics
description: Seaglider main electronics — Rev B (TT8) and Rev E (ARM) main boards, where settings live, backing up and restoring parameters, replacing a main board, TT8 failure modes, Rev E upgrades, 10/24 V to 15 V conversions, bench power and brown-outs, CF card corruption, reboots and $RELAUNCH, and handling the boards safely.
---

# Electronics

The main electronics board runs everything on a Seaglider: the motors, the
VBD, navigation, comms, the pressure sensor, and every sensor port. Two
generations are in service:

- **Rev B** — built around a **TT8** processor with a Persistor CF2 and a
  CompactFlash card. Its firmware lineage is 66.x.
- **Rev E** — an **ARM**-based board with an SD card. Its firmware lineage
  is 67.x. Existing gliders can be upgraded to it.

Most day-to-day differences between the two (firmware files, menus,
parameters, basestation versions) are documented by APL-UW IOP. **For
firmware versions, release notes and update procedures, use the IOP pages
rather than this wiki:**

- [Seaglider firmware (seaglider.pub)](https://seaglider.pub/firmware/index.html)
- [Rev E software notes (APL-UW IOP, PDF)](https://iop.apl.washington.edu/iopsg/RevE_software_notes.pdf)

This page covers the hardware side and the lessons from operating and
servicing both boards.

!!! info "Source"
    Paraphrased from 2016–2024 correspondence between Seaglider operators,
    APL-UW IOP, the manufacturer and service providers (main-board
    failures and replacements, Rev E upgrades, CF card corruption, 15 V
    conversions). Board revisions and factory configurations vary — defer
    to APL-UW IOP and your glider's documentation.

---

## Where the settings live

A glider's configuration is split between two places, and mixing them up is
the most common mistake when a board is replaced:

| Stored in the board's non-volatile memory | Stored on the card |
|---|---|
| All parameters (`$C_VBD`, `$PRESSURE_SLOPE`, `$DEVICEn`, …) | Sensor and logger `.cnf` files |
| Password, `telnum`, `altnum` (the "utility" settings) | `tcm2mat` compass calibration |
| Hardware configuration (which sensor is on which port) | `CURRENTS` and `BATTERY` files |
| | `capvec`, bathymetry maps, mission control files |
| | Logs, capture files, and on Rev B the firmware itself (`main.run`) |

**Moving the card to a new board does not move the settings.** They are only
on the card if someone saved them there deliberately.

### Back up before you change anything

- **Save the parameters to a file** (`param/save` from the main menu) before
  any firmware change and before any board work. Different firmware builds
  can change NVRAM contents, and parameter sets differ between versions. A
  saved file lets you restore everything with `param/load`.
- **Keep a parameter dump with every glider's records.** A self-test capture
  or a dive log also lists every parameter. It can be edited down to a
  load file if the board dies without a backup.
- **Try new firmware without committing to it.** On Rev B, APL-UW's advice
  for running different firmware temporarily (for example, to update the
  GPS) is to upload it under another name, such as `glider.run`, and start it
  from the top-level `PicoDOS>` prompt. Leave `main.run` untouched. A reboot
  returns to the original firmware. Restore the saved parameters afterwards.

## Replacing a main board

When a board is swapped, work through the list rather than trusting that
"everything carried over":

1. **Load the parameters** from the saved file, or from an edited log.
   Compare them with the last known-good parameter set, line by line.
2. **Re-enter the utility settings**: password, `telnum`, `altnum`.
3. **Pressure sensor**: check `$PRESSURE_SLOPE` and the gain, then redo the
   sea-level zero. See [Pressure Sensor](../pressure-sensor/index.md).
4. **Internal pressure**: zero it at atmospheric pressure before pulling
   vacuum.
5. **Sensors**: make sure the `.cnf` files are in the board's library and
   every sensor slot is configured. On Rev E, *none* of the serial sensors
   are built in. Every one needs its `.cnf`. See
   [Sensor Configuration](../sensors/index.md).
6. **Compass**: confirm the compass model and port. After some firmware
   updates the compass has to be reinstalled
   (`param/config/compass`).
7. **Fuel gauges**: check that `CURRENTS` and `BATTERY` are present and that
   consumption is being counted. See
   [Batteries](../batteries/index.md#the-fuel-gauge-is-an-estimate-not-a-meter).
8. **Run a full self-test** and compare it, section by section, with the
   last good self-test from before the swap.

The same list applies when only the TT8 is replaced on a Rev B board. The
parameters and the utility settings have to be copied across.

## Rev B: the TT8 and its failure modes

The conductivity and temperature frequency signals from the CT sail go
**directly to timer (TPU) pins on the TT8**. Damage to those I/O lines gives
the classic board-level CT fault:

- the CT reports **zero counts**, or values that jump between sensible,
  wildly wrong and zero, with nothing moving;
- a new or freshly calibrated CT shows the same fault;
- the fault **disappears when the main board is swapped** with one from
  another glider.

In one case the manufacturer couldn't reproduce the fault on the bench, so
the board went back to the owner as untrustworthy. In another, every other
cause was ruled out: firmware, ribbon cable, CT boards and supply voltage.
Damaged TT8 I/O lines have been seen before, sometimes with no known root
cause. Before blaming the board, APL-UW suggests powering the C and T boards
directly, disconnected from the tailboard, and checking for a clean frequency
output from each.

**TT8s are no longer available from the manufacturer.** A failing Rev B
board may therefore mean a **Rev E upgrade** rather than a repair. Weigh that
cost early when planning a refurbishment of an older glider.

## Rev E upgrades in practice

Upgrading a Rev B glider to Rev E is a board-and-wiring job plus a software
migration. Field upgrades have run into:

- **Kit differences.** Upgrade kits have arrived without some adapter
  cables, including the altimeter adapter and the internal shorting-plug
  connector, and without some jumpers. Some cables have been too short to
  reach their new headers. Check the kit against the procedure before the
  glider is opened.
- **Port assignments.** The transponder/altimeter UART and power assignments
  were not documented in one upgrade procedure. The glider pinged nothing
  until the right port was found. Ask APL-UW for the port and mux map.
- **Basestation.** Rev E needs a newer basestation than most Rev B
  installations run. Check this before the first sea trial. See the IOP
  links above.
- **Sensor integration changes.** Every serial sensor needs a `.cnf` file.
  The factory Rev E builds don't use SciCon. Some `.cnf` strings that worked
  on Rev B can crash Rev E firmware. See
  [Sensor Configuration](../sensors/index.md).
- **Pressure sensor.** A Paine sensor does not work on a Rev E board. Fit a
  Kistler as part of the upgrade. See
  [Pressure Sensor](../pressure-sensor/index.md#paine-sensors-on-rev-e).

## 10/24 V to 15 V conversions

Converting a 10/24 V glider to the univolt 15 V architecture changes more
than the battery. APL-UW's list of what has to change:

- **Motors**: boost pump, main pump, pitch and roll.
- **Solenoid coil** (the Skinner valve).
- **Phone DC-DC converter** and **RF relay**. These may be fine, but need
  checking.
- **Optional**: a resistor change so that the external-power relay picks up
  reliably, and 15 V-specific transponder magnetics. APL-UW has done
  conversions without either and saw no real difference.

The VBD assembly itself is built for one architecture. See
[VBD](../vbds/index.md) and [Batteries](../batteries/index.md).

## Bench power and brown-outs

- **Give the bench supply enough current.** A supply limited to 1.5 A let the
  battery bus sag below **4 V** while the main pump ran. The processor
  browned out while writing to the card and left corrupt, undeletable files
  that filled it. At about 3 A the same test only sagged to about 11 V.
  Low supply voltage also makes the pumps look slow, which can send you
  hunting for a VBD fault that isn't there.
- **Run at least one self-test and a simulated dive on the glider's own
  batteries** before launch. External power hides problems and creates
  others.
- **The powered comms cable has over-voltage protection.** It stops the
  glider powering up if the 10 V and 24 V leads are swapped. On some
  gliders this circuit made start-up on external power slow and erratic,
  sometimes dropping into the low-level TOM8 prompt, while start-up on the
  batteries was normal. The manufacturer said this was harmless. The real
  rule is: **never reverse the supply leads.**

## Rev B CompactFlash card

- **Watch the used space.** Corrupt or runaway files can fill the card.
  Once the card is full or the file structure is damaged, files may not
  delete or transfer with the normal tools. A glider in that state may keep
  flying as long as `main.run` is intact, but it stops writing new data.
- **Reformatting means opening the glider.** Before you do, gather the files
  you'll need to put back:
  - the firmware (`main.run`);
  - `capvec`;
  - every `.cnf` file;
  - the `tcm2mat` compass file;
  - `BATTERY` and `CURRENTS`;
  - bathymetry maps;
  - SciCon files such as `scicon.ins`, if used.

  Then reinstall the logger and sensor configuration. The sensor
  configuration lines in an old self-test capture show how it should look.
  After one reformat, the science sensors returned empty files until the
  SciCon files were put back.
- **Restore the `BATTERY` file too.** Without it the fuel gauge starts from
  zero and the consumption to date is lost.

## Reboots and `$RELAUNCH`

`$RELAUNCH` decides what the glider does after an unexpected reboot. The
default, 0, puts it into **recovery**. With 1 it carries on diving. The
manufacturer's view is that a random reboot at sea deserves investigation
before the glider dives again, hence the conservative default. The value
changes by itself: it becomes 4 while the glider is in recovery, and goes
back to the original setting when it leaves. So seeing 0 → 4 → 0 in capture
files, for example while trimming at the start of a mission, is normal.

## Handling the boards

- **Disconnect the battery from the main board first**, before you lift,
  probe or unplug anything. Removing the shorting plug or external power is
  not enough on its own.
- **Keep the insulating film under the main board in place.** In one case
  the film shifted during testing and the underside of the board touched the
  chassis. It gave off a puff of smoke and never booted again. That
  happened even with external power and the shorting cable removed.
- **Check the fasteners on the small board under the main board.** One was
  found completely loose, free to come off and rattle around the forward
  section during a mission.
- **Connectors:**
  - The 0.1-inch MTA connectors are reliable when made correctly. They are
    insulation-displacement types, so don't strip the wire first.
  - Never tin the ends of crimped wires. The solder makes a hard spot where
    the strands work-harden and break.
  - Poorly mated connectors on older gliders have caused intermittent
    pitch-sensor dropouts as cable tension changed.
  - A bad Molex connection caused GPS failures on another group of gliders.
- **If a fault reproduces in the field but not on the bench** (at depth, in
  the cold, at certain attitudes), a bench poke-and-prod test proves little.
  Log the symptom against depth, temperature, pitch and roll from the dive
  data before replacing parts.

---

## See also

- [Pressure Sensor](../pressure-sensor/index.md) — the analog front end
  on the main board and what to redo after a board swap.
- [Sensor Configuration](../sensors/index.md) — serdev/logdev `.cnf` files,
  the sensor library, and Rev E specifics.
- [Comms, GPS & Basestation](../comms/index.md) — modem, antenna and GPS
  faults.
- [Batteries](../batteries/index.md) — pack voltage measurement shares
  the board's relay and ADC.
