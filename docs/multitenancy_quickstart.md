# Quick Start Guide: Configuring Multi-tenancy support within the Rubrik plugin for vRealize

Multi-tenanted access can be configured within the Rubrik Plugin for vRealize in order to prevent vRA users from managing objects within Rubrik which they should not have access to. Before following the steps in this guide, ensure that the Rubrik Plugin for vRealize has been installed and the associated XaaS blueprints have been imported, both which are outlined in the [Rubrik Plugin for vRealize Quickstart Guide](quick-start.md). 

The process of configuring multi-tenancy involves the following:

1. Enabling the multi-tenancy by executing the built-in configuration workflow.
2. Configuring Rubrik Organizations for use with vRealize Business Groups
3. Modifying the XaaS Blueprints to retrieve the Business Group from the request information.
4. Creating services to group common XaaS blueprints. (OPTIONAL)

The following outlines the above processes in detail.

## Enabling Multi-Tenancy support in the Rubrik Plugin for vRealize

Multi-Tenancy support within the Rubrik Plugin for vRealize is enabled through the execution of a built-in workflow named `Rubrik - Configure vRA Integration` included with the plugin. The workflow sets up configuration variables within vRO which handle the behaviour of the integration.

Configuration variables are stored in a new Configuration Element Category (named `Rubrik`) inside Configuration Element (named `Configuration`). This Configuration Element contains the following attributes:

Name                | Type          | Description
------------------- | ------------- | -----------------------------------------------------
useShortName        | boolean       | Determines if a Business Group shortname custom attribute in vRA should be resolved to a Rubrik Organization name, rather than the Business Group name*
updatedDate         | Date          | Date that the configuration element was updated
useOnlyGlobalOrg    | boolean       | Determines if we should only ever use the Global organization in Rubrik. This is useful for customers who do not want integration with Business Groups.

---
**NOTE**

In some customers, it is preferable to use a shortened value of the Business Group name, e.g. `CCO` instead of `Colgate Corporation`. If this is desired, then we will look for the Custom Attribute with naming convention `*.Tenant.ShortName`, and use the retrieved value to resolve to Organization Name.

NOTE: the name of the custom property being used is hardcoded into the `rubrik_BGNameToOrgName` action. It is possible to change this in here, but has not been tested with any other combination, so may lead to issues.

---

### Configuration Scenarios

The following outlines the variable values defined within common configurations.

#### Not using Rubrik Organizations at all

Name                | Value
------------------- | -------------
`useShortName`      | `false`
`useOnlyGlobalOrg`  | `true`

#### Using Rubrik Organizations when the organization name matches the vRA Business Group name

Name                | Value
------------------- | -------------
`useShortName`      | `false`
`useOnlyGlobalOrg`  | `false`

#### Using Rubrik Organizations and the vRA Business Group Short Name Custom Attribute

Name                | Value
------------------- | -------------
`useShortName`      | `true`
`useOnlyGlobalOrg`  | `false`

---
**NOTE**

Where `useShortName` is set to `true`, and we are using Custom Properties from the Business Group, a vCACHost will be required for that specific tenant in the vRA Plugin in vRO. This is required so that we are able to look up Business Group properties. This can be added using the built in `Library > vRealize Automation > Configuration > Add a vRA Host` workflow. It is suggested here to use Shared Session authentication with a service account holding the Tenant Administrator role.

---

## Configuration Rubrik Organizations for use with vRealize Automation

To carry out some of the API calls needed by vRO on behalf of an Organization defined within Rubrik, it is necessary for vRO to obtain an API token from Rubrik specific to that Organization. This relies on the service account configured on the vRO REST endpoint inventory item to be added to each Organization in the Org Admin role.

For example, the following shows the REST API endpoint inventory item for a Rubrik Cluster specific to the `dbaorg` organization. The account utilized during the `Rubrik - Add Cluster Instance` was `dba`.

![alt text](/docs/images/image31.png)

The following shows the `dbaorg` organization within the Rubrik UI. As shown, the `dba` account is setup with the Org Admin role within Rubrik.

![alt text](/docs/images/image32.png)

---
**NOTE**

To ensure that the correct default organization is set to Global for the service account, login with it to the Rubrik UI after an organization has been created. When prompted, select 'Global' for the Organization and check 'Remember Selected Organization', then continue the sign-in.

---

### Rubrik Organization Workflows

The Rubrik Plugin for vRealize contains a number of prebuilt workflows designed to manage Organizations within Rubrik, including the creation and deletion of Organizations.

#### Creating an Organization

The `Rubrik - Create Organization` workflow can be used to create an Organization on the selected Rubrik cluster. This is located in the `Rubrik-DevOps > vRO-Workflows > Organizations` folder within vRO.

The `Rubrik - Create Organization` workflow also adds the specified user account as an Org Admin within Rubrik.

#### Deleting an Organization

The `Rubrik - Delete an Organization` workflow can be used to immediately delete an Organization from the selected Rubrik cluster. This is located in the `Rubrik-DevOps > vRO-Workflows > Organizations` folder within vRO

#### Automating the retirement of Organizations

In order to enable service providers to manage the lifecycle of their tenants, a workflow has been provided named `Rubrik - Retire an Organization`. This is located in the `Rubrik-DevOps > vRO-Workflows > Organizations` folder within vRO.

When run, the user is prompted to select a Rubrik cluster and an Organization Name. The workflow then queries the organization for all unexpired snapshots. The snapshots are then analyzed, obtaining the date the last snapshot will retire, which is then used for the date the Organization will be deleted.

##### Calculating the expiry date

Each snappable belonging to the Organization is queried for a list of snapshots, and for each snapshot the date of expiry is calculated. The oldest date of expiry of all snapshots will be used for marking the date at which the Organization should be deleted.

If there are snapshots which are flagged to keep forever (those which have the `UNPROTECTED` SLA applied to them), the workflow will throw an error with a list of the snapshots which are to be kept forever. The administrator would then need to go and manage these snapshots via the Rubrik UI, deleting or modifying the retention policy on them to ensure they are no longer kept forever.

---
**NOTE**

Once the expiry date is calculated, Configurations are used within vRealize Orchestrator (vRO) to track which Organizations have been flagged for deletion, and the date that they can be deleted. These can be found under `Configurations > Rubrik > Organization Expiry`.

---

##### Scheduled Workflow

There is a scheduled workflow which runs each day, and follows the process below to ensure that Organizations are deleted as expected:

* Re-calculate organization expiry date (using above process) for all expired organizations - this ensures that no new snapshots or SLA changes have taken place which could delay the retiring of the Organizations
* Delete any organizations which are past their expiry date from Rubrik
* Remove the configuration attribute for this organization from vRO

This workflow is named `Rubrik - Scheduled Organization Deletion`, and is in the `Rubrik-DevOps > vRO-Workflows > Scheduled` folder within vRO. Configuration of this workflow is optional, and is set through the `Rubrik - Configure vRA Integration` workflow.

## Configuring XaaS Blueprints for Multi-tenancy

A number of XaaS blueprints will be created when importing the vRA content using CloudClient.  While the imported blueprints have complete support for multi-tenancy, by default they are configured to provide global access to the objects and resources within Rubrik. Whether or not a blueprint abides by the permissions set forth within a Rubrik Organization is controlled by the value of the `Business Group` field embedded on the blueprint form. Setting the value of `Business Group` to Global removes the multi-tenancy support for the desired blueprint, while defining a value to retrieve the business group from the request (`Request Info > Business Group`) enables multi-tenancy support.

The following outlines the process of enabling and disabling multi-tenancy support for a given XaaS blueprint.

### Enabling support for multi-tenancy on an XaaS blueprint

1. When editing the vRA form, select the 'Business Group' field on the form
2. Click the 'Constraints' tab in the right hand pane
3. Under 'Read only', select 'Constant', 'Yes'
4. Under 'Value', select 'Field', click 'Define Field Values', select 'Request info > Business group > Name'
5. Under 'Visible', select 'Constant', 'No'

The following illustrates an XaaS Blueprint configured for multi-tenant use:

![alt text](/docs/images/image33.png)

### Disabling support for multi-tenancy on an XaaS blueprint

1. When editing the vRA form, select the 'Business Group' field on the form
2. Click the 'Constraints' tab in the right hand pane
3. Under 'Read only', select 'Constant', 'Yes'
4. Under 'Value', select 'Field', click 'Constant', enter the string 'Global'
5. Under 'Visible', select 'Constant', 'No'

The following illustrates an XaaS Blueprint configured for global use:

![alt text](/docs/images/image34.png)

An XaaS blueprint which has been enabled for multi-tenancy will now restrict the objects available for selection during the item request.

## Creating Services to group common XaaS blueprints

To help better organize the Rubrik XaaS blueprints and simplify the process of entitlement it is recommended to create Services within vRA. By creating services, vRA administrators are able to grant access to multiple XaaS blueprints with one entitlement. For instance, a service may be created containing all of the SQL Server related XaaS blueprints and then entitled to a group of DBAs.

While the organization of catalog items will vary depending on customer requirements, the following is a suggestion on how to deliver this:

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

Configured services are now available to be entitled to users and groups within vRA. For more information on entitlements, see the [Rubrik Plugin for vRealize Quickstart Guide.](quick-start.md)
