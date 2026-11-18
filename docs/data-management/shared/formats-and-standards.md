---
title: Data Formats & Standards
description: The data formats glider data ends up in — vendor files, the Seaglider per-dive netCDF, the US IOOS NGDAC netCDF v2, the European EGO format and the OceanGliders OG1.0 format — plus CF conventions, metadata, QC flag schemes, file naming, and compliance checkers.
---

# Data Formats & Standards

A glider's raw files are vendor formats built for small size and quick
transfer, not for users. Before data can be shared, it has to be written to
a **standard netCDF format**: self-describing files with agreed variable
names, units, metadata and QC flags. Which standard you use depends mostly
on where the data is going.

!!! info "Source"
    Paraphrased from the US IOOS Glider DAC documentation and compliance
    checker output, the basestation3 GliderDAC extension and its example
    configuration, the OceanGliders format user manual (OG1.0) and its
    announcements, Coriolis decoder release notes, the UG2 Slack #data
    channel (2022–2026), and operator correspondence with data users.
    Formats evolve: always check the current specification before building
    a pipeline.

---

## From raw files to standard files

| Stage | Seaglider | Slocum |
|---|---|---|
| Raw from the glider | Compressed, encoded dive files (`.eng`, `.log`, `.dat`) | Binary flight and science files (`.dbd`/`.ebd`, `.sbd`/`.tbd`, compressed versions) |
| Basic processed product | Per-dive netCDF (`pXXXYYYY.nc`) made by the basestation, already QC'd | None from the vendor; converted with community tools (see [Slocum Data Processing & QC](../slocum/data-processing-qc.md)) |
| Mission products | Mission timeseries and mission profile netCDF (basestation) | Toolbox timeseries and gridded files (for example pyglider L0 timeseries and grid) |
| Data centre format | NGDAC, EGO or OG1.0 | NGDAC, EGO or OG1.0 |

### Reading the Seaglider per-dive netCDF

The basestation's per-dive file is the starting point for everything on the
Seaglider side, and it confuses new users. Points that come up again and
again:

- **There are several time bases in one file.** Variables are sampled on
  different dimensions. The main glider series is on `sg_data_point`; the
  CTD may have its own (`ctd_data_point`) and each science-computer
  (scicon) sensor has its own, for example an optode on
  `<sensor>_data_point` with its own `<sensor>_time`. A separate, shorter
  series (`gc_event`) holds guidance-and-control events. Arrays of
  different lengths are normal, not a fault.
- **Match a variable to the time and depth on its own dimension.** Don't
  pair values by array index across dimensions.
- **Prefer `ctd_time` and `ctd_depth`** for science, rather than the
  pressure-sensor `depth`. On some configurations `time` and `ctd_time` are
  the same; on others they aren't.
- **Scalars carry per-dive values**: GPS fixes, depth-averaged current,
  surface current, and so on.
- **Every QC'd variable has a matching `_qc` variable.** See
  [Seaglider Data Quality Control](../seaglider/data-qc.md).

!!! tip "Give data users a variable guide"
    Users new to gliders struggle with these files ("it is confusing even
    for us" is a common pilot reply). When you hand data to a project
    partner, include a short table of the variables they need, which
    dimension each is on, and its units. Simple CSV exports are rarely a
    good substitute: users who expect netCDF often can't use them, and they
    lose the metadata.

---

## The standard formats

There are three glider netCDF formats in use. They overlap a lot but are
not interchangeable: a 2019 comparison by the OceanGliders data management
group found many differences in variable names, dimensions and metadata
between the US, European and Australian formats.

| | US IOOS NGDAC netCDF v2 | EGO (Everyone's Gliding Observatories) | OceanGliders OG1.0 |
|---|---|---|---|
| Used by | US IOOS National Glider Data Assembly Center | Coriolis (Europe) and the EGO network | Agreed community format, intended to replace the others over time |
| Structure | One file per **profile** (`featureType: trajectoryProfile`) | One file per **deployment** (time series), upper-case names (`TIME`, `LATITUDE`, `TEMP` …) with `_QC` variables | One file per **deployment** |
| QC flags | QARTOD-style `_qc` ancillary variables | Argo-style flags | Argo-style flags |
| Vocabularies | CF standard names, IOOS attributes | CF plus NERC/SeaDataNet codes (`sdn_parameter_urn`, `sdn_uom_urn`) | CF plus controlled vocabularies (NERC) |
| Notes | Mature, widely used; feeds the GTS through NDBC | Produced by the Coriolis decoder for Slocum, Seaglider and SeaExplorer | Published 2021–2024; adoption by data centres is still in progress |

### US IOOS NGDAC netCDF v2

Each profile is a separate file. Besides the measured variables, the
format expects:

- **Profile identifiers**: `trajectory`, `profile_id`, `profile_time`,
  `profile_lat`, `profile_lon`.
- **Depth-averaged current**: `u`, `v`, with their own `time_uv`,
  `lat_uv`, `lon_uv`.
- **Container variables** describing the platform and each instrument
  (`platform`, `instrument_ctd`, …) with make, model, serial number and
  calibration date.
- **`ancillary_variables`** on each measured variable, pointing to its
  `_qc` variable, even if no QC was done.
- Global attributes such as `date_modified`, `wmo_id`, creator and
  publisher details.

A whole-deployment timeseries file (for example straight out of pyglider)
is **not** what the DAC wants. Toolboxes that target the DAC add the
missing variables and split the data into profiles.

### EGO

The European format, produced mostly by the **Coriolis decoder**, a free
MATLAB tool (also as a runtime version that needs no MATLAB licence). It
reads Slocum, SeaExplorer and Seaglider netCDF files, writes EGO files and
applies real-time QC automatically. Each variable keeps a record of where
it came from, for example `glider_original_parameter_name =
"sci_m_present_time"` on `TIME`.

### OceanGliders OG1.0

The OceanGliders data management task team's common format, developed in
the open on GitHub with a user manual, example files and vocabulary
collections. File names follow `<platform_serial>_<start_date>_<data_mode>.nc`,
for example `sp065_20210616T143025_R.nc` (Spray 065, start time in ISO 8601
to the second, `R` for real time). Tools for checking files are listed
[below](#checking-a-file-before-you-send-it).

!!! note "Data that doesn't fit a profile"
    All three formats assume one set of time and depth dimensions. Data on
    a second grid (echograms from an echosounder, ADCP bins, spectra) does
    not fit cleanly. Teams have worked around it with extra dimensions and
    a `coordinates` attribute on each variable, following the CF
    trajectoryProfile examples. Extensions to the formats were still under
    discussion in 2024–2026. Until then, send the core CTD data to the data
    centre as usual and serve the rest separately (see
    [Serving Data with ERDDAP](serving-data-erddap.md)).

---

## CF conventions and metadata

All three formats build on the **CF (Climate and Forecast) conventions**:

- **`standard_name`** says what a variable physically is. Pick it with
  care: `sea_water_density` means **in-situ** density, while potential
  density is `sea_water_potential_density` (or `sea_water_sigma_theta`
  without the 1000). Data centres have received both under one name. Say
  which in the `long_name` too.
- **`units`** must match the numbers. A common failure is conductivity
  labelled `S m-1` while the values are in mS/cm (a factor of 10). In 2026
  the US DAC had several deployments like this, with impossible densities
  as the result. Check values, not just labels.
- **`_FillValue`, `valid_min`, `valid_max`** must have the same data type as
  the variable, or checkers and readers complain.
- **Global attributes** describe who made the data (`creator_*`,
  `publisher_*`, `institution`), the licence, the platform and the
  processing level. Most toolboxes take these from configuration files
  (YAML in pyglider and the Seaglider GliderDAC extension), so keep a
  per-glider and per-deployment template.

Keep instrument metadata (serial numbers, calibration dates) with the
deployment. It is tempting to harvest these from the glider's own
configuration files, but those rarely hold everything a science user needs.

---

## QC flag schemes

| Value | QARTOD (US) | Argo / EGO / OG1.0 |
|---|---|---|
| 0 | — | No QC performed |
| 1 | Pass | Good |
| 2 | Not evaluated | Probably good |
| 3 | Suspect | Probably bad (correctable) |
| 4 | Fail | Bad |
| 5–8 | — | Changed, not used, interpolated (scheme-dependent) |
| 9 | Missing | Missing |

The two schemes **mean different things for 2**: "not evaluated" in QARTOD,
"probably good" in Argo. Convert carefully when moving between formats.
The Seaglider basestation uses Argo-style codes internally (see
[QC flag values](../seaglider/data-qc.md#qc-flag-values)).

!!! warning "What a downstream tool does with your flags"
    The Seaglider GliderDAC extension keeps only `QC_GOOD` points from the
    per-dive file and writes everything else as NaN, then marks the
    remaining values good. Other tools pass flags through. Know which
    yours does, so flags aren't lost or misread on the way.

---

## Naming files

| Format | Real time | Delayed mode |
|---|---|---|
| US NGDAC | `glider_yyyymmddTHHMMSSZ.nc` (time of the profile) | `glider_yyyymmddTHHMMSSZ_delayed.nc` |
| OG1.0 | `<serial>_<start>_R.nc` | Same pattern with the delayed data-mode code |

The NGDAC deployment directory itself is usually named
`<glider>-<yyyymmddTHHMM>` after the deployment start.

---

## Checking a file before you send it

- **IOOS Compliance Checker** with the glider DAC plugin
  (`compliance-checker -t gliderdac:3.0 file.nc`) lists missing variables
  and attributes. Some messages are stale (it still asks for a
  `traj_strlen` dimension the current format doesn't need), and full
  compliance is "highly recommended" rather than required, but anything
  under *Required* is worth fixing.
- **OG1.0** has an online validator and a compliance checker in
  development (a Rust checker that covers recent CF versions, plus a
  Python plugin for the IOOS Compliance Checker).
- **Open the file in a second tool.** A dataset that passes after one
  toolbox can fail after the next. Re-check after every processing step
  that rewrites the file.

---

## See also

- [Submitting to Data Centres](submitting-to-data-centres.md)
- [CTD Post-Processing](ctd-post-processing.md)
- [Serving Data with ERDDAP](serving-data-erddap.md)
- [Seaglider Data Quality Control](../seaglider/data-qc.md)
- [Slocum Data Processing & QC](../slocum/data-processing-qc.md)
