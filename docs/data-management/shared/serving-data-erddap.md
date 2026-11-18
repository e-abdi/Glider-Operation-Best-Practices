---
title: Serving Data with ERDDAP
description: Running your own ERDDAP server for glider data — why, hardware, Docker images and security updates, organising datasets (timeseries, profiles, grids), GenerateDatasetsXml and the addAttributes/sourceAttributes split, profile and trajectory datasets, subsetting, reloading and debugging datasets, multidimensional data, and client access with erddapy.
---

# Serving Data with ERDDAP

**ERDDAP** is a free data server, widely used in oceanography, that lets
users search, subset, plot and download data in many formats (netCDF, CSV,
MATLAB, JSON …) through a web page or a URL. The US Glider DAC serves all
its glider data through ERDDAP, and many glider groups run their own
server as well, to:

- see and share their data before (or instead of) sending it to a DAC;
- serve products the DAC doesn't take, such as gridded sections or
  acoustic data;
- give project partners one stable place to get data.

!!! info "Source"
    Paraphrased from the UG2 Slack #data channel (ERDDAP set-up,
    datasets.xml and multidimensional-data threads, 2024), the ERDDAP
    documentation on setting up `datasets.xml`, and community Docker images
    and tutorials. ERDDAP changes between releases; follow the official
    documentation for details.

---

## Before you start

- **You don't need your own server to get data out.** If the goal is only
  public access, sending data to a DAC gives you its ERDDAP for free. Run
  your own when you have data or users the DAC doesn't serve.
- **Hardware.** One group serving many glider timeseries runs a dedicated
  server with 64 GB RAM, and found that more than it needs (16–32 GB would
  do). An **SSD** made processing and downloads about ten times faster;
  treat it as a must.
- **Use a Docker image.** The community images (the Axiom Data Science
  `docker-erddap` image, and the IOOS "ERDDAP gold standard" set-up built
  on it) take most of the pain out of installing Tomcat and ERDDAP. There
  are recorded tutorials and notebooks for both.
- **Keep it patched.** ERDDAP runs in Tomcat, and Tomcat security notices
  come round regularly (announced on the ERDDAP mailing list). Rebuild or
  pull a newer image when they do.

---

## Organising datasets

Glider data usually comes in three shapes, which map onto ERDDAP's two
dataset families:

| Your data | Dimensions | ERDDAP type |
|---|---|---|
| Timeseries (everything along the glider path) | time | Table (`tabledap`), `cdm_data_type` Trajectory |
| Profiles (as sent to the DAC) | profile, then time within it | Table, `cdm_data_type` TrajectoryProfile |
| Gridded sections | depth × time (or distance) | Grid (`griddap`) |

The natural unit is usually one dataset per **mission**. If you also run
repeat lines, you can aggregate missions (for example per year or per
line) and let users subset back down by deployment, profile or line.

---

## Building `datasets.xml`

ERDDAP is configured by `datasets.xml`, one block per dataset. Write it
with **`GenerateDatasetsXml`**, the tool that ships with ERDDAP, then edit
by hand.

- For each variable, `GenerateDatasetsXml` shows what it found in the files
  as a commented-out **`<sourceAttributes>`** block. Your changes go in
  **`<addAttributes>`**, which override the source.
- Setting an attribute to `null` in `<addAttributes>` removes it.
- With the `datasets.d` approach (one file per dataset, joined at start-up)
  each dataset can be edited on its own. If you script edits, use an XML
  library that keeps the comments `GenerateDatasetsXml` writes.

### Errors that cost the most time

- **"The variable with cf_role=profile_id must be in the
  cdm_profile_variables list"**, even though it is. The attribute was
  sitting in the commented `<sourceAttributes>`; it has to be set in
  `<addAttributes>`.
- **The subset selector doesn't work for a variable.** It needs string or
  integer values; floats don't work. Round times to whole seconds if you
  want to select by them. The variable also has to be listed in the
  `subsetVariables` global attribute.
- **A new dataset doesn't load and the log says little.** Set a **hard
  flag** for the dataset to force ERDDAP to reload it; the reload shows the
  specific error or hint. Repeat until it loads.

---

## Data that isn't a simple profile

Table datasets assume one set of time/depth coordinates. Data on a second
grid (an echosounder's echogram, ADCP bins) doesn't fit, and grid datasets
can't mix 1-D and 2-D variables. One approach that works:

- Write the extra data in the **same file** with its own dimensions (for
  example `echogram_time` × `echogram_bin`), following the CF
  trajectoryProfile multidimensional example.
- Give each variable a `coordinates` attribute naming its own time, depth,
  latitude and longitude.
- Serve it with the **`EDDTableFromMultidimNcFiles`** dataset type.
  `GenerateDatasetsXml` gets confused by the extra dimensions, so expect to
  tune the XML by hand.

netCDF4 groups are another option, but software support for them is
patchy. THREDDS serves any netCDF structure as-is over OPeNDAP, at the cost
of ERDDAP's subsetting and format conversion.

---

## Using ERDDAP data

- **`erddapy`** (Python) builds ERDDAP queries and loads results straight
  into pandas or xarray.
- The **graph** and **subset** pages let users explore a dataset with no
  code, for example stepping through profiles.
- Everything is a URL, so a query can be bookmarked, shared or scripted.

---

## See also

- [Data Formats & Standards](formats-and-standards.md)
- [Submitting to Data Centres](submitting-to-data-centres.md)
