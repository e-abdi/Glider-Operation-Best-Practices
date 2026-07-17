---
title: Seaglider Deployment Checklist
description: Seaglider deployment checklist — field kit, launch conditions, self-test and pilot sign-off, sea-launch dialogue, tethered launch, and first-dive monitoring.
---

# Seaglider Deployment Checklist

[Print this page :material-printer:](#){ .print-button onclick="window.print(); return false;" }

---

**Mission:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; **Seaglider ID:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_

**Field team:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; **Pilot:** &emsp;\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &emsp; **Date:** &emsp;\_\_\_\_\_\_\_\_\_\_

!!! info "Source"
    Paraphrased from community Seaglider deployment checklists (Cyprus Subsea
    and derivatives) and the APL-UW IOP launch guidance. Adapt to your
    vessel, glider configuration, and local procedures.

---

## 1. Field kit

- [ ] Release hooks, carabiners, shackles, slings, tag lines
- [ ] Cradle
- [ ] Glider spares if available &emsp;<small>*wings, rudder, antenna*</small>
- [ ] Magnetic switch wand(s)
- [ ] Laptop + RS-232-to-USB converter(s) + glider serial/power cable + power supply
- [ ] Glider tool box
- [ ] Binoculars and camera
- [ ] PPE &emsp;<small>*life jackets, helmet, safety glasses, steel-cap boots, gloves, weather gear*</small>
- [ ] VHF radios and Iridium phone

## 2. Conditions & readiness

- [ ] Launch conditions within limits &emsp;<small>*guideline: < 1.5 m waves, < ~0.25 kt (12 cm/s) surface current, > 200 m water depth*</small>
- [ ] Basestation ready to receive; pilot logged in and reachable
- [ ] Glider assembled and powered on well before launch; on standby in **recovery mode** during transit

## 3. Self-test & pilot sign-off

- [ ] Field team: all cables and connectors secure
- [ ] Field team: run interactive **self-test**, watching for errors; keep a terminal log
- [ ] Pilot: analyze the self-test capture on the basestation; complete self-test log
- [ ] Pilot: approve entering **Sea Launch** mode
- [ ] Field team: enter Sea Launch, start a new terminal log
- [ ] Double-check the Iridium phone numbers
- [ ] Antenna fully tightened; **O-ring present** in the antenna connector
- [ ] Pilot: stage a `cmdfile` for a **shallow first dive ending in `$QUIT`**
- [ ] Field team: wait at the *"Has the pilot given ok to launch?"* prompt
- [ ] Pilot: review the uploaded `.prm` parameter dump closely; make any last changes in the cmdfile; give the OK
- [ ] Field team: answer **Y** — watch the bladder pump to full, the glider complete one call, and the `$QUIT` come through
- [ ] Disconnect comms cable; install the dummy plug

## 4. At the launch site

- [ ] Install wings and rudder; assemble antenna
- [ ] Remove sensor caps
- [ ] Attach safety line/tether; request pilot permission to deploy
- [ ] Lower the glider &emsp;<small>*large vessel: sling + release hook on winch, extra line around the rudder; small boat: lower the cradle and free the glider by the antenna mast*</small>
- [ ] Push the glider down by the antenna mast to shed trapped bubbles
- [ ] Confirm floating position: antenna and at least half the rudder out of the water
- [ ] Report attitude and buoyancy to the pilot &emsp;<small>*add foam or lead if trim is off*</small>
- [ ] Pilot: if calls are coming through and trim looks right, instruct tether release, then send `$RESUME`
- [ ] Field team: confirm the glider has submerged and is diving

## 5. First dives

- [ ] Pilot: replace `$RESUME` with `$QUIT` as soon as the dive starts &emsp;<small>*so an unexpected surfacing parks the glider*</small>
- [ ] Field team: **stay on site** through the first shallow dive (~20 min) and until cleared
- [ ] Pilot: review dive 1, then step deeper dive-by-dive, trimming each time, until confident the glider flies reliably
- [ ] Pilot: clear the field team to leave

---

**Notes:**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
