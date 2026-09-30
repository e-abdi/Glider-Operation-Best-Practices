---
title: Comms, GPS & Basestation
description: Seaglider communications — Iridium RUDICS and dial-up paths, primary and alternate numbers, $PROTOCOL, the antenna mast and cable (water ingress, o-rings, resistance and signal-strength checks), dial-up basestations with mgetty, basestation2 vs basestation3 pitfalls, SMS alerts on lost comms, the Garmin GPS and the 2019 week rollover, and Argos/backup trackers.
---

# Comms, GPS & Basestation

A Seaglider gets everything from its surface calls: position, data, and the
next set of instructions. The chain is long: GPS and Iridium share the
antenna mast in the rudder, a cable and bulkhead connector bring the signal
into the hull, an RF relay switches it between GPS and modem, the Iridium
modem makes the call, and a basestation on the other end has to accept the
login and process the files. A weak link anywhere shows up the same way:
calls that fail, and a glider that can't be told what to do.

!!! info "Source"
    Paraphrased from 2017–2024 correspondence between Seaglider operators,
    APL-UW IOP, the manufacturer, satellite airtime providers and service
    providers (antenna failures, dial-up basestation debugging, the 2019 GPS
    rollover, Argos/backup trackers). Defer to APL-UW IOP for basestation
    software and firmware — see the
    [Electronics](../electronics/index.md) page for the IOP links.

---

## Call paths: RUDICS and dial-up

Gliders normally carry two numbers:

- **Primary (`telnum`)** — usually **RUDICS**. The call is routed from
  Iridium's gateway over the internet to a TCP port on the basestation. It is
  reliable, and the airtime rates are competitive.
- **Alternate (`altnum`)** — often a **dial-up (circuit-switched data)** call
  to a modem on a phone line, or a second RUDICS route.

Things to know when setting these up:

- **One RUDICS group delivers to one IP address.** For a second RUDICS
  number that goes to a different basestation, you need a second group, and
  that doubles the setup fee.
- **Dial-up over modern phone networks is fragile.** Iridium's analog data
  calls often fare badly across digital trunk lines, especially over long
  international routes. Some operators find it almost useless as a backup in
  their region.
- **An Iridium modem at the basestation** avoids the phone network. A modem
  with its own SIM, on a serial port of the basestation server, can take the
  glider's alternate calls. Both SIMs need active data service, and the
  basestation SIM needs incoming calls enabled.
- **SIMs lapse.** A deactivated SIM usually has to be replaced, not
  reactivated. After a service, confirm the original SIM went back into the
  glider and is still active.
- **Keep `$PROTOCOL,9` in the `cmdfile`.** The manufacturer's advice is to
  leave it there permanently. The glider can fall back to other transfer
  protocols when comms are bad, which doesn't help modems with flow control.
  Lower values (e.g. 0, XMODEM for everything) are for basestations that
  don't support the raw transfer command (a "rawsend: command not found"
  error).

## The antenna and its cable

Most "Iridium problems" that survive a basestation check are in the antenna
path.

- **Water gets in along the cable.** In one case, damage to the outer jacket
  let water run inside the cable to the connector. Comms were fine on shallow
  dives, then failed as the dives got deeper. The glider had to be recovered
  early with only sporadic positions. **Replace a damaged antenna cable; don't
  patch it**, especially for deep work.
- **Check both o-rings at the cable end** (one on the bottom face, one on the
  side). A flattened o-ring let water into another glider's connector.
- **Suspect water when comms get worse after diving**, or worse with depth.
  Tiny amounts of water in the bulkhead connector are often visible.
- **Resistance check.** The resistance between the centre and outer
  contacts of the antenna bulkhead should be very high. A cable reading in
  the kilohms worked, but badly. Measure with the cable disconnected at both
  ends, because the modem and GPS on the far side give misleading readings.
  A multimeter can't prove insulation is good, only that it is bad.
- **Signal-strength comparison.** Run `hw/modem/signal` for about 30
  minutes on each candidate antenna, with the same sky view, and compare the
  average bars. In one comparison three antennas averaged about 2.8, 1.9 and
  0.4 bars. Treat the result with care:
  - good signal with bad comms can point to the **modem** instead;
  - consistently low signal points to something in the RF path: the
    antenna, cable, bulkhead connector, internal cable, RF relay, or just
    a loose SMA connector.
- **Mast and rudder styles differ.** In older designs the threads are in the
  antenna's plastic shoe. In newer ones they're in the rudder, so a new
  antenna may need the matching rudder. Cable lengths vary between batches.
  Measure the old one before ordering. Weigh the new assembly (one swap
  added about 30 g) and account for it in the trim.
- **Test on land before deploying**, with the glider outside and a clear sky.
  One test failed inside a warehouse and passed at the edge of the car park.

## Dial-up basestations (mgetty)

When a glider connects to a RUDICS basestation but not to a dial-up one, the
modem or phone line is usually the problem. APL-UW's troubleshooting steps:

1. **Call the modem's number from an ordinary phone.** It should answer with
   a modem tone. If the modem rejects calls by caller ID, turn that off.
2. **Take mgetty out of the loop.** Stop it, open the modem's serial port in
   a terminal program (e.g. minicom), and set the modem to auto-answer. When
   the glider calls, does it connect? If you type, does the glider's debug
   output show it?
3. **Turn up the glider's logging** for the phone and surfacing code
   (`capvec HPHONE DEBUG BOTH`, `capvec SSURF DEBUG BOTH` from the menu or
   PicoDOS). Collect a terminal capture of a login attempt alongside
   `mgetty.log` for the same call.
4. **Keep the mgetty invocation simple.** APL-UW runs it with just the port
   (`mgetty ttyS0`) rather than a long list of options. A stray newline
   before the `login:` prompt is normal. Both ends handle it.
5. **Isolate the line.** Have the glider call someone else's dial-up
   basestation. If that works, the problem is at your end.

Symptoms seen in these cases:

- connections at **1200 baud with no error correction**, followed by garbage;
- modems failing to agree on a modulation during the handshake;
- very old modems without flow control, which a Rev E board wanted to use.

One team spent weeks on a backup dial-up station and in the end rebuilt it
from scratch, flying on a partner's backup in the meantime. Arrange a
partner's basestation as a spare before a mission.

## Basestation pitfalls

- **Custom `.login` scripts.** A script added to a glider account's `.login`
  that redirected its output broke the login sequence. Calls ended with
  "shell_disappeared" partway through file transfers. Commenting out the
  redirect fixed it. Test any change to `.login` with a self-test call.
- **basestation2 vs basestation3 `comm.log`.** The date format differs
  between the two. Don't switch a mission from one to the other on the same
  `comm.log`. Start a new one, or remove the old lines. Symptoms include
  "Found Disconnect with no previous Connected" warnings and a crash in the
  comm-log parser.
- **basestation3 flight-model warnings.** Older `sg_calib_constants.m`
  entries (such as `hd_a`, `hd_b`, `hd_c`, `volmax`, `rho0`) are ignored by
  the v3 flight model, which warns about each. Add `% FM_ignore` to suppress
  the warnings.
- **basestation3 `vis`.** In pilot mode the control-file editor needs its
  helpers (`cmdedit`, `validate`) installed next to `vis.py` and on the path.
  Otherwise saves fail with empty errors. Authenticated editing also needs
  `users.yml` and `missions.yml`. The simpler "private" mode runs as the
  invoking user and skips most of the authentication.
- **A glider account that stops processing** (files arrive, nothing is
  produced) can be a permissions problem. Recreating the account from a
  backup copy fixed one case.
- **Getting a `cmdfile` through on a bad link.** A glider in recovery for
  lost comms (`N_NOCOMM_REACHED`) keeps calling. With patience a short
  `cmdfile` gets through even when data files don't. Keep emergency
  `cmdfile`s short.
- **Mining `comm.log`.** Each successful login is followed by a status line
  with voltages, depth and other values. `awk '/logged in/{getline; print}'
  comm.log` pulls them all into one table, which is useful for spotting a
  falling battery or a comms trend over the mission.

### SMS when comms fail

The glider can send an Iridium SMS after a surfacing with failed comms:

- set bit 7 (128) in `$NOCOMM_ACTION`;
- set `$N_NOCOMM` (e.g. 1, to act after one failed cycle);
- store the destination address from PicoDOS with
  `writenv sms_email <address>`;
- test with `hw/modem/smsselftest`.

Only one address can be stored. Send to a shared mailbox and forward from
there.

## GPS

- **The standard receiver is a Garmin 15H or 15xH.** Some 15xL units were
  fitted for a period. They are not rated for the 10 V supply, so avoid them
  on Rev B gliders. On Rev E a board jumper can select a 3.3 V GPS supply.
- **The glider configures the GPS itself** at each use, turning off the NMEA
  sentences it doesn't need and turning on the ones it does, so a new unit
  needs no special setup.
- **An occasional "VGPS timeout – no data received"** on deck dives is
  harmless if the fix follows.
- **Bad connectors.** On two ten-year-old gliders the GPS stopped getting
  fixes because the GPS connector on the main board had gone unreliable. The
  RF relay only clicked when someone pressed on the connector. The same kind
  of connector caused pitch-sensor dropouts. Re-crimp such connectors with
  the proper tool. They aren't designed to be soldered.

### The 2019 week rollover

On 6 April 2019 the GPS week counter rolled over. Some older receivers
started reporting dates in **August 1999** (about 19.6 years off). The
position is unaffected. What happens next depends on the glider:

- some just log the wrong date;
- some go into an endless loop shortly after starting a dive. A watchdog
  reboots the glider about 10 minutes later and, with the default
  `$RELAUNCH`, it goes into recovery. Such a glider can't fly until the GPS
  is fixed.

Fixes and workarounds:

- **Flying with the wrong date** is possible if the glider keeps working.
  The basestation can correct the times in processing.
- **Glider firmware** exists that works around the problem.
- **Updating the Garmin's firmware** fixes it at the source. APL-UW has a
  procedure for doing this with the GPS still installed. It uses a temporary
  alternate firmware image and then goes back to the original (see
  [Electronics](../electronics/index.md#back-up-before-you-change-anything)).
- **The problem can reappear after the receiver loses backup power.** A unit
  that had passed the 2019 rollover began showing it after its backup cell
  was changed or died. A unit whose firmware was updated reverted after a
  power-on reset.

After an update:

1. Leave the GPS running in direct comms with a clear sky for at least
   15–20 minutes to collect a fresh almanac. You can check the almanac week
   with the Garmin almanac query.
2. If the date still won't correct, leave the glider and the GPS unpowered
   for some hours, e.g. overnight, so the receiver's memory fully resets.
   In one case the date corrected itself the next morning with no further
   changes.

### GPS that stops after closing up

On some Rev E gliders the GPS worked with the hull open, then stopped
responding once the glider was sealed and self-tested. It sent only one
status sentence a minute. Swapping modules moved the fault around
inconsistently, and the root cause wasn't found in the correspondence.
Treat it as a known issue: self-test the GPS after closing up, and again on
deck before launch.

## Argos and backup trackers

A backup position source independent of Iridium is what finds a glider whose
main comms have died.

- **Argos tags** (for example, Wildlife Computers tags on the antenna mast)
  only transmit after the glider has been at the surface for an extended
  time. A normal mission with short surfacings may produce no Argos
  positions at all. That's normal, not a failure.
  - The tag's ID must be activated in your Argos programme, and the data
    shared with your account (a "collaborator" rule). Check that positions
    arrive **before** launch. Leave the tag outside, with a clear sky, for a
    couple of hours.
  - Tags switch modes with a magnet. Put them in sleep mode after recovery,
    or they keep transmitting.
- **CLS Linkit-UW** is a newer alternative: rated to 1500 m, and recharged
  inductively on a pad.
  - Its glider profile gets a GPS fix about every 10 minutes while at the
    surface, and repeats the latest position over Argos about every
    2 minutes.
  - Detecting that it has surfaced can take up to about 15 minutes after
    days at sea, so short surfacings can be missed.
  - A unit whose battery ran very low got stuck in a reboot loop (flashing
    white, not responding to the magnet) and had to go back for service.
  - A direction-finding receiver ("platform finder") speeds up recovery
    from a boat.

---

## See also

- [Electronics](../electronics/index.md) — board connectors, firmware
  changes and `$RELAUNCH`.
- [Batteries](../batteries/index.md) — voltages in `comm.log` and a
  battery that won't support the phone at end of life.
- [Recovery](../../../recovery/seaglider/index.md) — what to do when a
  glider stops calling.
