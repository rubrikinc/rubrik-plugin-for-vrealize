# Creating vRA Custom Properties for Provisioning Hooks

Custom Properties can be used to provide provisioning hooks into vRA Blueprint deployment, enabling the addition of newly provisioned VMware VMs into Rubrik SLA Domain policies.

The following steps describe the process for configuring and applying these properties to existing blueprints:

## Creating the Property Group and Properties

Go to 'Administration > Property Dictionary > Property Definitions', create two new Custom Property definitions as follows:

Name | Label | Visibility | Data type | Required | Display as | Values | Script action | Input parameters
--- | --- | --- | --- | --- | --- | --- | --- | ---
rubrik.cluster | Rubrik Cluster | All tenants | String | Yes | Dropdown | External values | com.rubrik.devops.actions/rubrik_GetRestHosts | None
rubrik.sla_name | Rubrik SLA Domain | All tenants | String | Yes | Dropdown | External values | com.rubrik.devops.actions/rubrik_GetSlaList | rubrik_host/Yes/rubrik.cluster

Go to 'Administration > Property Dictionary > Property Groups', create a new Property Group as follows:

* Name: Rubrik
* ID: rubrik
* Visibility: All tenants
* Properties:

Name | Value | Encrypted | Show in Request
--- | --- | --- | ---
rubrik.cluster | \<blank\> | No | Yes
rubrik.sla_name | \<blank\> | No | Yes

## Creating the Event Broker Subscription

Go to 'Administration > Events > Subscriptions', create a new Subscription as follows:

* Event Topic: Machine provisioning
* Conditions: Run based on conditions (All of the following):
  * `Data > Machine > Machine type` Equals `Virtual Machine`
  * `Data > Lifecycle state > Lifecycle state name` Equals `VMPSMasterWorkflow32.MachineActivated`
  * `Data > Lifecycle state > State phase` Equals `POST`
* Workflow: Orchestrator > Library > Rubrik-DevOps > Helper Workflows > Rubrik - Post-Provisioning Workflow
* Details:
  * Name: Rubrik - Post-Provisioning Workflow
  * Description: Manages post-provisioning activities for VMs with Rubrik custom properties

Select the new subscription and click 'Publish'

## Using the Post-Provisioning Workflow

On a VM in an IaaS blueprint, the 'Rubrik' Property Group can now be added to facilitate protection of the VM as part of provisioning.
