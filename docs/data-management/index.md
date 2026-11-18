---
title: Data Management
description: Getting glider data from the vehicle to users — processing, quality control, formats and data assembly centres, organised by platform.
---

# Data Management

What happens to glider data after it leaves the vehicle: decoding and
processing, quality control, and preparing data for users and data
assembly centres. The processing chain differs a lot between platforms,
so the pages are organised by glider.

## Platforms

<div class="grid cards" markdown>

-   ![Seaglider](images/seaglider.png){ .platform-icon }

    **Seaglider**

    ---

    How the basestation processes and quality-controls each dive, and how to review and correct the result.

    [:octicons-arrow-right-24: Seaglider Data Management](seaglider/index.md)

-   ![Slocum](images/slocum.svg){ .platform-icon }

    **Slocum**

    ---

    Converting and merging the binary files, the community toolchain, and the QC and corrections the user has to apply.

    [:octicons-arrow-right-24: Slocum Data Management](slocum/index.md)

</div>

## All Platforms

Steps that are the same whatever the glider.

<div class="grid cards" markdown>

-   :material-file-table-outline: **Data Formats & Standards**

    ---

    NGDAC, EGO and OG1.0 netCDF, CF conventions, metadata, QC flag schemes and compliance checkers.

    [:octicons-arrow-right-24: Data Formats & Standards](shared/formats-and-standards.md)

-   :material-cloud-upload-outline: **Submitting to Data Centres**

    ---

    The US Glider DAC, Coriolis and OceanOPS: registration, WMO IDs, uploads, and archiving.

    [:octicons-arrow-right-24: Submitting to Data Centres](shared/submitting-to-data-centres.md)

-   :material-thermometer-water: **CTD Post-Processing**

    ---

    Units, sensor alignment, thermal lag, reference checks and TEOS-10 quantities.

    [:octicons-arrow-right-24: CTD Post-Processing](shared/ctd-post-processing.md)

-   :material-server-network: **Serving Data with ERDDAP**

    ---

    Running your own ERDDAP server for glider timeseries, profiles and grids.

    [:octicons-arrow-right-24: Serving Data with ERDDAP](shared/serving-data-erddap.md)

</div>
