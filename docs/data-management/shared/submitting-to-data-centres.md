---
title: Submitting to Data Centres
description: How glider data reaches data assembly centres — the US IOOS Glider DAC (registration, WMO IDs, real-time and delayed-mode files, FTPS upload, marking a deployment complete for NCEI archiving, the GTS), Coriolis and the EGO network, OceanOPS, and how Seaglider and Slocum pipelines produce the files.
---

# Submitting to Data Centres

A **data assembly centre (DAC)** collects glider data from many operators,
checks it, serves it to the public and passes it on: to weather and ocean
forecast centres in near real time, and to long-term archives once a
deployment ends. Sending data is usually a funder requirement, and it is
what makes a deployment visible to the rest of the community.

!!! info "Source"
    Paraphrased from announcements by the US IOOS Glider DAC team in the
    UG2 Slack #data channel (2024–2026), the Glider DAC submission
    documentation, the basestation3 GliderDAC extension and its sample
    configuration files, OceanGliders and Coriolis announcements, and
    operator correspondence. Procedures, server names and deadlines change:
    check the DAC's current documentation before setting up a pipeline.

---

## Which data centre?

| Data centre | Who uses it | Format | What it does with the data |
|---|---|---|---|
| **US IOOS National Glider DAC** (GDAC) | US operators, and others who choose it | NGDAC netCDF v2, one file per profile | Public ERDDAP and THREDDS, map portal, GTS via NDBC, archive at NCEI |
| **Coriolis / EGO** | European operators | EGO netCDF (Coriolis decoder) | GDAC for EGO, real-time QC, GTS |
| **OceanOPS** | Everyone (metadata, not data) | Deployment metadata | Tracks where gliders are, issues and links WMO IDs, publishes activity maps |
| National or project centres | Varies | Varies | Often mirror to one of the above |

Not every deployment reaches a DAC. Many groups never share their data
operationally, so a DAC map alone under-counts glider activity in a region.
Registering every deployment with OceanOPS, even when the data stays
private, at least makes the activity visible.

---

## The US IOOS Glider DAC

### 1. Register the deployment

1. Get a **provider account** on the Glider DAC providers page.
2. **Create a deployment** before the glider goes in the water. The
   deployment name is the glider name plus its start time
   (`<glider>-<yyyymmddTHHMM>`), and it becomes the upload directory.
3. **Request a WMO ID** if the data should go to the GTS. The DAC handles
   WMO ID requests as part of its core service. Put the ID in the file
   metadata (`wmo_id`).

### 2. Produce the files

The DAC accepts two kinds of file in a deployment directory:

| File | Contents |
|---|---|
| `glider_yyyymmddTHHMMSSZ.nc` | Real-time or near real-time data, usually a subset of the full resolution |
| `glider_yyyymmddTHHMMSSZ_delayed.nc` | Delayed-mode data, normally sent after recovery from the full-resolution files. A quality assessment is welcome but not required |

Both are one file per profile in NGDAC netCDF v2 (see
[Data Formats & Standards](formats-and-standards.md#us-ioos-ngdac-netcdf-v2)).
Run the IOOS Compliance Checker on a few files before the first upload.

### 3. Upload

- Upload by **FTPS** to `gliders.ioos.us`. Plain FTP was switched off on
  31 July 2026, and the older `ftp.gliders.ioos.us` host name is being
  retired. Update scripts and basestation push files to match.
- Upload into the deployment directory you registered.
- Files are picked up automatically and appear on the map and ERDDAP.

### 4. Check the data on the DAC

Look at your deployment on the DAC map or ERDDAP, not only on your own
plots. Problems that only show up downstream:

- **Units.** Conductivity labelled S/m but sent in mS/cm (a factor of 10)
  produced impossible salinity and density on the DAC while the operator's
  own plots looked normal.
- **Density.** The DAC computes and plots density; check whether it is
  in-situ or potential before comparing with other sources.
- **Missing files after an outage.** The DAC has had FTP outages and
  full-disk events. After any announced problem, check that every file
  from the affected period arrived, and re-upload the missing ones.

### 5. Mark the deployment complete

When the mission is over and the delayed-mode files are in, **mark the
deployment as completed** on the providers page. Only completed
deployments are sent to **NCEI** for archiving. Deployments left open also
keep being re-plotted by the DAC, which has caused real server load
problems.

### QC on the DAC

The DAC reads **QARTOD aggregate flags** for temperature and salinity, and
NDBC uses them when it sends the data to the GTS and forecast models. So
real-time QC flags in your files have a direct effect on what the forecast
centres use. See
[QARTOD](../slocum/data-processing-qc.md#automated-qc-qartod).

!!! note "Service level"
    In 2025 the DAC's support was cut back to mission-critical work: data
    ingestion, keeping data accessible, GTS submission, troubleshooting data
    flow and WMO IDs. Development and non-essential QC improvements were
    paused. Keep reporting problems to DAC support, but expect fixes for
    anything beyond data flow to take longer.

---

## Coriolis and EGO

In Europe, glider data goes to **Coriolis** in the EGO format. The
**Coriolis decoder** converts raw glider data to EGO and applies real-time
QC on the way:

- It reads Slocum and SeaExplorer data and Seaglider per-dive netCDF files.
- It runs as a MATLAB toolbox or as a free runtime version that needs no
  MATLAB licence.
- Coriolis can run the decoder for you if you send raw data and
  deployment metadata; check with them what they need.

Real-time EGO data goes to the GTS from Coriolis. Delayed-mode files can
be produced later from the full-resolution data.

---

## OceanOPS

OceanOPS is the WMO/IOC centre that monitors ocean observing platforms. For
gliders it:

- keeps track of deployments, including ones whose data is never shared;
- links each platform to its WMO ID;
- publishes regional and global maps of glider activity.

Tell OceanOPS about each deployment, ideally before it starts.

---

## Producing the files

### Seaglider

The basestation's **GliderDAC extension** writes NGDAC files from the
per-dive netCDF as each dive comes in:

- **Configuration** sits in three YAML files that override each other: a
  base file for all your Seagliders (creator, licence, standard variable
  attributes), a project file, and a deployment file (WMO ID, instrument
  serial numbers and calibration dates, and which per-dive variables map to
  which output names, for example oxygen or fluorescence). They are named
  in the glider's `.conf` file. The basestation ships commented examples.
- **Enable it** in the glider's `.extensions` file.
- **Timeseries or binned** output, set by a bin width (0 = timeseries).
- **QC**: only points flagged good in the per-dive file are written; the
  rest become NaN. Directives you add in `sg_directives.txt` therefore
  carry through to the DAC once the dive is reprocessed (see
  [Seaglider Data Quality Control](../seaglider/data-qc.md)).
- **Delayed mode**: rerun the extension over the whole mission with the
  delayed-submission option to get `_delayed` files.
- **Upload** with a line in the glider's `.ftps` file pointing at the
  deployment directory, or push by hand with the basestation's FTP push
  script.
- Global attributes for archiving centres (institution, PI, project) can
  also be set in the basestation's `NODC.yml`.

### Slocum

There is no vendor tool for this. Common routes:

- **pyglider**: converts the binary files to a CF timeseries using a
  deployment YAML file with the metadata, then to profiles. Out of the box
  its timeseries files don't pass the DAC checker; add the missing
  variables and write per-profile files.
- **GUTILS**: built specifically for producing DAC files from Slocum data.
- **The Coriolis decoder**, for EGO.
- **Regional portals**: some regional systems offer an "easy button" that
  takes common glider data types and submits to the DAC for you.

See [Slocum Data Processing & QC](../slocum/data-processing-qc.md#community-tools)
for the conversion step.

---

## Checklist

- [ ] Deployment registered on the DAC (and with OceanOPS) before launch
- [ ] WMO ID requested and in the metadata
- [ ] Instrument serial numbers and calibration dates in the deployment config
- [ ] A test file passes the compliance checker
- [ ] Upload uses FTPS and the current host name
- [ ] Data checked on the DAC map / ERDDAP, not just locally
- [ ] Units checked against the numbers (conductivity!)
- [ ] After recovery: delayed-mode files uploaded
- [ ] Deployment marked complete so it is archived

---

## See also

- [Data Formats & Standards](formats-and-standards.md)
- [CTD Post-Processing](ctd-post-processing.md)
- [Serving Data with ERDDAP](serving-data-erddap.md)
