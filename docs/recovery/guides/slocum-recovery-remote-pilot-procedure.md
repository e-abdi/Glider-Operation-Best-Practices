# Slocum Recovery Procedure (Remote Pilot)

## Overview

This guide describes the standard actions performed by a remote pilot before, during, and after recovery of a Slocum glider.

Consider:

* Environmental conditions
* Vessel traffic
* Local operating conditions
* Glider battery health

Adjust timing according to the situation. The glider should ideally already be drifting on the surface before the field team arrives on site.

---

## 1. Pre-Recovery Coordination

Before recovery, discuss the following with the field team:

* Estimated arrival time on site
* Estimated recovery time
* Potential schedule changes
* Communication method
* Frequency of position updates
* Glider configuration (call-in interval, strobe operation, etc.)

---

## 2. Catch the Glider on the Surface

Several hours before recovery:

* Catch the glider on the surface
* Shorten the surfacing interval by modifying:

  * `yo10.ma`
  * `yo14.ma`
  * `surface01.ma`
  * `surface21.ma`

---

## 3. Set the Glider to Drift

Approximately 60 minutes before the field team arrives.

### Disable XML Script

Remove the XML script from SFMC.

### GPS and Iridium Note

!!! warning

```
Iridium and GPS share the same antenna.

You cannot use both simultaneously.

Periodically disconnect Iridium to obtain a fresh GPS fix and check the GPS fix age in the Surface Dialog.
```

### Commands – Set Glider to Drift

| Command                             | Description                                                                                |
| ----------------------------------- | ------------------------------------------------------------------------------------------ |
| `^c`                                | Stop the current mission and return to `gliderDOS>`.                                       |
| `put u_max_time_in_gliderdos 14400` | Time (seconds) the glider will remain drifting before automatically running `lastgasp.mi`. |
| `put c_de_oil_vol 420`              | Set oil pump to maximum buoyancy.                                                          |
| `strobe on`                         | Turn strobe on (unless operating in bright daylight).                                      |
| `callback 1`                        | Disconnect and reconnect after 1 minute.                                                   |
| `callback 15`                       | Disconnect and reconnect after 15 minutes.                                                 |

### Common Drift Durations

| Duration | Value |
| -------- | ----- |
| 2 hr     | 7200  |
| 4 hr     | 14400 |
| 12 hr    | 43200 |
| 24 hr    | 86400 |

### Other Useful Commands

| Command                                                                                                   | Description                                   |
| --------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `where`                                                                                                   | Display Surface Dialog and GPS information.   |
| `report ++ m_gps_lat`                                                                                     | Enable GPS latitude reporting.                |
| `put u_iridium_max_time_til_callback 1800`                                                                | Change callback interval.                     |
| `use gps`                                                                                                 | Return GPS to service.                        |
| `use all`                                                                                                 | Return all devices to service.                |
| `report clearall`                                                                                         | Stop sensor reporting.                        |
| `put c_recovery_on 1`                                                                                     | Deploy nose recovery line.                    |
| `use - hd_pump attitude_rev ocean_pressure vacuum pitch_motor digifin altimeter science_super leakdetect` | Disable selected devices to conserve battery. |
| `put c_weight_drop 1`                                                                                     | Drop weight in an emergency.                  |
| `put c_weight_drop 0`                                                                                     | Reset weight-drop command.                    |
| `put m_weight_drop 0`                                                                                     | Reset weight-drop status.                     |

---

## 4. Position Monitoring

If the field team does not have direct access to SFMC:

* Provide regular position updates.
* Use the GPS Location value from the Surface Dialog.
* Monitor GPS fix age.
* Refresh GPS approximately every 300 seconds.

---

## 5. FreeWave Communications

If the field team is operating a FreeWave receiver:

* Iridium call-ins may stop.
* The glider will prioritize FreeWave communications when available.

This behaviour is expected.

---

## 6. Deploy Nose Recovery System

Deploy the nose recovery line when:

* The field team is approximately 10 minutes from the glider, or
* The field team has visual contact with the glider.

### Recovery Command

| Command               | Description                      |
| --------------------- | -------------------------------- |
| `put c_recovery_on 1` | Activate the nose recovery line. |

Inform the field team that deployment is not instantaneous and confirm successful release.

---

## 7. Recovery Operations

While recovery is in progress:

* Continue providing position updates.
* Expect reduced communication while the vessel crew focuses on retrieval.
* Be prepared to assist with troubleshooting if required.

---

## 8. After Recovery

Once the field team confirms the glider is safely aboard the research vessel:

* Position the glider where it has a clear view of the sky.
* Execute the shutdown procedure.

### Shutdown Commands

| Command                 | Description                           |
| ----------------------- | ------------------------------------- |
| `put c_air_pump 0`      | Deflate the air bladder.              |
| `put c_de_oil_vol -420` | Retract the ballast pump for storage. |
| `get m_de_oil_vol`      | Verify the pump reaches -420.         |
| `exit`                  | Shut down the glider.                 |

---

## 9. Post-Recovery Actions

Record:

* UTC hour of shutdown
* UTC minute of shutdown

Inform the field team:

* Remove the green plug.
* Install the red plug.
* Complete within 30 minutes of shutdown.

---

# Troubleshooting

## Nose Recovery Line Not Deploying

Possible causes:

1. Burn wire has not released.
2. Recovery spool is mechanically obstructed.

### Recommended Actions

| Action            | Description                                     |
| ----------------- | ----------------------------------------------- |
| Retry deployment  | Execute `put c_recovery_on 1` again.            |
| Boat hook assist  | Tap the yellow nose cone using a boat hook.     |
| Shallow dive test | Command a dive to approximately 10 m.           |
| Deploy workboat   | Consider manual recovery if other methods fail. |
|                   |                                                 |
