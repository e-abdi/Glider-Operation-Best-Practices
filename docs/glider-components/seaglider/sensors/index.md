---
title: Sensor Configuration
description: Getting science sensors working on a Seaglider — serdev vs logdev vs SciCon, the .cnf library and sensor slots, installing and fixing .cnf files remotely, basestation handling (.sensors, sg_calib_constants, CTD types), and per-sensor notes for the CT sail, GPCTD, Aanderaa optodes, WET Labs ECO sensors, RBR legato, PAR sensors and the AD2CP.
---

# Sensor Configuration

A Seaglider talks to its science sensors in one of three ways. Each needs
configuring on the glider **and** on the basestation, and most "sensor
failures" in the first days of a mission are really configuration problems
on one side or the other.

!!! info "Source"
    Paraphrased from 2016–2024 correspondence between Seaglider operators,
    APL-UW IOP, the manufacturer, sensor manufacturers and service
    providers (sensor integrations, `.cnf` debugging, CTD and optode
    faults, basestation processing). Firmware behaviour differs between
    Rev B (66.x) and Rev E (67.x) builds and between manufacturer and APL-UW
    firmware — see [Electronics](../electronics/index.md) and the IOP
    firmware pages.

---

## Three ways in

| Route | What it is | Typical use |
|---|---|---|
| **Built-in drivers** | Drivers compiled into the firmware (e.g. the SBE CT sail) | The CT, and on Rev B some standard optodes and ECO sensors |
| **serdev** | A generic serial driver driven by a `.cnf` text file: power the sensor, (optionally) send a command, parse the reply into columns | Simple sensors that power up and answer: optodes, ECO pucks, PAR |
| **logdev** | A logging-device driver, also `.cnf`-driven, for instruments with their own memory that log internally and hand back files | GPCTD, PAM recorders, AD2CP, UVP6, echosounders, RBR legato (in some integrations) |
| **SciCon** | A separate science controller (Rev B builds) that runs its own sensors to its own schedule (`scicon.sch`) | Multi-sensor payloads on manufacturer-built gliders |

On **Rev E, none of the serial sensors are built in**: everything goes through
serdev or logdev with a `.cnf` file. A self-test that lists only the CT after
a board change is the typical symptom of missing `.cnf` files. The
manufacturer's factory Rev E builds don't use SciCon.

For sensors too complex for a `.cnf` (odd protocols, hex output, lots of
data), operators have used a small interface board between the sensor and
the glider (e.g. a "Smart Cable"). The glider then talks to a simple serial
device and the board handles the sensor.

## The library and the slots

Two separate things have to be set up, and they're independent:

1. **The library** — which `.cnf` files the glider knows about. Add, list and
   remove with `seradd` / `serlib` / `serdel` (serial sensors) and
   `logadd` / `loglib` / `logdel` (loggers), under `param/config`.
2. **The slots** — which sensor is attached to which port. These are the
   `$DEVICEn` and `$LOGGERDEVICEn` parameters, set with *Configure sensor* /
   *Configure logger sensor* in `param/config`.

A sensor only appears as a choice in step 2 once its `.cnf` is in the
library. If *Configure sensor* offers only the CT and "not installed", the
library is empty, not the firmware. Setting `$DEVICEn` or `$LOGGERDEVICEn`
directly (by hand or in a `cmdfile`) runs the same setup as the menu, but
only works if the `.cnf` is already in the library. Otherwise the glider
rejects or resets the value.

!!! warning "File names must be lower case"
    Give the `.cnf` file name in **lower case** when you add it. An upper-case
    name loads into the library but never appears in the list of devices you
    can configure. If that has happened, delete it (`serdel`) and add it again
    in lower case.

### Getting files onto the glider

- On the cable: from PicoDOS, transfer with XMODEM (`xr`) and then run
  `strip1a` to remove the transfer padding. Make sure the target isn't
  read-only.
- If XMODEM keeps failing ("0 files transferred"), try **YMODEM** (`yr`).
  In one case repeated `xr` attempts failed and `yr` worked first time.
- **Rename the old file before overwriting**, and check that the new one
  arrived before you delete anything. One failed transfer after a rename
  left the glider with no calibration file at all.
- **Remotely**, the same menu actions can be put in `pdoscmds.bat`, for
  example `menu param/config/loglib` or
  `menu param/config/logadd device=0 file=gpctd.cnf`. Send **one command per
  call** and read the result before sending the next.

## `.cnf` gotchas

- **Trailing blank lines matter.** An optode `.cnf` with *two* blank lines at
  the end returned "got 1 of 5 columns", then "got 0 of 5 columns", even
  though the sensor streamed good data in direct comms. The fix was exactly
  **one** blank line at the end.
- **Start-up chatter.** A sensor that prints a banner or mode line on power-up
  (e.g. "MODE RS232") can confuse the parser. Check the sensor's own
  configuration in direct comms, not just the `.cnf`.
- **The prompt must match.** The glider waits for the prompt string in the
  `.cnf`. If the sensor's settings have changed (for example, a GPCTD with its
  "executed" tag turned on), the glider never sees the prompt and reports "no
  prompt detected". Either change the sensor setting or change `prompt=` in
  the `.cnf`.
- **Warm-up and timeouts.** Too short a warm-up gives empty first samples.
  You can adjust it without editing the file (`edit warmup=…` in the sensor's
  hardware menu).
- **Don't ask a logger for depth on early Rev E firmware.** On one Rev E
  build, a logdev `.cnf` that sent the depth (`%D`) in its start/stop strings
  made the glider crash and reboot (a bus fault) the moment the string was
  sent. Removing `%D` fixed it.
- **Power cycling.** Some sensors must not be powered off between samples
  (the RBR legato is one). Newer serdev drivers have `.cnf` options for this
  (`power-policy`, and `cycles` for frequency-counting instruments). They
  have been in APL-UW's Rev E firmware since about 2020 but not in Rev B
  builds. On Rev B, run such a sensor as a logdev instead, or slow sampling
  right down.
- **`voltage=` and `current=` are bookkeeping.** They tell the fuel gauge
  which battery to charge the sensor to, and how much. They don't change the
  supply. See [Batteries](../batteries/index.md#conversions-and-payload-voltage).
  A `CURRENTS` file entry is optional if the `.cnf` has a current value.

## The basestation side

The glider can log a sensor perfectly and the basestation can still drop it
on the floor.

- **The CTD is special.** The basestation needs to find one of the CTD types
  it knows, in the units it expects. Otherwise most processing stops ("No CT
  data found"), including the flight model and the derived quantities.
  Basestation2 knows the Seabird CT sail on the glider, and the GPCTD and
  legato only via SciCon. An **RBR legato as the main CTD on a serial port**
  needs **basestation3**, `sg_ct_type = 4` and a `legato_sealevel` value
  (the sea-level pressure reading from a self-test) in
  `sg_calib_constants.m`.
- **Other sensors** need a matching `.cnf` in the basestation's `Sensors`
  directory (listed in `.sensors`) to reach the NetCDF files with proper
  names and metadata. Without it they may appear in the `.eng` files but not
  in the `.nc`.
- **Column names differ between sensor builds.** A WET Labs puck whose
  columns didn't match the calibration names was fixed with a column remap
  in `sg_calib_constants.m` (`remap_wetlabs_eng_cols = "…"`). Another team
  corrected a mislabelled column directly in the `.eng` files before
  reprocessing.
- **Send the basestation log with any processing question.** The error lines
  ("No handler found for columns…", "Unknown nc metadata…") usually say
  exactly what's missing.

## Per-sensor notes

### CT sail (SBE)

- **A step change at apogee** (for example, +10 °C and −10 PSU from one dive
  on, with unrealistic density afterwards) has been traced to **water
  entering the thermistor**: micro-leaks where the cap is welded onto the
  thermistor tube. Sea-Bird resumed leak-testing thermistor tubes after
  these cases. A thermistor wire broken off by over-twisting the C and T
  wiring was found on another sail.
- **Zero or erratic counts on a CT that tests fine elsewhere** point to the
  main board. See [Electronics](../electronics/index.md#rev-b-the-tt8-and-its-failure-modes).
- **Coefficients on the glider differ slightly from the cal sheet.** That's
  normal. The glider's floating-point precision can't hold every digit, and
  it only uses the values for onboard density. Processing uses
  `sg_calib_constants.m`.
- **The plug seals.** The CT plug uses a -012 o-ring on the bore (with a
  backup ring) and a -016 on the face.

### GPCTD (Sea-Bird pumped CTD)

- **Prompt and output format.** If the GPCTD's "executed" tag has been turned
  on (e.g. by using Sea-Term), the glider can't find the prompt. Turn the tag
  off, or change the prompt in the `.cnf`. The output format also has to be
  what the `.cnf` expects (hex).
- **Garbage at the end of the first half-profile.** A known GPCTD behaviour
  puts about 20 samples of garbage at the end of the dive (`a`) file. On a
  short deck dive the whole dive file can be nonsense while the climb looks
  fine. Don't judge a GPCTD on a deck dive.
- **Configuration can silently disappear.** On one glider `$LOGGERDEVICE2`
  was found disabled after a firmware swap, so no CTD files were made
  ("No pumped CT data found"). Setting the parameter again, via the menu or
  the `cmdfile`, restored it. Always save and restore parameters around
  firmware changes.
- **Clock-sync errors** during a self-test have been intermittent. Timing
  changes in the `.cnf` can help.
- **Dive and climb temperatures disagree by degrees** → suspect the pump.
  The pump's energy use can be checked roughly by comparing the `BATTERY`
  file between two dives.
- **Connectors.** Corroded IE55 pins on a GPCTD had to go back to Sea-Bird.
  The small IE55 bulkheads are not a field repair.

### Oxygen optodes (Aanderaa)

- **4330F vs 4831F.** The two are essentially the same sensor with a different
  interface. The 4831F has a standard wet-mateable bulkhead (and an
  analog output option). The 4330F's sensor foot needs the manufacturer's own
  cable plug, so a home-made cable is much harder. For a Seaglider, the
  4831F is the simpler choice.
- **Storage.** Keep the foil **wet and dark**, with water in the cap. If it
  has been stored dry, hydrate it for about 24 h before calibrating or
  deploying.
- **Flooded cables and connectors** are a common cause of optodes dying
  mid-mission.

### WET Labs / Sea-Bird ECO sensors (BBFL2, SeaOWL)

- Channel wavelengths and names differ between models and builds. Check the
  characterisation sheet and set the column mapping to match.
- **Calibration sheets go missing** with second-hand and refurbished
  gliders. Sea-Bird can supply them by serial number, but it takes time.
- For a deck check, leave the sensor on the glider and run it through the
  glider (a bucket underneath works). Taking it off needs its own cable and
  software.

### RBR legato

- Can run as a serdev or a logdev, depending on firmware and integration.
  The `.cnf` for one won't work for the other.
- Needs basestation3 to be processed as the main CTD (see above).
- Reported issues on manufacturer-integrated gliders:
  - power use not being counted by the fuel gauge;
  - CTD data repeated several times in the NetCDF files;

### PAR sensors (Biospherical)

- The older QSP2150 has a simple serdev `.cnf` (one value per sample).
- The newer **MPE-PAR** outputs hexadecimal at 115200 baud, free-running at
  about 1 Hz once powered, and applies no calibration itself. Log the raw hex
  and convert afterwards: subtract a dark reading, divide by the calibration
  coefficient. Also log the internal temperature, which is useful for
  correcting the dark offset.
- A cosine (flat) collector lets in more light than a spherical one, but is
  more sensitive to the glider's pitch and roll.
- **Don't try to convert a digital unit to analog** by flipping its internal
  switch. The analog mode is logarithmic, needs different firmware settings,
  and needs recalibration.

### AD2CP (Nortek)

- Connected either through SciCon (APL-UW's usual way) or as a **logdev**.
  The logdev approach uses a `.cnf` plus an `ncp_go` command file, runs at
  38400 baud, and returns the AD2CP's own averaged telemetry file as the
  real-time data.
- **Beam switching.** Normally the instrument switches beams by pitch when
  configured for glider use. One manufacturer-integrated glider sampled the
  wrong three beams on dive and climb. The workaround was to sample all four
  beams and sort them out afterwards.
- Converting the `.ad2cp` files needs Nortek's tools, and beam geometry has
  to be checked against the configuration.

### SciCon

- **Start-up handshake.** The glider sends a "log start" command and expects
  a reply and the SciCon prompt within about 1.5 s. It tries three times. On
  one glider, after 400+ good dives, SciCon began missing the handshake: dive
  data went missing and climb data was labelled as the dive. Turning on
  SciCon debug capture (`capvec HSCICON DEBUG BOTH` in `pdoscmds.bat`) changed
  the timing enough to make it work. The team left debug on for the rest of
  the mission.
- A **0 interval in `scicon.sch`** skips that sensor in that depth bin.
- `SENSOR_SECS` in the log is SciCon's total on-time, not per sensor. SciCon
  measures per-sensor power itself and reports it to the glider's `BATTERY`
  file.
- The auxiliary compass on SciCon provides **pitch and roll only**. See
  [Compass Calibration](../../../piloting/seaglider/compass-calibration.md#auxiliary-and-spare-compasses).

### Removing a sensor

When a sensor comes off the glider, **remove it from the configuration too**
(set its slot to "not installed"). Otherwise the glider keeps trying to talk
to it, and the self-test and the fuel gauge are wrong.

---

## See also

- [Electronics](../electronics/index.md) — board swaps, Rev E, and why
  sensor configuration has to be redone.
- [Compass Calibration](../../../piloting/seaglider/compass-calibration.md).
