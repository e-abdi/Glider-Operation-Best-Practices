---
title: Seaglider One-Pager
description: Quick-reference commands and reminders for common Seaglider basestation, PicoDOS, and piloting operations.
---

# Seaglider One-Pager

Quick-reference notes for common Seaglider basestation and piloting operations. This page grows over time — add notes as new important reminders are identified.

!!! info "Source"
    Paraphrased from the APL-UW IOP *Basestation3 and seaglider.pub Best
    Practices* note, the *Extended PicoDOS Reference Manual*, the *Seaglider
    Piloting Parameters* guide, IOP PLOCAN training material, and pilot
    working notes. Always confirm against the
    [Parameter Reference Manual](https://iop-apl-uw.github.io/basestation3/html/Parameter_Reference_Manual.html)
    and defer to APL-UW IOP documentation.

---

## Basestation Shortcuts

| Command | What it does |
|---|---|
| `gcd sgXXX` | Jump straight to glider `sgXXX`'s current mission directory. |
| `basepy <script>.py --help` | Run a basestation3 script with the correct interpreter (`/opt/basestation/bin/python3`) without typing the full paths. |
| `tail -f comm.log` | Watch a glider's call-in log live as it happens. |

---

## Starting and Ending a Mission Cleanly

!!! tip "Use `NewMission.py` / `MoveData.py` for every mission"
    `basepy NewMission.py . MyMissionName` before a mission sets up the
    mission directory (copies in `sg_calib_constants.m`, symlinks `pagers.yml`,
    and points `current` at it) so the glider and pilot are both working from
    the right place. `basepy MoveData.py -m . -t ArchiveName` after a mission
    files everything away. Skipping either one is the easiest way to end up
    with stray files and a messy basestation before the next mission.

---

## Editing `missions.yml` Without Breaking vis

1. Copy it: `cp missions.yml ~/missions.new`
2. Edit the copy.
3. Test it: `basepy vis.py -r ./ -f ~/missions.new -t`
4. Only if that comes back clean: `cp ~/missions.new missions.yml`

---

## Simulating an Incoming Call

!!! tip "Test the basestation without waiting for the glider to phone home"
    Logging into a glider's dedicated basestation user account and exiting
    (`su - sgXXX` then `exit`) re-runs the same call-processing pipeline a
    real Iridium call triggers — handy for testing basestation-side scripts
    or plotting changes on demand.

---

## PicoDOS Batch Commands

Useful `pdoscmds.bat` / interactive PicoDOS commands beyond the basics
covered on the [Dive Cycle & Control Files](dive-cycle-and-control-files.md)
page:

| Command | What it does |
|---|---|
| `target NAME` / `targets NAME RADIUS` | Switch the glider's current target (and optionally its radius) without editing the full targets/mission file. |
| `resend_dive /d 289 1` | Resend one 4 kB chunk of dive 289's data file (`/l` log, `/c` capture, or drop the chunk number to resend the whole file). |
| `xr FILE` / `xs FILE` (also `get` / `put`) | Receive (`xr`/`get`) or send (`xs`/`put`) a file over XMODEM. |
| `ren OLD NEW` / `del FILE` | Rename or delete a file on the CF card. |
| `strip1a FILE` | Strip trailing XMODEM padding — required on anything transferred to the glider over XMODEM. |
| `tar c ARCHIVE.tar FILES` / `tar x ARCHIVE.tar` | Bundle or unpack files on the CF card, e.g. before pulling a batch off. |
| `menu /path/to/command args` | Run any command from the glider's menu tree by absolute path. |

!!! example "Swapping a sensor's `.cnf` file via a batch"
    ```
    ren pam.cnf pambad.cnf
    del pam.cnf
    xr pam.cnf
    strip1a pam.cnf
    menu param/config init=1
    ```
    Rename the old config out of the way, receive the replacement over
    XMODEM, strip the padding, then reinitialize the sensor's config menu so
    it picks up the new file.

---

## Loitering / Subsurface (Park) Dives

Two different things both get called "loitering":

**Picking a depth to sit at.** Look at the T/S and density (SigmaT) casts to
find a stable density surface at the target depth. As a rule of thumb, about
**1 SigmaT unit ≈ 50 cc** of buoyancy adjustment, and **1 cc ≈ 4 AD counts**
of VBD travel — useful for estimating how far to offset the VBD to sit
neutrally buoyant there.

**Making the glider actually stay there.** `$T_LOITER` holds the glider at
apogee (neutral buoyancy, zero vertical velocity) for that many seconds
before it pitches up to climb. While loitering the glider will pump but
**never bleed**, and it does not servo on depth. Remember to extend
`$T_MISSION` / `$T_ABORT` manually to cover `$T_DIVE + $T_LOITER`, or the
mission timeout will cut the loiter short.

!!! warning "Subsurface finishes and comms can miss each other"
    `$D_FINISH` / `$D_SURF` / `$N_NOSURFACE` let a dive finish at depth
    instead of the surface (`$D_FINISH` must be **≥ `$D_SURF`**, or the
    glider always surfaces normally). If you combine this with
    `$CALL_NDIVES > 1`, make sure the dives on which the glider actually
    calls line up with a real surface finish — otherwise you won't hear from
    the glider again until `$N_DIVES` or a low-battery recovery trigger.

---

## Bumping the Baud Rate for Fast File Transfers

Loading a new `main.run` or other large file over the serial/XMODEM link at
the default rate is slow. From PicoDOS:

```
PicoDOS> baud 38400
```

Change the terminal program's serial port setting to match, run the
transfer, then **set it back to the default (9600)** afterward — the glider
and terminal must agree on baud rate to talk at all, and leaving it changed
will strand the next session.
