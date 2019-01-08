# Quick Start Guide: Rubrik Plugin for vRealize

## Introduction to the Rubrik Plugin for vRealize
With Rubrik's core fundamental strategy of an API First architecture, integrating Rubrik CDM functionality and features into a vRealize Automation (vRA)  service catalog is easily achieved by importing the Rubrik Plugin for vRealize into vRealize Orchestrator (vRO). Once installed, custom vRA Property Definitions and Groups can be created and assigned to existing or newly created blueprints. Leveraging Rubrik with vRA brings many benefits to organizations such as:

*	**Data Loss Prevention** - This will ensure data protection is a key stakeholder in your VM Lifecycle Management and provisioning processes by requiring newly created VMs to be protected.
*	**Self-Service Instant Recovery** - This provides a one-click process to restore files to any point-in-time, and the ability to resume operations within minutes of an attack with self-service file-level recovery.
*	**Streamlined Operations** - This eliminates lengthy wait times at the help desk with self-service access to backup and restore operations.
*	**Alignment with Business SLAs** - Automate compliance policies in just a few clicks to adhere to strict business requirements.

The Rubrik Plugin for vRealize contains a number of pre-built workflows, actions, and configuration elements which, once imported into vRO, allow administrators to easily integrate data management processes into self-service catalogs.

## Rubrik Plugin for vRealize Quickstart
The following section outlines how to get started using the Rubrik Plugin for vRealize, including installation and configuration of the plugin as well as how to import sample, pre-built vRA blueprints and entitle them appropriately.

### Prerequisites
The following are the prerequisites in order to successfully install and configure the Rubrik Plugin for vRealize:

*	VMware vRealize Automation 7.3 or above
*	[Rubrik Plugin for vRealize](https://github.com/rubrikinc/rubrik-vrealize)
*	Rubrik CDM 4.1 or above

In addition to the above requirements, the following are the prerequisites in order to successfully import and execute the pre-built vRA blueprints outlined in this quick start guide:

*	[VMware vRealize CloudClient](https://code.vmware.com/web/dp/tool/cloudclient/4.6.0)
*	[Rubrik blueprints for vRA](https://github.com/rubrikinc/rubrik-vrealize/blob/master/vra_blueprints.zip)

### Installation
This section will outline how to install the Rubrik Plugin for vRealize as well as import sample Rubrik blueprints and resource actions into vRA.

#### Rubrik Plugin for vRealize Installation
Rubrik’s integration with vRealize Automation (vRA) is supported by the Rubrik Plugin for vRealize containing a number of pre-built workflows and configuration items. The following outlines the steps to download and install the Rubrik Plugin for vRealize:

1.	Download the Rubrik Plugin for Realize, located on GitHub. 
2.	Log into vRO. 
3.	Switch to either the **Design** or **Administer** view in the vRO client. This grants access to the **Packages** tab.

![alt text](/docs/images/image1.png)

4.	Click the **Import package** button, browse to the previously downloaded Rubrik Plugin (`com.rubrik.devops.package`) and select **Open**.

![alt text](/docs/images/image2.png)

5.	When prompted, review the associated packages certificate information and select **Import** to continue.

![alt text](/docs/images/image3.png)

6.	When prompted, select the package elements you wish to import, or click the **Select/Deselect all** checkbox to select all elements and click **Import selected elements**.

![alt text](/docs/images/image4.png)

7.	Once installed, the `com.rubrik.devops` package will appear in the list of packages. Upon selecting it, the **Workflows** tab will display a list of the pre-built Rubrik workflows available within vRO.

![alt text](/docs/images/image5.png)

The next section outlines how to install a sample set of Rubrik blueprints. 

#### Rubrik Blueprint / Anything as a Service (XaaS) Installation
A successful Blueprint / XaaS installation is dependent on proper configuration and authentication login of VMware vRealize CloudClient (“CloudClient”). This utility is downloadable from [here](https://code.vmware.com/web/dp/tool/cloudclient/4.6.0).

Once CloudClient has been installed and configured, you will want to download the Rubrik blueprints for vRA (available [here](https://github.com/rubrikinc/rubrik-vrealize/blob/master/vra_blueprints.zip)). Put it in a convenient location that can be easily accessed from CloudClient.

To begin:

1.	Obtain a Cloud Client prompt by executing `cloudclient.bat` or `cloudclient.sh` after configuration at the above URL.

![alt text](/docs/images/image6.png)

2.	The variable, `--dry-run`, can be used to conduct a check without actually importing any content. The command would look similar to the following:

```vra content import --path /users/rebecca/downloads/vra_blueprints.zip --resolution OVERWRITE --precheck WARN --verbose --dry-run```

3.	Once the dry run has successfully completed, run the command without `--dry-run`:

```vra content import --path /users/rebecca/downloads/vra_blueprints.zip --resolution OVERWRITE --precheck WARN --verbose```

![alt text](/docs/images/image7.png)

4.	Ensure the output of the command was successful. 

![alt text](/docs/images/image8.png)

5.	Upon successful import, use a web browser to access the vRA tenant. Navigate to **Design** > **XaaS** > **XaaS Blueprints**; you should see several pre-built blueprints. 

![alt text](/docs/images/image9.png)

6.	Now, navigate to **Design** > **XaaS** > **Resource Actions**; you should see multiple pre-built resource actions. 

![alt text](/docs/images/image10.png)

### Configuration
This section will outline the steps to configure the Rubrik Plugin for vRealize as well as information on how to define the entitlements to the Rubrik sample blueprints and actions within vRA.

#### Configuring the Rubrik Plugin for vRealize
Before consuming any workflows within vRA/vRO the Rubrik Plugin for vRealize must first be configured to communicate with a Rubrik cluster. As with most elements within vRO, configuring Rubrik is completed by running an included configuration workflow. The following outlines the steps to configure the Rubrik Plugin for vRealize:

1.	From the Workflows tab, expand the navigation tree to  Library > Rubrik-DevOps>Configuration. Select to run the Rubrik - Add Cluster Instance workflow.

![alt text](/docs/images/image11.png)

2.	When prompted, complete the inputs for the workflow. The **Host Properties** section prompts to input a friendly **Name** for the REST host, along with the **URL** to connect to a Rubrik CDM cluster. **Connection** and **Operation timeout** may also be adjusted, however, the defaults of 30 and 60 seconds, respectively, suffice for most environments. The credentials of a user with access to the Rubrik cluster also needs to be populated in the **Authentication username** and **Authentication password** fields respectively. Once finished, click **Next**.

![alt text](/docs/images/image12.png)

3.	*Optional* If using a proxy to connect to Rubrik CDM, select **Yes** and enter the details. If not, leave **No** selected. Click **Submit**.

![alt text](/docs/images/image13.png)

4.	Once the workflow has completed processing, the logs can be viewed by selecting the workflow session and navigating to the logs tab. The success or failure is indicated by a green checkmark or red x placed to the right of the workflow session, as shown below.

![alt text](/docs/images/image14.png)

5.	Selecting the **Inventory** section and expanding the HTTP-REST tree shows our Rubrik cluster has been successfully added to the vRO instance.

![alt text](/docs/images/image15.png)

The Rubrik Plugin for vRealize has now been successfully configured, set up, and connected with a Rubrik CDM cluster. All workflows contained within the plugin are now accessible and executable. 

#### Configuring Entitlements in vRA
This section will configure access based on two levels of access as described below. The exact configuration may vary, dependant on the environment configuration and RBAC settings.

The imported blueprints and resource actions require entitlement. As an example, this section will demonstrate the following configuration:

*	"XaaS Blueprints" to the Administrative Entitlements
*	"XaaS Resource Actions" to the User Entitlements

##### Administrative Entitlement
In the vRA tenant, navigate to **Administration** > **Catalog Management** > **Entitlements** and select an existing Entitlement used for administrators. 

![alt text](/docs/images/image16.png)

Select the **Items & Approvals** tab and then the plus sign (**+**) next to **Entitled Items**.

![alt text](/docs/images/image17.png)

Under **Type**, select **XaaS Blueprint** and then choose the two Rubrik related items. Press **OK**. 

![alt text](/docs/images/image18.png)

Press **Finish** to complete the process. 

##### User Entitlement
In the vRA tenant, navigate to **Administration** > **Catalog Management** > **Entitlements** and select an existing Entitlement used for users. 

![alt text](/docs/images/image16.png)

Select the **Items & Approvals** tab and then the plus sign (**+**) next to **Entitled Actions**.

![alt text](/docs/images/image19.png)

On the **Add Items** dialog, select the Rubrik related items. Press **OK**. 

![alt text](/docs/images/image20.png)

Press **Finish** to complete the process. 

### Using the Rubrik Post-Provisioning Workflow
The Rubrik Plugin for vRealize contains a custom built workflow designed to assist with assigning newly provisioned VMs from vRA to Rubrik SLA domains. The workflow, `Rubrik Post-Provisioning Workflow` can be found by expanding the vRO navigation tree to **Library** > **Rubrik-DevOps** > **Helper Workflows**.

![alt text](/docs/images/image21.png)

The workflow is intended to be set up within vRA as a Workflow Subscription, allowing the workflow to be triggered once a VM has been provisioned. The `Get Custom Properties` element within the workflow contains pre-configured syntax which retrieves all the information needed from vRA in order to process the `Rubrik - Assign SLA` element. Most of the required information is configured within vRA by default with the exception of the following two custom properties which need to be configured manually:

*	**`rubrik.cluster`** - a string value representing the target Rubrik cluster
*	**`rubrik.sla_name`** - a string value representing the desired SLA Domain name to use

![alt text](/docs/images/image22.png)

In order to utilize the `Rubrik - Post-Provisioning` workflow, custom **Property Definitions** and **Property Groups** are required to be configured within vRA. The **Property Definition** names within vRA must exactly match the defined variable names within the vRO workflow.

![alt text](/docs/images/image23.png)

Once Property Definitions and Groups have been defined, the `Rubrik - Post-Provisioning` Workflow may then be added as a Workflow Subscription within vRA.

![alt text](/docs/images/image24.png)

For more information on how to configure a Provision and Protect blueprint within vRA and how to define the custom Property Definitions, see the [Provision and Protect Use Case](https://github.com/rubrikinc/rubrik-blueprints-for-vrealize/blob/master/Provision%20and%20Protect/quick-start.md) on GitHub.

### Sample Use Case - Change provisioned VM SLA Domain
The `Rubrik - Assign SLA Domain` Resource Action is one of many pre-built components provided with the Rubrik vRA blueprints download. The resource action provides a means for end-users to select a new SLA Domain for provisioned virtual machines - allowing organizations to provide self-service around backup frequencies, retention, and archival. 

|**Note:** This section requires that the pre-built Rubrik vRA blueprints have been installed along with the proper entitlements configured. For more information on how to achieve this, see the Rubrik Blueprint / XaaS Installation section. |

The following outlines the steps to execute the `Rubrik - Assign SLA Domain` Resource Action:

1.	With the resource action imported and properly entitled to a vRA user, select **Deployments**, then select the provisioned resource to be modified.

![alt text](/docs/images/image25.png)

2.	Select the **Actions** menu for the provisioned virtual machine, then **Rubrik - Assign SLA Domain**.

![alt text](/docs/images/image26.png)

3.	On the **Rubrik - Assign SLA Domain** form, select the desired `Rubrik Cluster` and `SLA Domain` name from the dropdowns and click **Submit**.

![alt text](/docs/images/image27.png)

4.	The task process will display in the **Deployments** tab with the associated vRO workflow, `Rubrik - Assign SLA Domain`, running in the background displaying any generated logs.

![alt text](/docs/images/image28.png)

5.	The vRO workflow makes the appropriate API calls to the Rubrik cluster to modify the SLA Domain assignment of the given virtual machine. The virtual machine is now assigned to the `Gold` SLA Domain.

## API Documentation
The Rubrik Plugin for vRealize provides workflows and actions supports the most common integrations between Rubrik CDM and vSphere. That said, release cycles between the Rubrik Plugin for vRealize and Rubrik CDM are not simultaneous. This means there may be times when new features or enhancements are added to the product but workflows and actions to consume these features have yet to be released. For these situations, the Rubrik Plugin for vRealize contains the `rubrik_GetFromAPI` action which handles the execution of raw API requests to be sent to the Rubrik cluster. The following outlines the syntax required within vRO’s Scriptable Task element in order to utilize the `rubrik_GetFromAPI` action to retrieve a list of ESXi hosts within the Rubrik inventory: 

```
// setup variables
var resthost = 'Cluster_B';
var method = 'GET'
var url = 'vmware/host';
var content = '';

// execute the API call
var response = System.getModule("com.rubrik.devops.actions").rubrik_GetFromAPI(resthost,url,method,content) ;

//convert the response to JSON
var json = JSON.parse(response.contentAsString).data;

// loop through response and output hostname to log
for(key in json) {	
    var obj = json[key];
    System.log(obj.name);
}
```

Rubrik prides itself upon its API-first architecture, ensuring everything available within the HTML5 interface, and more is consumable via a RESTful API. For more information on Rubrik’s API architecture and complete API documentation, please see the official Rubrik API Documentation.

## Troubleshooting
The Rubrik Plugin for vRealize includes robust error reporting and exception handling for the workflows and actions included within the package. That said, there may be times when chaining together multiple workflows or designing workflows from scratch when additional troubleshooting and debugging is required. The following outlines two options which can be used to help with the development of vRO workflows integrating with the Rubrik Plugin for vRealize

### Using vRO Debug Mode
vRO includes debugging functionality which allows workflow designers to add breakpoints to elements within a workflow schema. Upon hitting a breakpoint, the workflow execution will suspend, allowing for workflow execution information to be viewed, variables to be viewed and/or modified, and the review of any general logging information. Once reviews and modifications have been made, administrators have a number of options to continue the workflow execution:

*	**Resume** - Resumes the workflow execution until another breakpoint is reached or the workflow has completed.
*	**Step into** - Steps further into the workflow element.
*	**Step over** - Steps over the current element and pauses at the next breakpoint.
*	**Step return** - Exits a workflow element which has been stepped into.

![alt text](/docs/images/image29.png)

Breakpoints are inserted and deleted by simply right-clicking on a schema element and choosing to `Toggle Breakpoint`. Associated workflow execution options are displayed at the top of the `Debugger` window.

### Using `System.log()`
When developing vRO workflows it may be useful to output different variables or messages to the log window at different points within the workflow. This can be accomplished by inserting a **Scriptable Task** element into the schema of the workflow and using the `System.log()` function to display a value as shown below.

```
//display contents of rubrik_host variable
System.log(rubrik_host);

//display message indicating workflow execution status
System.log('About to call rubrik_GetFromAPI action');
System.getModule("come.rubrik.devops.actions").rubrik_GetFromAPI(rubrik_host,url,method,content);
System.log('rubrik_GetFromAPI action has been called');
```

The output of the `System.log()` function will then be displayed within the **Logs** tab of the vRO client.

## Contributing Additional Workflows


## Further Reading
*	Rubrik and VMware vRealize Reference Architecture
*	[Rubrik Build Use Case: Provision and Protect with vRA](https://github.com/rubrikinc/rubrik-blueprints-for-vrealize/blob/master/Provision%20and%20Protect/quick-start.md)
*	[Rubrik Plugin for vRealize GitHub Repository](https://github.com/rubrikinc/rubrik-vrealize)
* Rubrik CDM API Documentation
