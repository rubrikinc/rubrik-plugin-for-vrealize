# Managing Organizations using vRA

## Creating an Organization

The `Rubrik - Create Organization` workflow can be used to create an Organization on the selected Rubrik cluster. This is located in the `Rubrik-DevOps > vRO-Workflows > Organizations` folder within vRO.

To carry out some of the API calls needed by vRO on behalf of an Organization in Rubrik, it is necessary for vRO to obtain an API token from Rubrik specific to that Organization. This relies on the account configured on the vRO REST endpoint to be added to each Organization in the Org Admin role. This workflow will add the required permissions to the organization, such that it will support the other vRO workflows.

## Deleting an Organization

The `Rubrik - Delete an Organization` workflow can be used to immediately delete an Organization from the selected Rubrik cluster. This is located in the `Rubrik-DevOps > vRO-Workflows > Organizations` folder within vRO

## Automating the retirement of Organizations

In order to enable service providers to manage the lifecycle of their tenants, a workflow has been provided named `Rubrik - Retire an Organization`. This is located in the `Rubrik-DevOps > vRO-Workflows > Organizations` folder within vRO

When run, the user is prompted to select a Rubrik cluster and an Organization Name. The workflow then queries the organization for all unexpired snapshots, these are then used to calculate the date the last snapshot will expire, and so the date that the Organization can be safely deleted.

### Calculating the expiry date

Each snappable belonging to the Organization is queried for a list of snapshots, and for each snapshot the date of expiry is calculated. The oldest date of expiry of all snapshots will be used for marking the date at which the Organization should be deleted.

If there are snapshots which are flagged to keep forever (those which have the `UNPROTECTED` SLA applied to them), the workflow will throw an error with a list of the snapshots which are to be kept forever. The administrator would then need to go and manage these snapshots via the Rubrik UI, deleting or modifying the retention policy on them to ensure they are no longer kept forever.

### Creating a Configuration Element Attribute

Once the expiry date is calculated, Configurations are used within vRealize Orchestrator (vRO) to track which Organizations have been flagged for deletion, and the date that they can be deleted. These can be found under `Configurations > Rubrik > Organization Expiry`.

### Scheduled Workflow

There is a scheduled workflow which runs each day, and follows the process below to ensure that Organizations are deleted as expected:

* Re-calculate organization expiry date (using above process) for all expired organizations - this ensures that no new snapshots or SLA changes have taken place which could delay the retiring of the Organizations
* Delete any organizations which are past their expiry date from Rubrik
* Remove the configuration attribute for this organization from vRO

This workflow is named `Rubrik - Scheduled Organization Deletion`, and is in the `Rubrik-DevOps > vRO-Workflows > Scheduled` folder within vRO. Configuration of this workflow is optional, and is set through the `Rubrik - Configure vRA Integration` workflow.