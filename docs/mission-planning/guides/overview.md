---
title: Pre-deployment Preparation and Operations
description: Summary of pre-deployment planning, logistics, glider and sensor preparation, operations, piloting, and documentation based on the OceanGliders Best Practices Chapter 2.
---

# Pre-deployment Preparation and Operations

*This guide summarises Chapter 2 of the OceanGliders Best Practices document, led by Josh Kohut and Alvaro Lorenzo Lopez, with contributions from Nicole Waite, Estelle Dumont, Gillian Damerell, Dave Aragon, Steve Woodward, Victor Turpin, Adam Comeau, Theodore Thompson, and Tania Morales.*

---

## 1. Pre-deployment Preparation

Glider deployments begin with a clear and communicated mission plan that enables proper planning and implementation throughout the mission — from pre-deployment preparation to recovery and post-deployment checks.

### 1.1 Mission Planning

All mission plans should start with a clear statement of the science and monitoring objectives, developed by the PI/Lead Scientist and communicated to the deployment team. At minimum, the plan should capture: required **track and/or area of operation**, **sensors**, **science sampling configuration**, and **mission duration**. The plan should be signed off by both the science lead and the glider logistics lead before any glider preparation begins.

Planning timelines are mission-dependent. The phases below are indicative minimums for straightforward missions and should be extended significantly for complex or international deployments.

#### More than 1 year before deployment

- Define the broad mission plan: area, timescales, glider behaviour (e.g. endurance line, station-keeping), sensor requirements, deployment/recovery options
- Assess major obstacles or show-stoppers: environmental, technical, operational, legal
- Discuss scientific sensor and depth requirements between researchers and the technical team
- Calculate endurance requirements accounting for duration/distance goals, payload, and environment (depth, stratification, currents)
- Calculate the total number of vehicles required across the project
- Resource plan: glider and sensor availability, required maintenance and purchases, vessel availability, qualified personnel (including training/hiring needs)
- Estimate mission costs: staff, vessels, shipments, insurance, batteries, spares, sensor calibrations, Iridium/Argos communications
- Contingency planning: emergency recovery, back-up glider
- Establish a rough project timeline and engage stakeholders and international partners

Establish lead times and deadlines as early as possible — especially for glider and vessel availability, equipment purchases, shipping (including customs), and diplomatic clearance applications.

#### 6 to 12 months before deployment

- **Risk analysis:** Detailed assessment of the area of operation (shipping traffic, fishing, ice cover, currents); establish mitigation measures; assess insurance options; compile a list of potential emergency recovery vessels
- **Legal requirements:** Diplomatic clearance is required for gliders operating in foreign waters. Application deadlines vary widely between countries (6 months to 2+ years). Local notifications may also be required: Notice to Mariners, navigational warnings, sub-nav warnings, marine equipment deployment authorisations, harbour master notifications
- **Pilot training:** If new pilots are needed, training should begin as early as possible

#### 1 to 6 months before deployment

- **Detailed mission plan:** Timelines, waypoints, survey patterns, sensor sampling configurations; define roles, communication methods/frequency, and the piloting rota
- **Glider preparation:** Configure the mission on the piloting interface and data transfer systems
- **Logistics:** Arrange equipment shipments, staff travel, vessel bookings
- **Health and safety:** Write or update the Risk Assessment and Standard Operating Procedure; familiarise all personnel with them
- **Data and metadata:** Set up data flow, create repositories, follow DAC file naming conventions, set up automated data transfers, create metadata files — do this before the mission, not during

### 1.2 Mission Logistics

Logistics must be considered from the very beginning of planning. Key considerations:

- **Domestic shipments:** Hazardous material classification and delivery timelines
- **International shipments:** ATA carnets (typically valid for < 2 years), commercial invoice, customs documentation, customs delays (2+ weeks are common)
- **Dangerous goods certification:** Lithium batteries require appropriate DG certification for each mode of transport (air vs. sea freight — each has separate requirements). Air freight for lithium batteries is extremely restricted
- Notify third-party recipients of hazardous goods in advance

### 1.3 The Glider Vehicle

- Follow manufacturer recommendations for component service intervals; maintenance frequency varies with glider type, use, and age
- Routine maintenance items: pumps, air bladders, fins, O-rings — rubber components can dry-rot even without use
- Re-calibrate sensors in-house or with the manufacturer on the recommended schedule
- Review maintenance and calibration history before each mission preparation to identify any preemptive service needs
- Fault tracking and maintenance records should be associated with individual **sub-components**, not just gliders, so that history follows the part when components are swapped between vehicles
- **Ballasting:** The glider must be ballasted for the expected water density range at the mission location and time of year. Use recent CTD casts, historical records, or ocean models. Key targets: lowest surface density, coldest surface water, and densest bottom water for the full deployment span. Surfacing reliability is the primary constraint
- Consider labels/signage on the glider: include contact information and, for high-traffic areas, consider multiple languages. "Scientific Research" labels with a mission end date help deter premature recovery by well-meaning third parties

### 1.4 The Integrated Sensors

- The sensor payload has implications for the glider's energy budget and hydrodynamics — choose carefully
- Annual factory calibration is standard for most sensors; adjust schedules for biologically active deployments
- If timing prevents recalibration before a time-sensitive mission, evaluate the sensor against a calibrated reference and document the result
- Document all calibration and maintenance activity in the mission metadata
- Refer to sensor-specific SOPs from the OceanGliders community

---

## 2. Operations

### 2.1 Launch and Recovery

General principles that apply in all cases:

- Clearly separate responsibilities between the **field team** (on deck) and the **pilot team** (remote) before departure — agree this in advance, not at sea
- Pre-launch checklists must be available to both teams; completed checklists must be archived
- Agree and test the communication protocol between pilot and field team before departure; prefer message-based over voice; keep comms minimal during launch/recovery

**Before launch:**
- Hold a toolbox talk covering: glider overview, lifting points and delicate parts, personnel responsibilities, time estimate for the procedure, and the go/no-go authority
- Assemble equipment for all possible recovery methods before the glider is in the water
- If weather does not permit an immediate emergency recovery, do not deploy
- Perform a CTD cast or tethered buoyancy check immediately before launch to verify ballast

**At launch:**
- The pilot performs a final functional test and gives the go/no-go
- Visual contact must be maintained with the glider until it leaves the surface
- Carry out progressive test dives (starting shallow); field team should remain in the area until the pilot gives the all-clear
- In-situ sensor validations (CTD casts, Niskin samples) should be performed at launch and recovery where possible

Investigate emergency recovery options during mission planning: local contacts may include shipping agents, harbour authorities, coast guard, fisheries enforcement, and local fishing vessels.

### 2.2 Piloting

#### Team structure

- The number and experience level of pilots must be considered during planning
- Groups with 3 or fewer pilots may struggle on longer missions
- Newly trained pilots must be supported by an experienced pilot initially; launch piloting must be done by an experienced pilot
- An escalation list of emergency contacts must be available to all pilots
- A piloting rota is essential; handover documentation must be rigorous — shared log, email handover, or a shared system; the methodology must be completely clear to all pilots

#### Pre-deployment and deployment piloting

- Review functional test results; set up first dive parameters and directives (waypoints, behaviours, sensor sampling rates); verify the piloting alert system
- Liaise with the field team on-site conditions (weather, timings, ship traffic); check external sources (weather forecasts, AIS, ice maps)
- After launch: confirm Iridium comms, check all surface readings (GPS, leak/pressure, battery voltages, attitude) before sending the glider diving
- Increase dive depth progressively over the first few dives; review glider performance (trim, trajectory, sensor data) before committing to full depth

#### Day-to-day piloting

The glider must be checked daily (ideally several times per day). Each check should cover:

- Error messages
- Glider location and waypoint adherence
- Flight performance: vertical velocities, pitch, roll, and steering
- Internal readings: leak sensors, internal pressure, humidity
- Energy usage and battery voltage trends
- Iridium communications quality
- Altimeter performance
- Sensor data quality: realistic values, no spikes, no timeouts

The on-call pilot must respond to alerts 24/7 during their shift and escalate unusual situations to a more experienced pilot. Any parameter or file change must be logged with a comment.

#### Recovery piloting

- Shorten underwater segment duration in the hours before recovery to reduce surface waiting time
- Set an appropriate call rate once the glider is at surface; monitor AIS for collision risk
- Verify glider safety parameters (leak, pressure, temperature, humidity) and give the field team the all-clear before they handle the vehicle

#### Longer-term mission monitoring (experienced pilot)

- Ensure key science objectives and KPIs are being met
- Liaise with the PI regularly on any science changes or notable sensor anomalies
- Monitor battery usage against capacity limits; evaluate energy-saving measures
- Track environmental hazards and opportunities at a larger scale (eddies, sea ice, shipping)
- Ensure regulatory notifications are filed at the required times (e.g. Notice to Mariners, EEZ entry notifications)
- Ensure an experienced pilot is available at all times for technical emergencies

#### Area-specific considerations

| Area | Key risks and strategies |
|---|---|
| **Coastal** | Ship traffic, fishing gear, tidal and persistent currents, river plumes, shallow water. Use marinetraffic.com, local fisheries/coast guard contacts |
| **Polar / ice** | Ice prevents surfacing → entering recovery mode under ice = likely loss of vehicle. Disable weight-drop behaviour. Minimise surface time in forming ice. Treat recovery as a bonus, not a given |
| **Open ocean** | Generally safest. Conservative battery management essential; limited emergency recovery options. Monitor seamounts |
| **Shelf break** | Rapidly changing bathymetry: monitor altimeter frequently, adjust settings often. Fishing/trawling risk; consider minimising bottom time |
| **Strong currents** | Use autonomous navigation modes for predictable flows; longer-term path planning (altimetry, models) for eddies and episodic currents |
| **Storm-prone areas** | Minimise unnecessary surfacings. Consider deeper upper inflection if near-surface data not required |

#### Sampling configuration

- Balance satellite cost and time budget against spatial/temporal resolution needs
- NRT data should at minimum resolve larger-scale features (surface and bottom temperature)
- Obtain sequential dive and climb data where possible to allow correction of sensor hysteresis and lag
- Typical sampling intervals: 4–60 seconds or 0.5–10 m depending on mission requirements
- Be mindful of sensor interoperability: e.g. pumped CTDs can interfere with passive acoustic sensors; switched-power sensors can introduce noise

### 2.3 Training

Training spans three areas: **maintenance/refurbishment and ballasting**, **piloting**, and **fieldwork**.

- Manufacturer courses (typically 4–5 days) cover the basics of all three; new operators are strongly encouraged to attend
- Supplement manufacturer training with institution-specific procedures, piloting logs, and communication protocols
- Trainee pilots should shadow experienced pilots and gradually take over with experienced backup
- Informal communication channels (Slack, Teams) help inexperienced pilots understand decision-making
- Field teams should always include at least one experienced person; toolbox talks with all deployment/recovery personnel are required
- The EGO Glider School at PLOCAN (https://gliderschool.eu) is an international training resource held annually

### 2.4 Post-recovery Activities

- Follow a post-deployment checklist to ensure complete vehicle check-in
- Inspect the glider for leaks, hardware faults, and any physical damage
- Analyse mission oddities, warnings, and aborts
- Cross-check sensors (CTD comparison, optode check-in, LISST baselines) for validation, drift, or data quality issues
- Download, archive, and submit the full high-resolution dataset to the appropriate databases

---

## 3. Documentation and Metadata

### Pre-deployment checklists

Pre-deployment checklists should cover: O-ring cleaning/replacement, data back-up and software updates, battery checks, pitch/ballast/fin motor checks, communications tests, compass calibration, altimeter functionality, and sensor validation. Completed checklists must be archived.

### Sensor calibration records

Calibration sheets from the manufacturer or in-house facility should be archived at the facility and data centre levels. Coefficients must be updated onboard the glider and/or in the processing system.

### Minimum metadata requirements (OceanOPS)

| Field | Notes |
|---|---|
| Programme | |
| WMO ID | |
| Principal Investigator | |
| Deployment lat/lon/time | Approximate is acceptable at planning stage |
| Operating agency | |
| Sensor models | Controlled vocabulary — see OG format manual |
| Glider model | Controlled vocabulary |
| Glider serial number | |

!!! tip "Submit metadata before deployment"
    During and after a mission, metadata submission is rarely a priority. Collect and submit metadata — including setting up the data flow with your DAC — **before** the mission starts. Notify the DAC and OceanOPS at deployment, and again at mission completion.

### Data flow setup

Contact your regional Data Assembly Centre (DAC) before mission preparation to clarify data and metadata submission procedures. If no national DAC is available, existing DACs can support data processing — arrange this arrangement well in advance, not during mission preparation.

---

## References

Kohut, J. et al. (2021). *Pre-deployment preparation and Operations.* OceanGliders Best Practices, Chapter 2.

OceanOPS metadata standard: https://www.ocean-ops.org/metadata/

OceanGliders format user manual: https://github.com/OceanGlidersCommunity/OG-format-user-manual

Rutgers pre/post-deployment checklists: https://rucool.marine.rutgers.edu/data/underwater-gliders/glider-operation-checklists/

EGO Glider School (PLOCAN): https://gliderschool.eu/
