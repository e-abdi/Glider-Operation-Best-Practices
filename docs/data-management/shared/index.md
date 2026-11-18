---
title: All Platforms
description: Data management topics that apply to every glider — data formats and standards, submitting to data assembly centres, CTD post-processing, and serving data with ERDDAP.
---

# Data Management — All Platforms

Once the platform-specific processing is done (see
[Seaglider](../seaglider/index.md) and [Slocum](../slocum/index.md)), the
remaining steps are much the same for every glider: correcting the CTD,
writing standard files, sending them to data assembly centres, and serving
them to users.

## In This Section

<div class="grid cards" markdown>

-   :material-file-table-outline: **Data Formats & Standards**

    ---

    The glider netCDF formats in use (US IOOS NGDAC, EGO, OG1.0), CF conventions, the metadata they expect, QC flag schemes, and how to check a file before you send it.

    [:octicons-arrow-right-24: Data Formats & Standards](formats-and-standards.md)

-   :material-cloud-upload-outline: **Submitting to Data Centres**

    ---

    Getting data to the US Glider DAC, Coriolis and OceanOPS: registering a deployment, WMO IDs, real-time vs delayed-mode files, upload over FTPS, and marking a deployment complete for archiving.

    [:octicons-arrow-right-24: Submitting to Data Centres](submitting-to-data-centres.md)

-   :material-thermometer-water: **CTD Post-Processing**

    ---

    From raw temperature, conductivity and pressure to trustworthy salinity and density: units, sensor alignment, thermal lag, dive/climb comparison, reference checks, and which TEOS-10 quantities to report.

    [:octicons-arrow-right-24: CTD Post-Processing](ctd-post-processing.md)

-   :material-server-network: **Serving Data with ERDDAP**

    ---

    Running your own ERDDAP server for glider data: hardware, Docker images, laying out datasets, `GenerateDatasetsXml`, profile and trajectory datasets, and the errors that cost the most time.

    [:octicons-arrow-right-24: Serving Data with ERDDAP](serving-data-erddap.md)

</div>
