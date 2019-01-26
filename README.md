# Rubrik Plugin for vRealize
Rubrik provides cradle-to-grave data management for VMs provisioned using vRealize. Day 2 operations such as Instant Recovery, Live Mount, and on-demand snapshots are available

## Installation
The Rubrik Plugin for vRealize consists of two primary components: a package for vRealize Orchestrator and blueprints for vRealize Automation. 

### Rubrik Package vRealize Orchestrator

* Download vRO Package - available [here](https://github.com/rubrik-devops/rubrik-vrealize/blob/master/com.rubrik.devops.package)
* Run vRO Designer
* **Administer** > **Packages** > **Import Package**
* Select `com.rubrik.devops.package`
* Select **Import selected elements**
* Run the Workflow `Rubrik - Add Cluster Instance`, entering your cluster information in the form
* Module is now configured

### Rubrik Blueprints for vRealize Automation

* Download vRA blueprints - available [here](https://github.com/rubrik-devops/rubrik-vrealize/blob/master/vra_blueprints.zip)
* Authenticate to vRA via CloudClient 
  
  ```
  vra login userpass
  ```
  
* Import Module 
  
  ```
  vra content import --path [path to vra_blueprints.zip] --resolution OVERWRITE --precheck WARN --verbose \[--dry-run\]
  ```https://www.rubrik.com/blog/a-how-to-guide-on-rubriks-vrealize-automation-integration/
  
* Entitle Resource Actions within the tenant - Administration->Catalog Management->Entitlements

## Quick Start
* [Quick Start Guide - Rubrik Plugin for vRealize](https://github.com/rubrikinc/rubrik-plugin-for-vrealize/blob/master/docs/quick-start.md)
* [Use Case: Provision and Protect with vRealize Automation](https://github.com/rubrikinc/rubrik-blueprints-for-vrealize/blob/master/Provision-and-Protect/quick-start.md)

## Documentation
* [Rubrik API Documentation](https://github.com/rubrikinc/api-documentation)

## Additional Links
* [Rubrik Blueprints for vRealize](https://github.com/rubrikinc/rubrik-blueprints-for-vrealize)
* [VIDEO: Getting Started with the Rubrik Plugin for vRealize]()
* [VIDEO: Getting Started Provisioning and Protecting with vRealize]()
* [BLOG: Provision and Protect vRealize Workloads](https://www.rubrik.com/blog/provision-protect-vrealize-rubrik/)
* [BLOG: A How-To Guide on Rubrik’s vRealize Automation Integration](https://www.rubrik.com/blog/a-how-to-guide-on-rubriks-vrealize-automation-integration/)
* [BLOG: New vRealize Orchestrator Workflows for Enhancing Your Rubrik Experience](https://www.rubrik.com/blog/vrealize-orchestrator-rubrik/)
* [BLOG: Open Source vRealize Orchestrator Plugin Released](https://www.rubrik.com/blog/open-source-vrealize-orchestrator-plugin-released/)
