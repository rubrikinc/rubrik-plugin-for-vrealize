# Creating Catalog Items

## Overview

This document describes the management of Rubrik Catalog Items in the vRA Service Catalog.

## Creating Services

The Rubrik Catalog Items are served out to users will depend on the customer, but below is a suggestion of how to deliver this:

---

**Service Name**: Rubrik - Administration

**Description**: Manage the Rubrik vRA Integration

**Catalog Items**:

* Rubrik - Add Cluster Instance
* Rubrik - Remove Cluster Instance

---

**Service Name**: Rubrik - Linux Hosts

**Description**: Manage protection of Linux Hosts with Rubrik

**Catalog Items**:

* Rubrik - Add a Linux Fileset
* Rubrik - Add a Linux Host
* Rubrik - Delete a Linux Fileset
* Rubrik - Delete a Linux Host
* Rubrik - Modify a Linux Fileset
* Rubrik - Restore a Linux File/Folder
* Rubrik - Restore a Linux Fileset
* Rubrik - Snapshot a Linux Fileset

---

**Service Name**: Rubrik - SQL Server

**Description**: Manage protection of MSSQL DBs with Rubrik

**Catalog Items**:

* Rubrik - Export a SQL Server Backup
* Rubrik - Modify a SQL Server DB
* Rubrik - Protect a SQL Server DB
* Rubrik - Snapshot a SQL Server DB

---

**Service Name**: Rubrik - Unmanaged Objects

**Description**: Report on and delete Unmanaged Objects on Rubrik

**Catalog Items**:

* Rubrik - Delete Unmanaged Snapshots
* Rubrik - Umanaged Snapshot Report

---

**Service Name**: Rubrik - Windows Hosts

**Description**: Manage protection of WindowsHosts with Rubrik

**Catalog Items**:

* Rubrik - Add a Windows Fileset
* Rubrik - Add a Windows Host
* Rubrik - Delete a Windows Fileset
* Rubrik - Delete a Windows Host
* Rubrik - Modify Windows Fileset Protection
* Rubrik - Restore a Windows File/Folder
* Rubrik - Restore a Windows Fileset
* Rubrik - Snapshot a Windows Fileset or Volume

---

NOTE: These are suggestions only, whether each Catalog Items should be published to any service will depend on what the vRA and Rubrik administrators want to deliver to users.

## Managing the XaaS Blueprints

XaaS blueprints will be created when importing the vRA content using CloudClient, this defaults to the settings described in the XaaS Blueprint Forms - Using Business Groups for Multi-Tenancy section below. This may need amending depending on your environment, the below steps detail this.

### Editing a blueprint

1. Go to the 'Design' tab in vRA, select 'XaaS > XaaS Blueprints'
1. Click '+ New', select the desired workflow from the 'Orchestrator > Library > Rubrik-DevOps > VRA-CatalogItems' folder
1. Click 'Next', 'Next'
1. Edit the form as desired (see below)
1. Click 'Next', 'Next', 'Finish'

### XaaS Blueprint Forms - Using Business Groups for Multi-Tenancy

1. When editing the vRA form, select the 'Business Group' field on the form
1. Click the 'Constraints' tab in the right hand pane
1. Under 'Read only', select 'Constant', 'Yes'
1. Under 'Value', select 'Field', click 'Define Field Values', select 'Request info > Business group > Name'
1. Under 'Visible', select 'Constant', 'No'

### XaaS Blueprint Forms - No Multi-Tenancy Requirement

1. When editing the vRA form, select the 'Business Group' field on the form
1. Click the 'Constraints' tab in the right hand pane
1. Under 'Read only', select 'Constant', 'Yes'
1. Under 'Value', select 'Field', click 'Constant', enter the string 'Global'
1. Under 'Visible', select 'Constant', 'No'

### Publish Blueprints

Once all blueprints have been created, ensure that these are published, by selecting the blueprint from the summary screen, and clicking the 'Publish' button.

## Attaching Services to Entitlements

These services can now be attached to vRA Entitlements as required.