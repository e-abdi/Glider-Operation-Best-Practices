---
title: Argos
description: The Slocum Argos PTT — a one-way 401 MHz satellite beacon for locating a glider in recovery. What it is, how c_argos_on activates it at the surface, its ~90 s transmit cadence as a source of electrical noise, service and IDs, message decoding, and testing.
---

# Argos

**Argos** is the Slocum's **one-way satellite position beacon** — the backstop that
lets you *find* a glider when the two-way links ([Iridium](../iridium/index.md) and
[Freewave](../freewave/index.md)) can't be reached. The glider carries a **Seimac
X-Cat PTT** (Platform Transmitter Terminal) whose 401 MHz antenna lives in the
[tail fin](../digifin/index.md) alongside the GPS/Iridium and Freewave antennas. It
transmits **last-known GPS positions** and the Argos network also derives **periodic
surface fixes accurate to ~100 m** from the bursts themselves.

Unlike Iridium, Argos is **transmit-only**: you cannot command the glider over it,
and you cannot send data down to it. It exists for one job — buying you a search
area when everything else is silent.

!!! info "Source"
    Paraphrased from the *Slocum G3 Glider Operators Manual* (Rev. 1, "Argos
    Satellite Platform Transmitter Terminal", "Communicating with Argos", and
    Appendix H), the *Slocum G3 Maintenance Manual*, the UG2 community Slack, and
    the Teledyne Webb Research user forum. This is a condensed field reference —
    always defer to the official Teledyne documentation, and contact
    `glidersupport@teledyne.com` (and **Service Argos**) before changing any Argos
    configuration.

---

## How Argos is activated

This is the question that trips people up: **Argos transmits only while the glider
is powered up at the surface — never underwater.** 401 MHz radio doesn't propagate
through seawater, so there is nothing to gain (and nothing emitted) while diving.
The PTT keys up only when the glider is sitting on top with its antenna in the air.

Behaviour is set by a single sensor, **`c_argos_on`**:

| `c_argos_on` | Behaviour |
|---|---|
| **< 0** | PTT **always off**, *even at the surface* |
| **0** (default) | PTT powered off underwater, but **auto-enabled at the surface** |
| **> 0** | PTT **powered on and transmitting** (`1` = no diagnostics; `2` = transmitted chars to MLOG/TERM; `3` = transmitted **and** received chars logged) |

- With the default `c_argos_on 0`, the glider brings the PTT up **on every
  surfacing** and shuts it off when it dives — so in normal operation it *is*
  pinging at the surface, just not all the time and not at depth.
- During an **abort**, the flight code turns on **all** communication and location
  devices (GPS, Argos, etc.) so you have every possible way to locate the vehicle.
- The **emergency circuit** independently powers the **Argos PTT** (along with the
  air pump and the jettison-weight burn wire). So even after the emergency battery
  takes over, Argos keeps transmitting — by design, because that is exactly the
  scenario where you need to find the glider. Note the emergency batteries are
  **not monitored**, so don't assume they're at full capacity after a deployment.

!!! tip "Taking Argos out of service to save power"
    Argos itself is **low-power**, so it's rarely worth disabling. One operator
    only removed it (`use - argos`) **out of desperation** months from a recovery
    window — it is not a meaningful power lever compared with the science bay or
    the Freewave [console](../../../piloting/slocum/power-saving.md). Leave it on
    unless you have a specific reason not to.

---

## The ~90-second ping is also a source of electrical noise

Argos doesn't sit quietly. The standard **repetition rate is ~90 seconds** (the
value you register with Service Argos), and each burst is **~1 W at ~401 MHz**.
That periodic, fairly strong RF transmission can **couple electrically onto other
sensor lines that share an A/D**, showing up as a **periodic spike in the data**.

- The classic symptom is **voltage spikes on `leakdetect_voltage` /
  `leakdetect_voltage_forward`** — identical in timing and amplitude (a tell-tale
  that the cause is *electrical*, not a real leak). When an operator reported this,
  TWR's **first suspect was coupling to Argos transmissions**; the next suspect was
  another device keying on the same A/D. These spikes appear **at the surface**,
  which lines up with Argos only transmitting up top.
- This is the **same family of problem** as the false [digifin leak detect](../digifin/index.md#leak-detect)
  aborts caused by Iridium line noise — an RF transmitter injecting noise into the
  leak-detect path. If you see periodic leak-detect dips that line up with comms,
  rule out RF coupling before you suspect water.

!!! note "90 s vs. \"every two minutes\""
    Operators often remember the cadence as *roughly every couple of minutes*. The
    **documented standard repetition rate is 90 s**; the exact spacing you observe
    can drift a bit and isn't perfectly regular, so don't be surprised if it looks
    closer to ~2 minutes in a given record. The takeaway is the *periodicity*, not
    the exact number.

---

## Service, IDs, and the antenna

- **Service Argos / CLS** administers the network. Submit a program application
  form to the **Argos User Office** (North America `useroffice@argosinc.com`,
  Australia/NZ `clsargos@bom.gov.au`, all others `useroffice@cls.fr`,
  <http://www.argosinc.com>); they return an acknowledgment, user manual, and IDs.
- You must provide the glider's ID in **both decimal and hexadecimal**. The
  **standard repetition rate is 90 seconds**. The ID lives in the glider's
  **`autoexec.mi`**.
- **Antenna integrity matters for recovery.** TWR specifically warns **against
  reflective tape on the fin** — testing showed it significantly degrades the
  antenna VSWR and can cause **very poor Argos/Freewave/Iridium performance**, the
  worst case being trouble locating a glider in distress. If you need to mark the
  glider, the suggested spot is the **aft cowling**, not the fin.

---

## Decoding Argos messages

Argos relays the glider's last-known GPS position (plus water-velocity estimates)
as a packed hex string delivered by **email or telnet** from your Argos account.

- The **message format depends on the transmitter and ID width.** Gliders with
  **X-Cat PTTs and 28-bit IDs** use the current format; older **20-bit IDs** use
  the **legacy** format. The relevant sensor is **`f_argos_format`**. See *Argos
  Data Format* in Appendix H for the byte-by-byte layout.
- A typical message carries an **age/timestamp**, a **valid** lat/lon, an
  **invalid** (lower-confidence) lat/lon, the **last too-far** fix, and water
  **v_x / v_y** (scaled by 0.05 before transmission — multiply by 0.05 to decode).
- TWR publishes a decode utility (under
  `…/glider/windoze/production/windoze-bin/`), and the forum has a platform-
  independent **open-source Python decoder** that parses the hex string bitwise
  (two's-complement handling for negative lat/lon and water velocity).
- If a glider is lost and you need fixes fast, contact Service Argos and ask them
  to enable **ALP (All Location Processing)** so you get the maximum number of
  derived positions. See the
  [emergency-recovery notes](../../../piloting/slocum/power-saving.md#staying-out-of-a-mission-lastgasp-and-reverting-settings).

---

## Testing Argos

Argos satellites are in **polar orbits**, so coverage at any one spot comes and
goes — give the test plenty of time.

1. Put the glider **outside with a clear view of the entire sky** — *not* deployed,
   ideally **on a bench power supply** to save battery.
2. Power up, `ctrl-c` to GliderDOS, then:
   ```
   lab_mode on
   use - iridium
   ```
   (taking Iridium out of service keeps it from competing while you let Argos run).
3. **Let it transmit for ~3 hours** (1–3 h) so multiple passes get through.
4. `exit`, bring the glider in, and power off.
5. Log in to **Service Argos / CLS America** and confirm hits were received for the
   glider's **ID** (from `autoexec.mi`). You can also email Service Argos
   (`useroffice@cls.fr`) to request the data.

!!! tip "Confirming transmissions locally — no network needed"
    To verify the PTT is keying without waiting on the satellite network, use an
    **RF detector/receiver sensitive to 401.650 MHz ±30 kHz**. These range from a
    cheap passive **chirper** up to a handheld **TSUR-400 Argos receiver**, which
    shows the unit ID, the data bytes received, and some diagnostics. On the glider
    in PicoDOS, the legacy `talk arg` command keys the transmitter; every ping
    prints `Transmitting / Send Data Now:` — odd-looking, but correct.

!!! warning "PicoDOS / `talk arg` is lab-only"
    `talk arg` lives in **PicoDOS** — **never enter PicoDOS on a deployed glider**;
    it drops the flight code. Use it only on the bench.

---

## Field troubleshooting

| Symptom | Things to check |
|---|---|
| Argos shows **no hits** in a test | Needs **1–3 h** of clear sky (polar-orbit coverage gaps); confirm `c_argos_on` ≥ 0 and the **ID** (decimal **and** hex) in `autoexec.mi`; confirm the account is active with Service Argos. |
| **Periodic spikes** on `leakdetect_voltage` (or false leak/digifin aborts) at the surface | Suspect **RF coupling from the Argos burst** onto the shared A/D (identical-timing/amplitude spikes ⇒ electrical, not water). Same family as [Iridium-line-noise false digifin leaks](../digifin/index.md#leak-detect). |
| Glider in distress is **hard to locate** | Confirm Argos is on; ask Service Argos to enable **ALP**; check the fin antenna isn't degraded (**no reflective tape on the fin**). Pair with a [pinger](../digifin/index.md) and strobe for recovery. |
| Want to **save power** with Argos off | Rarely worth it — Argos is low-power. Only `use - argos` as a last resort far from recovery; revisit the [power-saving page](../../../piloting/slocum/power-saving.md) first. |

!!! note "Argos is for finding, not flying"
    Argos sends position **only** — you cannot command the glider over it. It is the
    one-way backstop that turns a lost glider into a search *area*, which is why it
    (and a [pinger](../digifin/index.md) and strobe) factor into every recovery
    plan. For two-way comms, see [Iridium](../iridium/index.md) and
    [Freewave](../freewave/index.md).

!!! tip "Quick reference"
    | Item | Command / sensor |
    |---|---|
    | Enable / disable PTT | `c_argos_on` ( <0 off · 0 auto-at-surface · >0 on ) |
    | Take Argos out of service (power) | `use - argos` |
    | Message format selector | `f_argos_format` |
    | Glider ID (decimal **and** hex) | in `autoexec.mi` |
    | Standard repetition rate | **90 s** |
    | Transmit frequency / power | **~401 MHz**, **~1 W** (RX detect 401.650 MHz ±30 kHz) |
    | Local test receiver | TSUR-400 / passive chirper |
    | Manual key (lab/PicoDOS only) | `talk arg` |
    | Emergency position processing | ask Service Argos to enable **ALP** |
