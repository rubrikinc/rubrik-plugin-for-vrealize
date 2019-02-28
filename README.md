# Rubrik Plugin for vRealize
Rubrik provides cradle-to-grave data management for VMs provisioned using vRealize. Day 2 operations such as Instant Recovery, Live Mount, and on-demand snapshots are available

# :hammer: Installation
The Rubrik Plugin for vRealize consists of two primary components: a package for vRealize Orchestrator and blueprints for vRealize Automation. 

## Rubrik Package vRealize Orchestrator

* Download vRO Package - available [here](https://github.com/rubrik-devops/rubrik-vrealize/blob/master/com.rubrik.devops.package)
* Run vRO Designer
* **Administer** > **Packages** > **Import Package**
* Select `com.rubrik.devops.package`
* Select **Import selected elements**
* Run the Workflow `Rubrik - Add Cluster Instance`, entering your cluster information in the form
* Module is now configured

## Rubrik Blueprints for vRealize Automation

* Download vRA blueprints - available [here](https://github.com/rubrik-devops/rubrik-vrealize/blob/master/vra_blueprints.zip)
* Authenticate to vRA via CloudClient 
  
  ```
  vra login userpass
  ```
  
* Import Module 
  
  ```
  vra content import --path [path to vra_blueprints.zip] --resolution OVERWRITE --precheck WARN --verbose \[--dry-run\]
  ```
  
* Entitle Resource Actions within the tenant - **Administration** > **Catalog Management** > **Entitlements**

# :blue_book: Documentation 

Here are some resources to get you started. If you find any challenges from this project are not properly documented or are unclear, please [raise an issue](https://github.com/rubrikinc/rubrik-plugin-for-vrealize/issues/new/choose) and let us know! This is a fun, safe environment - don't worry if you're a GitHub newbie! :heart:

* [Quick Start Guide - Rubrik Plugin for vRealize](https://github.com/rubrikinc/rubrik-plugin-for-vrealize/blob/master/docs/quick-start.md)
* [Use Case: Provision and Protect with vRealize Automation](https://github.com/rubrikinc/rubrik-blueprints-for-vrealize/blob/master/Provision-and-Protect/quick-start.md)
* [Rubrik API Documentation](https://github.com/rubrikinc/api-documentation)
* [Rubrik Blueprints for vRealize](https://github.com/rubrikinc/rubrik-blueprints-for-vrealize)
* [VIDEO: Getting Started with the Rubrik Plugin for vRealize](https://www.youtube.com/watch?v=Bpzp64YwrCQ&feature=youtu.be)
* [VIDEO: Getting Started Provisioning and Protecting with vRealize](https://www.youtube.com/watch?v=T1FSBsVwg-g&feature=youtu.be)
* [BLOG: Provision and Protect vRealize Workloads](https://www.rubrik.com/blog/provision-protect-vrealize-rubrik/)
* [BLOG: A How-To Guide on Rubrik’s vRealize Automation Integration](https://www.rubrik.com/blog/a-how-to-guide-on-rubriks-vrealize-automation-integration/)
* [BLOG: New vRealize Orchestrator Workflows for Enhancing Your Rubrik Experience](https://www.rubrik.com/blog/vrealize-orchestrator-rubrik/)
* [BLOG: Open Source vRealize Orchestrator Plugin Released](https://www.rubrik.com/blog/open-source-vrealize-orchestrator-plugin-released/)

# :muscle: How You Can Help

We glady welcome contributions from the community. From updating the documentation to adding more Intents for Roxie, all ideas are welcome. Thank you in advance for all of your issues, pull requests, and comments! :star:

* [Contributing Guide](CONTRIBUTING.md)
* [Code of Conduct](CODE_OF_CONDUCT.md)

# :pushpin: License

* [MIT License](LICENSE)

# :point_right: About Rubrik Build

We encourage all contributors to become members. We aim to grow an active, healthy community of contributors, reviewers, and code owners. Learn more in our [Welcome to the Rubrik Build Community](https://github.com/rubrikinc/welcome-to-rubrik-build) page.
