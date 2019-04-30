# Configuring vRealize Automation

## Integrating Business Groups with vRA Workflows

### Overview

Business Groups in vRA can be combined with Rubrik Organizations to allow customers using vRA to provide multi-tenanted access to Rubrik through vRA Catalog Items, and prevent vRA users from managing objects which they should not have access to. This is an optional feature, and described below is how to both enable and disable this integration.

### Creating Organizations in Rubrik for use with vRA/vRO

To carry out some of the API calls needed by vRO on behalf of an Organization in Rubrik, it is necessary for vRO to obtain an API token from Rubrik specific to that Organization. This relies on the account configured on the vRO REST endpoint to be added to each Organization in the Org Admin role.

There is a workflow which will create Organizations included with the vRO package, this will create Organizations with the correct permissions, and can be integrated into existing Business Group provisioning workflows in the customer environment, if required.

### Using ShortName Custom Properties

In some customers, it is preferable to use a shortened value of the Business Group name, e.g. `CCO` instead of `Colgate Corporation`. If this is desired, then we will look for the Custom Attribute with naming convention `*.Tenant.ShortName`, and use the retrieved value to resolve to Organization Name.

NOTE: the name of the custom property being used is hardcoded into the `rubrik_BGNameToOrgName` action. It is possible to change this in here, but has not been tested with any other combination, so may lead to issues.

## Run the configuration workflow

The configuration workflow for vRA/vRO is named `Rubrik - Configure vRA Integration`, this sets up some configuration variables within vRO which determine the behaviour of the integration.

This is done through a new Configuration Element Category (named `Rubrik`) and Configuration Element (named `Configuration`). This Configuration Element contains the following attributes:

Name                | Type          | Description
------------------- | ------------- | -----------------------------------------------------
useShortName        | boolean       | Determines if a Business Group shortname custom attribute in vRA should be resolved to a Rubrik Organization name, rather than the Business Group name*
updatedDate         | Date          | Date that the configuration element was updated
useOnlyGlobalOrg    | boolean       | Determines if we should only ever use the Global organization in Rubrik. This is useful for customers who do not want integration with Business Groups.

\* see above section named 'Using ShortName Custom Properties' for more details.

### Configuration Scenarios

#### Not using Organizations at all

Name                | Value
------------------- | -------------
`useShortName`      | `false`
`useOnlyGlobalOrg`  | `true`

#### Using Organizations, Organization Name is the same as Business Group name

Name                | Value
------------------- | -------------
`useShortName`      | `false`
`useOnlyGlobalOrg`  | `false`

#### Using Organizations, using Short Name Custom Attribute

Name                | Value
------------------- | -------------
`useShortName`      | `true`
`useOnlyGlobalOrg`  | `false`

### Login as service account

To ensure that the correct default organization is set to Global for the service account, login with it to the Rubrik UI after an organization has been created, select 'Global' and 'Remember setting' when logging in.

### vRA Plugin Configuration

Where `useShortName` is set to `true`, and we are using Custom Properties from the Business Group, a vCACHost will be required for that specific tenant in the vRA Plugin in vRO. This is required so that we are able to look up Business Group properties. This can be added using the built in `Library > vRealize Automation > Configuration > Add a vRA Host` workflow. It is suggested here to use Shared Session authentication with a service account holding the Tenant Administrator role.

## Creating Catalog Items

See [Creating Catalog Items](create_catalog_items.md) for instructions.

## Managing Organizations

See [Managing Organizations](managing_organizations.md) for instructions.