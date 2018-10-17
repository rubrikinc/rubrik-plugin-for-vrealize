# vRealize Automation Integration Requirements
## vRealize Environment
* Rubrik 4.1 or above 
* vRA 7.3 or above
* vRO 7.3 or above - If you're importing the vRA Blueprints

## Development Workstation
* VMware’s Cloudclient - https://code.vmware.com/web/dp/tool/cloudclient/4.6.0
* VMware’s vRO Workflow Designer
* Network Access and Credentials for vRealize Infrastructure

# Rubrik Customization Installation

## vRo Package 
* Download vRO Package - https://github.com/rubrik-devops/rubrik-vrealize/blob/master/com.rubrik.devops.package
* Run vRO Designer
* Administer->Packages->Import Package
* Select com.rubrik.devops.package 
* Select 'Import selected elements'
* Run the Workflow 'Rubrik - Add Cluster Instance', entering your cluster information in the form
* Module is now configured

## vRA Blueprints
* Download vRA blueprints - https://github.com/rubrik-devops/rubrik-vrealize/blob/master/vra_blueprints.zip
* Authenticate to vRA via CloudClient - vra login userpass
* Import Module - vra content import --path [path to vra_blueprints.zip] --resolution OVERWRITE --precheck WARN --verbose [--dry-run]
* Entitle Resource Actions within the tenant - Administration->Catalog Management->Entitlements
