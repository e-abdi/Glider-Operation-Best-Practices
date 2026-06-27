---
title: Iridium
description: What the Slocum Iridium satellite modem does, RUDICS vs. dial-up (PSTN), the primary/alternate numbers, the surface comms sequence, SIM cards and service, testing with callback, and data transfer. (The one-way Argos beacon has its own page.)
---

# Iridium

**Iridium** is the Slocum's satellite link and the **primary way
you talk to a glider once it is deployed** and out of Freewave range. The glider
carries an **Iridium 9522b** bidirectional satellite modem on the lower
electronics tray; a low-noise-amplifier (LNA) switch board lets the modem **share
its quad-helix antenna with the GPS** (Iridium ~1626 MHz, GPS 1575 MHz), so the
glider can fix its position and then call home through the same antenna in the
tail.

Where [Freewave](../freewave/index.md) is fast, free, and line-of-sight, Iridium
is **slow and metered but global**: when the glider surfaces anywhere in the
world with a clear view of the sky, it can reach your Dockserver.

!!! info "Source"
    Paraphrased from the *Slocum G3 Glider Operators Manual* (Rev. 1, "Iridium
    Satellite Telemetry", "Glider Communications", and Appendices G and H), the
    UG2 community Slack, and the Teledyne Webb Research user forum. This is a
    condensed field reference — always defer to the official Teledyne
    documentation for your specific glider, and contact
    `glidersupport@teledyne.com` before changing SIM, phone-number, or Argos
    configuration.

---

## How the call reaches shore: RUDICS vs. dial-up (PSTN)

When the glider dials in, energy leaves the tail antenna, **bounces satellite-to-
satellite** across the Iridium constellation, and comes down at a **ground
station**. What
happens *after* the ground station is the difference between the two transports:

| Transport | Path after the ground station | Notes |
|---|---|---|
| **RUDICS** (recommended) | Patched onto the **internet** to a dedicated IP — your **Dockserver** | More robust connections, **~half the cost** (roughly **$0.60/min** vs. ~$1.00–1.20/min). The Dockserver must be configured for a network connection. |
| **Dial-up (PSTN)** | Out into the **phone network** to a shoreside modem | The legacy path. A **modem** must sit on a **copper-lined, dedicated phone jack**; university switchboards and some carriers often will not pass the data call. |

- **RUDICS is the modern primary.** Today the glider's *primary* number is a
  RUDICS connection, with a **dial-up modem kept as the backup** in case the
  RUDICS host goes down.
- The carrier matters for dial-up: operators have had data calls that worked on
  one phone carrier simply **stop passing data** on another — if you run a PSTN
  backup, test the actual data call, not just the ring.

---

## Primary and alternate numbers

The **primary and alternate phone numbers** the glider dials live in its
**`autoexec.mi`** (in the `config` directory). You can override one temporarily
with `put` to test, but the persistent values belong in `autoexec.mi`.

- The alternate exists as a **backup** so a glider isn't cut off if the primary
  host fails (the feature was added after an operator lost a full day of comms to
  a shoreside power outage).
- The backup logic is **more nuanced than a simple "try A, then B"** — confirm
  how your firmware and Dockserver are configured rather than assuming, and test
  both numbers before relying on the fallback.

---

## The surface comms sequence

Every time a surface behavior brings the glider up, it runs the same sequence —
worth knowing because it explains *when* and *how* you get a console:

1. **GPS fix first** — the glider tries to fix position for up to **300 s** (5
   min). Older/slow GPS modules are why some groups raise this.
2. **Hand off to comms** — once it has a fix it establishes a console: it
   **prefers Freewave if a carrier is present**, otherwise it **dials Iridium**.
3. **Surface dialog** — it prints the surface dialog and **waits ~5 minutes** for
   you to act (end mission, send data, send in new `.ma` files, retask waypoints
   or behaviors, etc.). Every option is reminded to you in the dialog itself.
4. **No input → continue** — if nobody (or no [script](../../../piloting/slocum/power-saving.md))
   interacts within the wait window, the glider simply **resumes the mission as
   written**.

!!! tip "Force the Iridium call when simulating on the bench"
    Because the glider prefers Freewave, a bench glider in range of a master never
    calls Iridium on its own. The surface-dialog argument **`force_iridium_use:
    1.0`** in a `surfac*.ma` file (or dropping master power at the GPS-fix point)
    forces the Iridium call so you can watch the whole dive-to-call cycle. See the
    [Freewave page](../freewave/index.md#freewave-vs-iridium-during-a-mission) for
    how the two links arbitrate.

---

## Iridium vs. Freewave during a mission

- **In GliderDOS**, Iridium is the primary route and can run **alongside** a
  Freewave connection at the same time.
- **Mid-mission**, the glider picks **one**: it uses Freewave if a carrier is
  present and only calls Iridium when Freewave is absent. Data transfers the same
  way — over Iridium **only if** Freewave isn't available, unless you force it.
- **Force a transfer over Iridium** with the `-f=irid` flag, e.g.
  `S -f=irid -num=3 *.sbd *.tbd`.

A neat side effect of two-way Iridium: you can use the glider as a (very
expensive) **text relay** to talk to a field/deployment crew — passing command of
the vehicle back and forth between shore and boat through the glider.

---

## SIM card and service

- The Iridium phone and **SIM card are configured at the factory** (`talk
  iridium` in PicoDOS). **Depinning** a SIM is normally a factory step — only
  needed if you install your own card or change services, and best done with
  Teledyne's help.
- Buy a **data-only** commercial Iridium SIM — no extra equipment is needed.
  Several resellers serve glider users (e.g. **NAL Research**, **JouBeh**, CLS
  America, others). The card **must be activated ~30 days before shipment**, and
  Teledyne needs the card and unlock PIN during manufacturing.

!!! note "Budgeting airtime"
    Billing is monthly and metered. A reference figure from one user is **~90
    minutes/day per glider** with data-reduction techniques applied — on the order
    of **~$100/day**. Expect **significantly more on your first deployment** while
    you monitor, test, and learn; ~75–90 min/day is a steady-state plan.

---

## Testing Iridium

Place the glider **outside with a clear view of the sky** (buildings, hills, and
cars degrade the link far more than open ocean does), then use **`callback`**:

| Command | Effect |
|---|---|
| `callback 0 0` | Dial the **primary** number **immediately** |
| `callback 1 1` | Dial the **alternate** number in **1 minute** |
| `callback 30 0` | Dial the primary number in **30 minutes** |

- **30 minutes is the maximum** callback interval.
- Watch **`m_iridium_signal_strength`** (0 = no signal, 5 = max).
- Connection time varies with cloud cover and satellite availability;
  [gpredict](http://gpredict.oz9aec.net/) can confirm coverage for a test window.

!!! warning "PicoDOS is lab-only"
    `talk iridium` (and manual `AT`-dialing) live in **PicoDOS** — **never enter
    PicoDOS on a deployed glider**; it drops the flight code, leaving an expensive
    computer doing nothing but looking for comms. For manual dialing in the lab:
    `AT 001 <number>` (commercial card) or `AT 00697 <number>` (military card);
    `ata` answers, `ath` (or control-C) hangs up.

---

## Data transfer over Iridium is slow — plan for it

Iridium bandwidth is low, so **surface time is dominated by how much science data
you ship**. Practical guidance:

- Aim for **~10–20 minutes** of surface time per call. Much beyond that and you
  accumulate **surface drift** (the glider is pushed by wind/current the whole
  time it sits up top) — and you're paying by the minute.
- If you routinely exceed 20 minutes, you're probably sending **too much** —
  trim `sbdlist`/`tbdlist`, decimate, or sample on the downcast only.
- **Simulate a real dive's worth of data in the lab** and try the transfer before
  deploying; one second of simulation = one second of real time, so you'll quickly
  see if your data volume is unrealistic.
- The G3's **high-speed wired comms port** transfers roughly **5× faster** than
  Iridium/Freewave for bench data offload — use it in the lab rather than waiting
  on the radio. (G1/G2 had no speed advantage from a wire.)

---

## Argos — the one-way emergency position beacon

The glider also carries **Argos**, a **one-way** 401 MHz satellite beacon (the
**Seimac X-Cat PTT**) used to **locate** a glider when Iridium and Freewave can't
be reached. It is a separate system from the two-way Iridium link covered here —
it sends position only, you can't command the glider over it, and its periodic
~90 s transmissions can even **couple electrical noise** onto other sensor lines.

➡️ **See the dedicated [Argos page](../argos/index.md)** for activation
(`c_argos_on`), the noise behaviour, service/IDs, message decoding, and testing.

---

## Field troubleshooting

| Symptom | Things to check |
|---|---|
| Glider won't connect over Iridium at the surface | Clear sky? Check `m_iridium_signal_strength`; confirm the primary number/RUDICS host and Dockserver network config; try `callback 0 0`. |
| Calls connect but **drop frequently** | Common near buildings/hills during lab testing; usually fine in open ocean. On dial-up, suspect the carrier/jack — test the actual data call. |
| Dial-up backup never passes data | U.S. Robotics modem must be on a **copper-lined dedicated jack**; switchboards and some carriers won't pass it. |
| Surfaced in range but glider **calls Iridium instead of Freewave** | Expected — the carrier didn't latch in the brief window; issue `callback`. See the [Freewave page](../freewave/index.md). |
| Airtime bill far higher than expected | You're shipping too much data — reduce surface time to 10–20 min, decimate, downcast-only sampling. |

!!! tip "Quick reference"
    | Item | Command / sensor |
    |---|---|
    | Dial primary now | `callback 0 0` |
    | Dial alternate in 1 min | `callback 1 1` |
    | Callback in 30 min (max) | `callback 30 0` |
    | Signal strength (0–5) | `m_iridium_signal_strength` |
    | Force file transfer over Iridium | `S -f=irid …` |
    | Force an Iridium call (sim) | `force_iridium_use: 1.0` in `surfac*.ma` |
    | Manual modem (lab/PicoDOS) | `talk iridium`, `AT 001 <num>`, `ata`, `ath` |
    | Phone numbers | primary/alternate in `autoexec.mi` |
