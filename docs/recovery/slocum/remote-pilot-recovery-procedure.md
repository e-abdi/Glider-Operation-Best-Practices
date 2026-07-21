---
title: Slocum Remote Pilot Recovery Procedure
description: Standard actions for a remote pilot before, during, and after recovery of a Slocum G3 glider — setting the glider to drift, deploying the nose recovery line, and shutdown.
---

# Slocum Glider Recovery Procedure (Remote Pilot)

This guide describes the standard actions carried out by a remote (on-shore)
pilot before, during, and after recovery of a Slocum glider. For the
corresponding field-team actions, see
[Field Recovery Procedure](field-recovery-procedure.md).

!!! info "Source"
    Paraphrased from NorGliders / University of Bergen (UiB) field
    procedure notes (*SL12 — User Notes — G3 Recovery Remote Pilot*).

Consider the environment, vessel traffic, local operating conditions, and
the glider's battery health — is it safe to keep the glider on the surface
for an extended period? Adjust timing to the situation. We typically set the
glider to drift 60 minutes before the field team is due on site, but if
arrival time is uncertain, set it to drift earlier — the glider should
already be drifting by the time the field team arrives.

---

## 1. Pre-Recovery Coordination

Discuss with the field team beforehand:

- Estimated time the field team arrives on site, and the likelihood of the
  schedule shifting.
- Estimated time of recovery (e.g. after a CTD cast).
- Method of communication, and how often the field team will receive glider
  position updates.
- Glider configuration: call-in interval, strobe function, etc.

---

## 2. Catch the Glider on the Surface

Several hours before the planned recovery, catch the glider on the surface
and shorten the surfacing interval by editing `yo10.ma`/`yo14.ma` and/or
`surfac01.ma`/`surfac21.ma`.

---

## 3. Set the Glider to Drift

About 60 minutes before the field team is due on site:

1. Turn off the XML script in SFMC.
2. Run the commands below to set the glider to drift.

!!! warning "Iridium and GPS share an antenna"
    You cannot use both at the same time. Periodically hang up the Iridium
    phone (`callback 10`) to let a fresh GPS fix through, and check the
    fix's age in the surface dialog. If the GPS device has been taken out
    of service, put it back with `use gps`.

### Commands — Set Glider to Drift

| Command | Description |
|---|---|
| `^c` | Stop the current mission and return to `gliderDOS>` (repeat if several missions are sequenced). |
| `put u_max_time_in_gliderdos 14400` | Drift this many seconds before `lastgasp.mi` runs automatically — 2 hr = 7200, 4 hr = 14400, 12 hr = 43200, 24 hr = 86400. |
| `put c_de_oil_vol 420` | Set the oil pump to maximum buoyancy. |
| `strobe on` | Turn the strobe on (unless in broad daylight). |
| `callback 1` | Hang up and call back in 1 minute — use to force a fresh GPS fix while staying connected. |
| `callback 15` | Hang up and call back in 15 minutes (or 5/10/30, depending on the situation) once finished communicating. |

### Other Useful Commands

| Command | Description |
|---|---|
| `where` | Display the surface dialog — GPS fix, time, and other sensor values. Also a good way to just confirm the glider is connected. |
| `report ++ m_gps_lat` | If the field team has a FreeWave receiver and is nearby, turn on reporting of a sensor so they pick up a signal as soon as they're in range. |
| `put u_iridium_max_time_til_callback 1800` | Change the default Iridium callback interval (default 600 s). Keep it at least 5 minutes less than `u_max_time_in_gliderdos`, and be sure you're OK not hearing from the glider for that long. |
| `use` | List sensor devices and check whether any are out of service. |
| `use gps` / `use all` | Return GPS, or all devices, to service. |
| `report clearall` | Stop reporting a sensor. |

!!! danger "Disabling devices to save battery"
    If the glider is low on battery, disable non-essential devices — **but
    only after** setting max buoyancy and confirming with `get
    m_de_oil_vol`:

    ```
    use - hd_pump attitude_rev ocean_pressure vacuum pitch_motor digifin altimeter science_super leakdetect
    ```

    The glider will ask you to confirm with `y` for each device — type
    quickly, and double-check the command before sending it. **Never**
    disable Iridium or GPS.

!!! danger "Dropping the weight"
    Only do this if there is genuine concern about the glider's buoyancy —
    once dropped, the glider cannot overcome positive buoyancy and can no
    longer dive or continue a mission.

    ```
    put c_weight_drop 1
    put c_weight_drop 0
    put m_weight_drop 0
    ```

    The glider will report that the burn wire has activated; give it a
    minute to burn, then zero the sensors as above. You will likely need
    `exit reset` to clear the messages — do this *before* disabling other
    devices, or you'll need to do it twice.

3. Depending on how far away the field team is, either stay connected or
   run a drifting script from the SFMC glider terminal (e.g. `Callback5.xml`,
   `Callback10.xml`) to have the glider hang up and call back the primary
   number every 5 or 10 minutes.

---

## 4. Position Monitoring

If the field team doesn't have direct SFMC access, provide regular position
updates from the **GPS Location** value in the surface dialog, noting how
many seconds old the fix is. Refresh it roughly every 300 seconds, or more
often if the glider is drifting significantly.

---

## 5. FreeWave Communications

If the field team is running a FreeWave receiver, or the glider is very
close to the ship, Iridium call-ins may stop — the glider prioritizes
FreeWave when it finds a receiver, or the ship may be blocking the
satellite signal. This is expected behaviour.

---

## 6. Deploy the Nose Recovery System

Deploy the nose recovery line when the field team is about 10 minutes from
the glider, or as soon as they have visual contact. Inform them that release
isn't instantaneous — the line is wound on a spool and takes several
minutes to uncoil — and to let you know if it doesn't release.

| Command | Description |
|---|---|
| `put c_recovery_on 1` | Activate the nose recovery line. |

---

## 7. During Recovery

Expect reduced communication while the field team focuses on retrieval —
continue providing position updates and be ready to help troubleshoot (see
below) if needed.

---

## 8. After Recovery

Once the field team confirms the glider is safely aboard the **research
vessel** (not the workboat), have them position it with a clear view of the
sky, then run the shutdown sequence:

| Command | Description |
|---|---|
| `put c_air_pump 0` | Deflate the air bladder. |
| `put c_de_oil_vol -420` | Retract the ballast pump for safe storage. |
| `get m_de_oil_vol` | Confirm the pump reaches −420 after a few minutes. |
| `exit` | Shut down the glider — confirm with `y` once you're sure (via the field team) that it's safe to do so. |

---

## 9. Post-Recovery

Note the UTC hour and minute you shut the glider down, and tell the field
team they have **exactly 30 minutes** from that time to remove the green
plug and install the red plug.

---

## Troubleshooting: Nose Recovery Line Not Deploying

A nose line has never failed to deploy so far, but two things could cause
it: the burn wire hasn't burnt through, or the recovery spool is fouled or
caught on something in the nose cavity.

| Action | Description |
|---|---|
| Retry | Send `put c_recovery_on 1` again. |
| Boat hook assist | Have the vessel come alongside and tap the yellow nose cone with an extended boat hook, at several angles. |
| Shallow dive test | Command a dive to ~10 m via `yo14.ma` — if the wire has burnt, the buoyant nose may lift off on its own. |
| Deploy workboat | If none of the above works, consider a [workboat recovery](field-recovery-procedure.md#backup-recovery-procedure-workboat). |
