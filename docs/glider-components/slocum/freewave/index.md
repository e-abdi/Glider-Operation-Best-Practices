---
title: Freewave
description: What the Slocum Freewave 900 MHz RF modem does, how the glider slave and shoreside master are configured, how the glider chooses Freewave vs. Iridium, power-saving with the console, and field troubleshooting for interference and dead links.
---

# Freewave

The **Freewave** is a 900 MHz spread-spectrum RF radio modem used for
**short-range, high-speed** communication with a Slocum glider. When the glider
is on the surface within line-of-sight of a shoreside (or boat-side) Freewave,
it gives you a fast, no-cost console — fast enough that **no cable is needed**
for in-lab work, so most bench communication is done over RF rather than a
direct connection.

Each glider carries a **slave** modem internally; you operate a **master**
modem at the dock, in the lab, or on the recovery boat. The link is the glider
operator's primary backup to Iridium: short range, but free and immediate when
you can reach it.

!!! info "Source"
    Paraphrased from the *Slocum G3 Glider Operators Manual* (Rev. 1,
    "RF Modem Telemetry" and Appendix F, "FreeWave Configuration"), the
    UG2 community Slack, and the Teledyne Webb Research user forum. Appendix F
    itself reproduces excerpts of the
    FreeWave Technologies *Spread Spectrum User Manual* — for the radios
    themselves, refer to FreeWave's documentation. This is a condensed field
    reference — always defer to the official Teledyne documentation for your
    specific glider.

---

## Master and slave roles

The link is **point-to-point**: one master talks to one slave at a time.

| Role | Where | Factory configuration |
|---|---|---|
| **Slave** | Inside the glider, on the flight Persistor | Set to **call all** masters |
| **Master** | Shoreside / lab / boat | Set to talk to **one specific glider** |

- The glider **slave is factory-set to "call all"**, so any properly configured
  master can reach it. Teledyne strongly recommends **never changing the slave**
  configuration on the glider.
- The **master should never be set to "call all."** You point each master at a
  specific glider by entering that glider's seven-digit Freewave serial number
  (from the glider's `autoexec.mi`) into the master's call book and selecting
  that entry.

!!! note "Older gliders may not be set to call all"
    Some early units were *not* configured to call all, so a shared "emergency"
    master may fail to connect to them. Reconfiguring the slave is **not**
    trivial — it requires a special programming cable (one that can momentarily
    pull the setup pin to ground), and Teledyne's guidance is to contact glider
    support rather than reprogram the in-glider modem yourself.

---

## Configuring a master to a glider

To point a master at a different glider (from Appendix F):

1. Connect the master to a computer's serial port and open a terminal program
   (e.g. PuTTY/HyperTerminal) at **19,200 N-8-1, no flow control**.
2. Press the **setup button** next to the serial port on the back of the radio.
   The three board lights turn green and the **Main menu** appears.
3. **Operation Mode** (menu `0`): set the radio as point-to-point **master** (`0`).
4. **Baud rate** (menu `1`): setup is always 19,200, but set the radio's
   *communication* baud to **115,200** to match the glider link.
5. **Frequency key** (menu `3`): set the key (the manual's example uses key `5`).
   The master and slave must share the same frequency key.
6. **Call book** (menu `2`): add the glider's seven-digit Freewave serial
   number into one of the 10 slots, then press **C** and select that entry to
   call. **Do not select "A" (call all)** on a master.
7. Press **Esc** to exit setup.

!!! tip "One master, many gliders in the lab"
    A common lab/yard setup is to keep one master permanently wired to the
    network and load several gliders into its call book, then switch which
    glider it calls as needed — rather than swapping modem boxes. This avoids
    cross-connecting to the wrong glider and means you never touch the
    glider-side slave.

!!! danger "A forgotten powered-on master will steal your comms"
    Because every glider slave is set to **call all**, *any* powered master whose
    call book contains your glider's serial can grab the link — and you won't know
    it. The classic time-sink: a **second master left powered on a bench somewhere
    in the building**, programmed to the same glider, intermittently steals the
    connection while you troubleshoot a glider that **isn't actually broken**.
    Operators have lost **days** to this. When comms are flaky in the lab, first
    confirm no other master (or another group's radio) is powered up and pointed at
    your glider.

!!! warning "Changing the glider-side baud or table needs a wired connection"
    You generally **cannot** reconfigure the in-glider Freewave through the RF
    link itself (you'd be cutting the very link you're using). Changing the
    glider's slave table or baud rate requires connecting directly to the modem
    board with the special cable. Note the baud the glider's Persistor uses to
    talk to its slave is independent of the baud between the master and your
    terminal emulator.

---

## How to test the link

When both the glider and the master are powered and in range, the master's
**carrier detect (CD) light turns from red to green**. A green CD is your
quick confirmation that the RF link is up — this is also the standard bench
test that the glider's comms board and Freewave module are alive.

---

## consci — talking to the science Persistor over Freewave

The Freewave normally connects to the **flight** Persistor. To reach the
**science** Persistor over the same radio:

- **From PicoDOS:** type `consci`. This is a hardware-controlled hand-off. To
  return to the flight Persistor, the carrier must drop for **three seconds** —
  cut power to the master for about 10 seconds.
- **From GliderDOS:** type `consci`. This uses a software-controlled connection
  (the **"clothesline"**); type `quit` to return to flight.

A successful hand-off changes the prompt from `(GPICO)C:\>` to `(SCI)C:\>`.

---

## Freewave vs. Iridium during a mission

On the surface mid-mission, the glider **prefers Freewave** and falls back to
Iridium:

1. On surfacing, the glider powers the Freewave console and **looks for a
   carrier** first.
2. If a carrier is **found**, it stays on Freewave and **does not** place an
   Iridium call.
3. If **no carrier** is found, it powers the Freewave off and dials in over
   **Iridium**.

!!! note "Why a surfaced, in-range glider sometimes still calls Iridium"
    If the glider doesn't latch the Freewave carrier in that brief window, it
    will go to Iridium even though you're standing right there with a master.
    Issuing the **callback** command while in range usually establishes the
    Freewave connection. Note the behavior differs by state: from **GliderDOS**
    the glider can connect by Freewave *and* place its Iridium call at the same
    time; mid-mission it picks one.

**Forcing the choice:**

- In mission, `H` is the in-mission shortcut for `callback` (e.g. `h 0 0`).
- `put c_iridium_on 1` turns Iridium on as a second console; for file transfers
  you can force the transfer over Iridium with the `-f=irid` flag, e.g.
  `S -f=irid -num=3 *.sbd *.tbd`. (When moving files, the Iridium phone hangs up
  and Freewave takes priority unless you force it.)
- Surface-dialog argument `force_iridium_use: 1.0` in a `surfac*.ma` file forces
  an Iridium call even while Freewave is connected — handy when simulating a
  mission on the bench: watch the dive over Freewave, drop master power at the
  GPS-fix point to trigger Iridium, then restore power to keep watching.

---

## Power: the console and low-power drift

The Freewave console is a **surprisingly large surface power draw**. Operators
report turning it off saved on the order of **~1 A·h per day** on a glider
drifting on the surface waiting for recovery.

`c_console_on` controls it:

| Value | Behavior |
|---|---|
| `0` | Freewave console **off** |
| `1` | On at surface; powers **off underwater** after `u_console_reqd_cd_off_time` (default **15 s**) with no carrier detect |
| `2` | **On regardless** (the usual default) |

- For a low-power surface drift far from any master, `put c_console_on 0` is a
  meaningful saving; the starting-point mission `nofly.mi` is the canonical
  low-power surface-drift mission.
- **In mission**, the console already turns off ~15 s after the surface check if
  there is no carrier (that's the "choosing Iridium" log line), so the savings
  there are smaller. **In GliderDOS** the Freewave is always on at the surface —
  this is where leaving it on really costs you.
- Newer firmware exposes `u_console_disabled_in_mission` as a cleaner way to
  keep it off for low-power missions.

!!! danger "Turn the console back on before you send a boat"
    The Freewave is your in-range backup for recovery. If you take it out of
    service (`use - console`) or `put c_console_on 0` to save power, **remember
    to turn it back on** before a recovery crew goes out expecting to home in on
    it. Also note: the operator does **not** have fine-grained control of
    Freewave power mid-mission — the surface behaviors constantly overwrite
    `c_console_on` as the glider climbs, fixes GPS, and chooses comms. Freewave
    is a **critical device** and cannot be taken out of service from GliderDOS
    with a glider on the pier.

---

## Antenna placement and RF interference

Placement drives link quality — and a noisy Freewave can interfere with the
glider's own sensors.

- **Height helps.** A higher master antenna generally gives a better link.
- Keep the master **away from computers, phones, and other RF gear**; even a
  ~2 ft move can clear up a noise problem.
- For longer reach, FreeWave sells directional and omni antennas; band-pass /
  cavity filters help in extreme noise (near cell or pager towers).

!!! tip "Realistic range depends almost entirely on antenna height"
    Freewave is **line-of-sight**. From a ship's deck, expect roughly
    **0.5–1 mile**. But operators using a **directional Yagi raised up high** — for
    example on a cliff or headland above the deployment site — have held a Freewave
    link **10–15 miles** offshore. If you need range, get the master antenna
    **high and pointed**, not just bigger. Wave action that periodically blocks the
    line of sight will also cut in and out at the edge of range.

!!! warning "Freewave RF noise can trip pump and leak-detect faults"
    Several operators have traced bench and at-sea oddities — a **deep/HD pump
    that misbehaves**, spurious **digifin leak-detect aborts** ~300 s after
    surfacing — to **RF interference from the Freewave** coupling into the pump
    pot or leak-detect/pressure lines. Reported mitigations, with mixed success:
    use a **good (outdoor coax-type) antenna** and move it farther away; add
    **ferrite beads** to the antenna leads; **physically separate** the
    Freewave, Iridium, leak-detect, and pressure-sensor cabling inside the
    glider. For confirmed-noisy leak-detect, some operators (on Teledyne's
    advice) lower `f_digifin_leakdetect_threshold` to match the glider's
    background noise — values reported from ~980 to ~1015 are glider-specific.
    A few stubborn G3/G3S units never fully cleared and went back to Teledyne
    under warranty.

---

## Field troubleshooting

| Symptom | Things to check |
|---|---|
| In range, on surface, no Freewave (calls Iridium instead) | Issue `callback`; carrier may not have latched in the brief surface window. Confirm master powered and CD light behavior. |
| Master CD green in setup but **dead outside setup** (no lights, no comms) | Receiver may have failed — verify it works only in setup mode; if so the unit is likely toast and needs replacement. |
| Can't reach an **older glider** with a shared master | That glider's slave may not be set to "call all" / may have Slave Security on; needs the special cable to reconfigure (contact support). |
| Bench board powered but **no Freewave comms** | Confirm the glider-side modem has power — check voltage across the Freewave connector power pins; check TX/RX signal pins; confirm board is actually booting (a powered, booting flight board draws a few mA, not ~0). |
| Master not seen by **Dockserver** (rings, lights, but no pickup) | Confirm the right `/dev/ttyUSB*` is mapped to `freewave` in `dockServerState.xml`; verify you can reach the modem with `minicom` while Dockserver is stopped (rules out the cable/port). |
| Two gliders, one antenna | Operators have asked about a coax splitter feeding one antenna for dual-glider deployments — not a documented Teledyne setup; expect reduced link margin and test before relying on it. |

!!! tip "Local terminal access"
    For direct low-level access you can talk to the glider over Freewave with a
    terminal program such as `minicom` (see the Dockserver notes), or use
    `u4stalk` for a glider terminal session. The radios run at **19,200 N-8-1**
    in setup mode regardless of the link's communication baud.
