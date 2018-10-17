# vRealize Automation Integration Requirements
## Non Production Environment
* Rubrik 4.1 (preferred)
* vRA 7.3 or above
* Microsoft SQL Server 2008+
* Functional IAAS Infrastructure
* Functional vCenter Integration
* Functional vRO Integration
* vRO 7.3 or above
* Functional vCenter Integration
* Functional vRA Integration
* vCenter 6.0 or above
## Development Workstation
* VMware’s Cloudclient - https://code.vmware.com/tool/cloudclient/4.4.0
* VMware’s vRO Workflow Designer
* Network Access and Credentials for- vRealize Infrastructure
* Github Code Download - https://github.com/rubrik-devops/rubrik-vra/archive/development.zip

## Installation

### Rubrik's vRA/vRo Modules - https://github.com/rubrik-devops/rubrik-vra/tree/development
* Run vRO Designer
* Administer->Packages->Import Package
* Select com.rubrik.devops.package 
* Deselect 'Import the values of the configuration settings'
* Select 'Import selected elements'
* After import, select 'Configurations' and double click Rubrik
* Select Attributes->Edit, and double click username/password to set them
* Select Workflows->Library->Rubrik-DevOps->Configuration->Rubrik - Add Cluster Instance
* Run the Workflow (Play), entering your cluster information in the form
* Module is now configured
### Run CloudClient
* Authenticate to vRA via CloudClient - vra login userpass
* Import Module - vra content import --path [path to Rubrik_VRA.zip] --resolution OVERWRITE --precheck WARN --verbose [--dry-run]
* Entitle Resource Actions within the tenant - Administration->Catalog Management->Entitlements
