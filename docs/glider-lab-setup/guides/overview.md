---
title: Setting Up a Glider Facility
description: Summary of key considerations for establishing an underwater glider facility, covering facility design, budget, equipment, personnel, and communications.
---

# Setting Up a Glider Facility

*This guide summarises Chapter 1 of the OceanGliders Best Practices document, led by Jack Barth, Sandy Thomalla, Pedro Monteiro, and Sebastiaan Swart, with contributions from the global glider operations community.*

---

## 1. Introduction: Matching the Facility to User Needs

The success of glider-based observing relies on establishing an appropriately equipped, sized, and supported physical facility alongside a well-coordinated team with expertise across ocean science, engineering, IT, field operations, and outreach.

**The size and structure of a glider facility should match its observing goals.** These range from full-time, 24/7/365 monitoring of fixed sampling lines to short-term, intensive process studies. Key decisions that flow from those goals include:

- **Glider selection** — depth range, buoyancy displacement, speed, endurance, payload capacity, battery type, cost, and upgrade path. Note that requirements change as science evolves, so flexibility matters.
- **Operational range** — local deployments versus international shipping with customs and hazmat expertise.
- **Data services** — contributing raw data to a regional assembly centre versus operating a dedicated real-time, quality-assured data delivery system.
- **Uptime requirements** — in-house repair and refurbishment capability drives uptime but increases facility cost and complexity.

### Facility Models

| Model | Description | Trade-offs |
|---|---|---|
| Standalone (institutional) | PI- or university-led, flexible | Unstable funding, limited space to grow |
| National facility | Centralised, serves the community as a service | Adds friction between scientists and operators; requires strong visibility so it isn't underutilised |
| Hybrid / networked | Smaller operators collaborate with larger facilities | Balances diversity of expertise with access to a larger knowledge base (e.g. U.S. IOOS regional associations) |

!!! tip
    A well-designed facility can also provide leverage for sensor development, technology innovation, and student training beyond its primary observing mission.

---

## 2. Budget, Funding Model, and Sustainability

Budget drives many choices. Common cost categories that are sometimes overlooked:

| Category | Notes |
|---|---|
| **Gliders and sensors** | Include spares and components to minimise downtime |
| **Building** | Floor space, power, internet — allow room for expansion |
| **Maintenance equipment** | From basic tools to ballast tanks and pressure chambers |
| **Staff** | Technicians, pilots, managers, and admin |
| **Insurance** | Gliders are regularly lost or damaged at sea; options vary by country and institution |
| **Shipping** | International customs, ATA carnets, lithium battery hazmat certification |
| **Cyber infrastructure** | Iridium comms costs, server/cloud hosting, IT support |
| **Refurbishment / spares** | Ongoing wear-and-tear budget — often underestimated |
| **Batteries** | Expensive; lithium batteries cannot be shipped by air, so plan for long lead times |
| **Deployment/retrieval** | Boat hire including emergency rescue missions |
| **Fleet replacement** | Gliders have a finite lifespan; budget for rejuvenation |

### Funding Models

There is no single correct model. Considerations include:

- **Research-driven vs. cost recovery** — or a combination of both
- **Single PI vs. federal/core funding**
- **User charging** — a glider use fee (e.g. per 30 days at sea) is often necessary in multi-PI academic environments to build reserves for fleet upgrades and replacements, since grants rarely cover large capital impulses
- **Stakeholder buy-in** — potential users should be involved from the beginning, both to shape the facility and to help justify funding

---

## 3. Infrastructure

### 3.1 Physical Equipment

Equipment needs are driven by the mission types the facility will support. Key considerations:

- **Ballast tank** — at minimum, access to a tank for neutral buoyancy testing is strongly recommended
- **Pressure chamber** — required for self-reliance on pressure housing testing; otherwise ensure enough spare vehicles/sensors to accommodate manufacturer turnaround time
- **Sensor calibration** — some payloads (e.g. active acoustics) require specialised large tanks; others can be calibrated in-house or sent to the manufacturer
- **Spare parts and asset tracking** — track every component through its lifetime. Spreadsheets shared from experienced facilities are a practical starting point; dedicated asset management software may be warranted at scale
- **Handling equipment** — larger glider types require hoists, carts, and adequate storage space
- **Number of gliders** — maintain enough vehicles and components so that servicing one does not halt all operations

### 3.2 Information Technology

- Base stations and laptops running manufacturer glider control software — keep software current
- Redundant data storage, including at least one off-site or cloud copy, to protect against catastrophic loss
- Stable power with uninterruptible power supply (UPS) and backup generator for 24/7 operations
- Secure remote access to base stations for piloting from anywhere
- A modem fallback for communications if internet is interrupted — particularly important if multiple gliders call in simultaneously
- Establish a relationship with the host institution's central IT group; 24/7 operations will eventually generate out-of-hours IT needs

!!! note
    Small facilities without dedicated IT staff can use the manufacturer's hosted base station service for a fee. This trades flexibility for reduced administrative burden.

### 3.3 Shipping, Insurance, and Legal Compliance

- Expertise in international shipping and customs is essential for any facility that deploys outside its home country
- Lithium battery handling requires a certified dangerous goods person; storage and disposal must also comply with hazmat regulations
- Consider glider insurance against loss at sea, particularly for small fleets where a single lost vehicle would significantly impact operations. Pooled insurance among national facilities may offer better terms
- When operating in territorial waters, research permit requirements well in advance

---

## 4. Personnel

A successful glider operation requires a team with diverse and complementary skills. Key roles:

### 4.1 Glider Technicians

The core of any facility. Responsibilities include:

- Hardware and software repair, refurbishment, and upgrade
- Sensor payload configuration, ballasting, and communications testing
- Manufacturer liaison for diagnostics and refurbishments
- Field operations: packing equipment, coordinating with vessel captains, conducting deck and at-sea tests alongside the pilot

### 4.2 Pilots

Responsible for in-mission glider control, navigation decisions, and handoff documentation between shifts. Piloting may be performed by facility staff or by the science team depending on the facility model.

### 4.3 Additional Roles

- **Data processing and posting** — real-time QC, delivery to data assembly centres, FAIR compliance
- **IT support** — base station administration, cloud infrastructure, cybersecurity
- **Administrative support** — shipping coordination, insurance, customs, grant administration

### Team Structure

- Build a tiered structure — senior pilots and technicians mentor junior staff
- Follow and document best practices: repair logs, glider metadata, piloting decisions
- Regular communication within the team before, during, and after every mission is non-negotiable

!!! tip
    Consider whether a standalone full facility is warranted, or whether partnering with a larger regional or national facility for maintenance, calibration, and IT services is more efficient for your operation.

---

## 5. Science, Public, and Stakeholder Communications

Effective communication sustains a facility long-term by maximising utilisation, demonstrating impact, and attracting ongoing funding.

- **24/7 contact number** — post a monitored cell number on every glider: *"Oceanographic Research Equipment: If found adrift, please leave alone. If found ashore, please call X-XX-XXX-XXXX."*
- **Ocean user engagement** — meet with local fishing fleets, mariners, and harbour authorities to explain glider operations; provide data access instructions where data are public
- **Outreach** — gliders capture public imagination; use social media, press, and school engagement to build support
- **Website and branding** — a well-maintained website with mission plots, news, and contact information is a minimum requirement for any facility

---

## References

Barth, J. et al. (2021). *Setting up a glider facility.* OceanGliders Best Practices, Chapter 1. OceanGliders Best Practices Workshop.

GROOM (2014). D5.7 Report describing costs to build and operate the glider observatory infrastructure. [groom-fp7.groom-h2020.eu](http://groom-fp7.groom-h2020.eu/lib/exe/fetch.php?media=public:deliverables:groom_d5.7_cnrs.pdf)

GROOM (2015). D5.1 Ground segment description and the glider port concept. [groom-fp7.groom-h2020.eu](http://groom-fp7.groom-h2020.eu/lib/exe/fetch.php?media=public:deliverables:groom_d5.1_hzg.pdf)

Pattiaratchi, C. B., Woo, L. M., Thomson, P. G., Hong, K. K., & Stanley, D. (2017). Ocean glider observations around Australia. *Oceanography*, 30(2), 90–91. https://doi.org/10.5670/oceanog.2017.226
