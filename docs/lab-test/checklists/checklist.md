---
title: Lab Test Checklist
description: Printable pre-deployment lab test checklist covering bench tests, comms, sensors, and pressure testing.
---

# Lab Test Checklist

[Print this page :material-printer:](#){ .print-button onclick="window.print(); return false;" }

---

**Date:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Operator:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Glider S/N:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ &nbsp;&nbsp; **Mission #:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## 1. Pre-Test Setup

- [ ] Lab setup complete and Lab Setup Checklist signed off
- [ ] Mission plan approved and parameter configuration document available
- [ ] Battery charged and voltage verified: \_\_\_\_\_\_\_\_ V (required minimum: \_\_\_\_\_\_\_\_ V)
- [ ] All hull sections opened, O-rings inspected, hull sections closed and torqued
- [ ] Test equipment on bench and deck unit powered on without fault codes

## 2. Power and Comms

- [ ] Vehicle boots without fault codes (record any warnings: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_)
- [ ] Reported battery voltage matches independent measurement (within 0.1 V)
- [ ] System clock set to correct UTC time
- [ ] Deck unit communication established; test command set completed successfully
- [ ] Satellite modem acquires network registration (note: full data transfer not required for bench test)
- [ ] GPS fix acquired (or deferred to outdoor pre-deployment check — document reason: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_)
- [ ] Acoustic modem initialises without fault (if fitted)

## 3. Sensor Checks

- [ ] All science sensors initialise without error codes
- [ ] CTD data compared against reference — temperature offset: \_\_\_\_\_\_ °C, salinity offset: \_\_\_\_\_\_ PSU
- [ ] Dissolved oxygen sensor verified against saturation reference (if fitted)
- [ ] All sensor data streams confirmed logging to vehicle file system
- [ ] Any sensor anomalies documented in lab test log with disposition

## 4. Simulated Dive

- [ ] Actual deployment mission file uploaded to vehicle (not a generic test file)
- [ ] Mission simulation executed: buoyancy engine commands verified correct
- [ ] Pitch battery and fin commands observed and match planned profile
- [ ] Abort threshold test: low battery simulation triggers abort correctly
- [ ] Abort threshold test: depth exceedance simulation triggers abort correctly
- [ ] Vehicle targets recovery waypoint correctly on abort

## 5. Post-Test

- [ ] Pressure test completed to specified pressure \_\_\_\_\_\_\_ bar for \_\_\_\_\_\_\_ minutes — result: Pass / Fail / N/A
- [ ] No leaks observed at any seal or connector face during or after pressure test
- [ ] Lab test data file downloaded and verified (all sensor, event, and mission logs present)
- [ ] Data file archived to: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_
- [ ] Vehicle file system cleared of test data; operational mission file loaded and confirmed
- [ ] Mission Lead notified: vehicle cleared for deployment

---

## Sign-Off

| Role | Name | Signature | Date |
|---|---|---|---|
| Operator | | | |
| Reviewer | | | |

---

*Lab Test Checklist — v1.0*
