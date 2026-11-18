---
title: Science Sensors
description: Field notes on the Slocum science payload — the pumped CTD (mincondfreq, fresh water, blocked cells, calibration tags), the Aanderaa oxygen optode (u_oxy4_slow_surface_mode, the G3 cable/bulkhead corrosion and failure problem), SUNA nitrate sensors (MCBH pinouts and mounts), acoustic receivers and tags, and general advice on MCBH wiring and connector care.
---

# Science Sensors

The science bay runs its own computer and sensor "proglets", separate from
the flight computer. Most science problems at sea show up as **science
warnings or aborts**, corrupted sensor strings, or data that looks wrong
once it's processed. This page collects field experience with the common
Slocum payload sensors. For processing the data, see
[Slocum Data Processing & QC](../../../data-management/slocum/data-processing-qc.md).

!!! info "Source"
    Paraphrased from the UG2 Slack #piloting, #general and #data channels
    (2024–2026), the Slocum `masterdata` and `proglets.dat` comments, and
    operator correspondence. Sensor configuration differs between firmware
    releases and payload builds: check your own `proglets.dat` and ask
    Teledyne glider support before changing a sensor's set-up.

---

## Pumped CTD (Sea-Bird GPCTD)

### The pump only runs in seawater

The CTD has an internal setting, **`mincondfreq`** (minimum conductivity
frequency, usually 3000 Hz), and it won't start its pump until the
conductivity frequency is above it. 3000 Hz corresponds roughly to water of
25 PSU or more, depending on the cell's calibration. So:

- **On the bench or in a simulation**, the CTD powers up but the pump stays
  off, which protects it from running dry.
- **In fresh or brackish water** the pump may never start. Lower
  `mincondfreq` for those deployments, and set it back afterwards.

Check the current value by talking to the CTD from the science computer
(`uart` / `u4stalk`) and sending `ds`; the output includes `minimum
conductivity frequency`.

!!! warning "Never run the pump dry for more than about 30 seconds"
    If you override `mincondfreq` for a bench test, keep the cell wet.

### Salinity that goes wrong mid-mission

Dive/climb salinity differences that grow partway through a mission,
after the data has already been through thermal lag correction, are
usually:

- a **partly blocked cell or tubing** (biology), which often flushes itself
  at sea, but not always; or
- a **failing pump**.

Look at raw conductivity at inflections (dive and climb data close in time)
rather than at salinity. Neither cause can be fixed in processing: flag the
affected profiles. More in
[CTD Post-Processing](../../../data-management/shared/ctd-post-processing.md#4-look-for-sensor-problems).

### After factory calibration

A glider came back from factory CTD calibration with a paper calibration tag
trapped in the stiffener ring at the front of the science bay. Don't deploy
like that: the stiffener ring has O-rings on both sides. Getting it out
means opening the glider fully, removing the science bay and the bracket
that holds the ring, and pushing the ring out with a hull-cracking tool.
Then replace the O-rings, clean the sealing surfaces of all paper lint, and
reseal, pull vacuum and run a functional check. Inspect the science bay
whenever a glider comes back from service.

---

## Aanderaa oxygen optode

### `u_oxy4_slow_surface_mode`

The `oxy4` proglet comment says this setting should be **1 for the 4330F
and 0 for the 4831**. The 4831 is essentially a 4330 with an MCBH-style
connector, and the "F" marks the fast-response foil, so some operators
reason that a 4831F should use 1. The masterdata doesn't say what the
setting actually changes. Ask Teledyne support before relying on either
value, and record which one you flew.

To change it at sea, set it in the **longterm** sensors or in the mission
rather than editing `autoexec.mi` remotely (a truncated `autoexec.mi`
upload is a real risk).

### Optode, cable and bulkhead failures on G3s

From about 2023, many groups reported Aanderaa optodes on newer G3s failing
at sea, often within weeks, sometimes after 3–4 months:

- **Symptoms:** a sudden increase in science warnings, corrupted optode
  strings causing **science aborts**, then a dead ("bricked") optode that no
  longer answers even on the raw UART.
- **What came back:** heavy white corrosion at the optode's **MCBH
  bulkhead on the aft end cap**, sometimes salt crystals inside the aft cap
  (water ingress through the bulkhead), sometimes corroded screws on the
  optode window, and sometimes optodes and pins that looked perfect.
- **Not the optodes alone:** the same optode model ran for years without
  failure on moorings and profilers in the same groups. One group saw
  problems on most of its G3s with the newer **single, thicker, stiffer
  cable**, but none on older gliders with the Y-cable. Suspected causes:
  the stiff cable's **tight bend** in the cramped tail cowling loading the
  connector at an angle, a **grounding** problem, and a connector body not
  protected by the vehicle's anode. Teledyne was reported to be working on a
  board change for the grounding issue.

What has helped:

- A **more flexible (neoprene) cable**, coiled gently, and **no cable ties**
  forcing it into a tight radius. One group saw no more failures after this,
  but didn't call it solved.
- Mounting the optode elsewhere (dorsally, or cabled to an MCBH on the
  payload bay instead of through to the aft cap). Dorsal mounts also allow
  in-air calibration checks at the surface.
- Checking with a multimeter that the bulkhead is at the **same potential**
  as the other exposed metal and the zinc. A broken internal wire or poorly
  crimped pin can isolate it.
- On G2s the optode often shared a power bit with the CTD, so its
  connector carried voltage whenever the CTD was on, which speeds up
  corrosion. One G2 had all its science-bay metal badly corroded after an
  optode failure. On G3s each sensor is powered only while its UART is
  active, so **removing a failing optode from `proglets.dat`** removes its
  power, and gliders have finished missions of 30+ days after doing that.
- Leaky current from other sensors (an electromagnetic sensor on a
  turbulence package) has also been blamed for connector corrosion.

If an optode starts throwing errors mid-mission, comment it out of the
proglets, keep flying, and inspect the bulkhead, the inside of the aft cap
and the cable on recovery. Report it to Teledyne with photos.

### Data notes

The optode has a large thermal lag. Log the **phase** outputs so oxygen can
be recomputed shoreside with the CTD temperature and corrected for salinity
and pressure; the optode doesn't do that itself.

---

## SUNA nitrate sensor

- **MCBH pinouts vary** between payload builds and sensors. Before probing
  for power, find the pinout for your sensor (the deep SUNA used on gliders
  has been reported to match the SUNA V2) and trace it through the cable
  with a continuity test, rather than probing live pins.
- Some groups **standardise** their payload-bay MCBH wiring as straight
  through (pin *n* on the bulkhead to pin *n* on the internal Molex), so any
  sensor's harness can be worked out from the sensor's own pinout. The
  science-board side connects to the UART channels in `proglets.dat`.
- **Mounting:** the G3 forward mounting hardware for other sensors (for
  example a turbulence package) looks similar but doesn't fit the SUNA.
  Some groups 3D-print their own forward SUNA mounts.

---

## Acoustic receivers and tags

- **Fish-tag receivers** have been carried on both Slocums (easy to strap
  on) and Seagliders. On a Seaglider, one was mounted on the aft fairing
  and detected tagged squid at around 500 m. Keep it **away from the
  CT sensor** (on a Seaglider with a legato on the top cover, mount the
  receiver on the bottom cover).
- **Downloading seabed receivers** from a glider over an acoustic modem is
  being tried; surface vehicles have done it for years with success rates
  in the 90s per cent.
- A **transmit-only tag** on the glider is a cheap backup locator; see
  [Argos → acoustic beacons](../argos/index.md#acoustic-beacons-as-a-backup).

---

## Other payload notes

- **Nortek AD2CP:** set-up is mostly in its `ad2cp.cfg` file. Ask other
  operators for a worked configuration; several groups maintain internal
  guides.
- **Storage:** 8 GB cards in each computer have been enough for 45–60 day
  missions with file compression on.
- **Connectors:** grease every MCBH and SubConn as the maker specifies, and
  inspect for white corrosion every recovery. See
  [Connectors](../../shared/connectors/index.md) and
  [O-Rings → the green GO plug](../o-rings/index.md#the-green-go-plug).

---

## See also

- [Slocum Data Processing & QC](../../../data-management/slocum/data-processing-qc.md)
- [CTD Post-Processing](../../../data-management/shared/ctd-post-processing.md)
- [Aborts](../../../piloting/slocum/aborts.md): science "stop logging" behavior errors
- [Power Saving](../../../piloting/slocum/power-saving.md): sampling only some yos
