# Options for Scheduling a Batch Scoring Pipeline

## Prerequisites
- An Azure subscription
- A resource group

## Terms
- DSVM = Data Science Virtual Machine
- AML = Azure Machine Learning
- ACI = Azure Container Instance
- ARM = Azure Resource Manager
- AKS = Azure Kubernetes Service

## Create Dev Environment

### Use ARM Script Locally to Create Windows DSVM
- TODO

### Use ARM Script Locally to Create Linux DSVM
- TODO

### Use Python Locally to Create Windows DSVM
- TODO

### Use Python Locally to Create Linux DSVM
- TODO

### Use Portal to Create Windows DSVM
- Browse: **portal.azure.com**
- Select: ``your resource group``
- Click: **+ Add**
- Type: **dsvm**
- Click: **Data Science Virtual Machine - Windows 2016** > **Create**
- Select: Subscription: ``<your subscription>``
- Select: Resource Group: ``<your resource group>``
- Type: Virtual machine name: ``<your vm name>``
- Select: Region: ``<your region>``
- Type: Username: ``<your user name>``
- Type: Password: ``<your password>``
- Click: **Review + create** > **Create**

or

### Use Portal to Create Linux DSVM
- Browse: **portal.azure.com**
- Select: ``<your resource group>``
- Click: **+ Add**
- Type: **dsvm**
- Click: **Data Science Virtual Machine for Linux (Ubuntu)** > **Create**
- Select: Subscription: ``<your subscription>``
- Select: Resource Group: ``<your resource group>``
- Type: Virtual machine name: ``<your vm name>``
- Select: Region: ``<your region>``
- Select: **Authentication**
- Type: **Password**
- Type: Username: ``<your user name>``
- Type: Password: ``<your password>``
- Click: **Review + create** > **Create**

## Open Jupyter Notebook on Dev Environment

### On Windows DSVM
- Login
  - Click: ``<your vm>`` > **Connect**
  - Click: **Download RDP File**
  - Save: locally
  - Double click: ``<your RDP file>``
  - Click: **OK** > **Connect**
  - Click: **More choices**
  - Select: **Use a different account**
  - Type: User name: ``<your user name>``
  - Type: Password: ``<your password>``
  - Click: **OK** > **Yes**
- Double click: **Jupyter** (takes a minute)

or

### On Linux DSVM
- Setup port forwarding (to access Jupyter Notebook on local browser)
   - Open: **PuTTY**
   - Expand: **Connection** > **SSH** > **Tunnels**
   - Type: Source port: **8000**
   - Type: Destination: **localhost:8000**
   - Click: **Add** > **Save**
   - SSH into DSVM (while open, port forwarding is active)
- Browse: https://localhost:8000
- Login using VM's username/password

## Register Subscription with ACI Using Jupyter Notebook on Dev Environment
- Expand: **AzureML**
- Click: **configuration.ipynb**
- Run: first cell to verify SDK version (should see output like version 1.0.2)
   ```python
   import azureml.core

   print("This notebook was created using version 1.0.2 of the Azure ML SDK")
   print("You are currently using version", azureml.core.VERSION, "of the Azure ML SDK")
   ```
- Insert new cell to login
   ```python
   !az login
   ```
- Insert new cell to see if your subscription is registered with ACI
   ```python
   !az provider show -n Microsoft.ContainerInstance -o table
   ```
- If not registered, insert new cell to register your subscription with ACI
   ```python
   !az provider register -n Microsoft.ContainerInstance
   ```
- Replace default values in next cell and run to set workspace parameters
   ```python
   import os

   subscription_id = os.getenv("SUBSCRIPTION_ID", default="<my-subscription-id>")
   resource_group = os.getenv("RESOURCE_GROUP", default="<my-resource-group>")
   workspace_name = os.getenv("WORKSPACE_NAME", default="<my-workspace-name>")
   workspace_region = os.getenv("WORKSPACE_REGION", default="eastus2")
   ```

## Create AML workspace

### Using Jupyter Notebook on Dev Environment

- Run next cell to create new workspace

### Using Portal (no hiccups)
- Browse: **portal.azure.com**
- Select: ``<your resource group>``
- Click: **+ Add**
- Type: **machine learning**
- Click: **Machine Learning service workspace** > **Create**
- Type: Workspace name: ``<your workspace name>``
- Select: Subscription: ``<your subscription>``
- Select: Resource group: ``<your resource group>``
- Select: Location: ``<your location>``

### Using Portal (hiccup - policy requires "Secure Transfer Required" for Storage Accounts)
- Browse: **portal.azure.com**
- Select: ``<your resource group>``
- Click: **+ Add**
- Type: **machine learning**
- Click: **Machine Learning service workspace** > **Create**
- Type: Workspace name: ``<your workspace name>``
- Select: Subscription: ``<your subscription>``
- Select: Resource group: ``<your resource group>``
- Select: Location: ``<your location>``
- Click: **Automation options** (Don't click **Create**)
- Click: **Download** > **Save As** > ``<your local folder>``
- Copy and paste zip file to your DSVM (drag and drop won't work, but copy and paste will)
- Extract contents of zip file
- Open a command prompt
- Change to the folder containing your extracted contents
- Type: **code .** (this will open Visual Studio Code)
- Modify **template.json** by inserting the below snippet where the Storage Account is created
```json
"properties": {
	"supportsHttpsTrafficOnly": true
},
```
- From command prompt, run: 
```
az group deployment create -g ``<your resource group>`` --subscription ``<your subscription id>`` --template-file template.json --parameters @parameters.json
```

### Create Compute Cluster Using Jupyter Notebook on Dev Environment

- Run: next cell to create CPU cluster
- Run: next cell to create GPU cluster (optional)

## Create and Deploy Model Using Jupyter Notebook on Dev Environment
- Expand: **how-to-use-azureml** > **machine-learning-pipelines** > **pipeline-batch-scoring**
- Click:  **pipeline-batch-scoring.ipynb**
- Run each cell individually (the first experiment run takes about 20 minutes, subsequent runs take a few seconds)

## Test calling REST AKS AML endpoint
- Insert new cell to set subscription id
   ```python
   # https://docs.microsoft.com/en-us/cli/azure/account?view=azure-cli-latest
   !az account set -s "{ws.subscription_id}"
   !az account show
   ```
- Insert new cell to create service principal
   ```python
   # https://docs.microsoft.com/en-us/cli/azure/ad/sp?view=azure-cli-latest
   !az ad sp create-for-rbac --name ``<your app name>``
   ```
- Insert new cell to generate token
   ```python
   # https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli?view=azure-cli-latest
   from azure.common.credentials import ServicePrincipalCredentials

   # "client_id" is the value for "appId" show above. you can see it the registered app on AAD in the portal
   # the "secret" is the value for "password" shown above. You can manage passwords for registered apps on AAD in the portal
   # the "tenant" is show above. It's also known as the "directory id" and you can get it on AAD in the portal and clicking "properties" 
   credentials = ServicePrincipalCredentials(client_id='{appId}',
                                             secret='{password}',
                                             tenant='{tenant}')
   api_key = credentials.token['access_token']
   aad_token = {'Authorization':('Bearer '+ api_key)}
   ```
- Insert new cell to call endpoint
   ```python
   response = requests.post(rest_endpoint, 
                         headers=aad_token, 
                         json={"ExperimentName": "batch_scoring",
                               "ParameterAssignments": {"param_batch_size": 50}})
   run_id = response.json()["Id"]
   ```

## Schedule using ADF
- Create ADF
   - Browse: **portal.azure.com**
   - Select: ``<your resource group>``
   - Click: **+ Add**
   - Type: **data factory**
   - Click: **Data Factory** > **Create**
   - Type: Name: ``<your name>``
   - Select: Subscription: ``<your subscription>``
   - Select: Resource Group: **Use existing**
   - Select: ``<your resource group>``
   - Select: Version: **V2**
   - Select: Location: **East US**
   - Click: **Create**
- Authorize ADF access to AML workspace using Managed Service Identity
   -Click on ``<your AML workspace>`` > ``<Access control (IAM)>`` > **Add role assignment**
   -Select: Role: **Contributor**
   -Type: Select: ``<your ADF name>``
   -Click: ``<your ADF name>`` > **Save**
- Configure ADF
   - Click: **Author & Monitor**
   - Click: **Create pipeline**
   - Expand: **General**
   - Drag: **Web**
   - Click: **Settings**
   - Paste: URL: ``<your endpoint>``
   - Select: Method: **POST**
   - Click: Headers: + New: NAME: **Authorization**, VALUE: ``<your bearer token>``
   - Click: Headers: + New: NAME: **Content-Type**, VALUE: **application/json**
   - Paste: Body: {"ExperimentName": "batch_scoring", "ParameterAssignments": {"param_batch_size": 50}}
   - Expand: **Advanced**
   - Select: **MSI**
   - Type: Resource: **https://management.azure.com/**
   - Click: **Validate**
   - Click: **Publish All**
   - Click: **Trigger** > **Trigger Now**
- Add Trigger
   - Click: **Trigger** > **New/Edit**
   - Select: Choose trigger... > **+ New**
   - Type: Name: ``<your trigger name>``
   - Select: **Schedule**
   - Type: Start Date (UTC): ``<your start date>``
   - Type: Recurrence: Every: ``<your interval>``
   - Click: **Next** > **Finish** > **Publish All**
   
## Schedule using AzureFunctions
- Setup Local Build Environment
   - Install [Python 3.6][install-python]
   - Install [Azure Functions Core Tools]
   - Install [.NET Core 2.x SDK for Windows][.NET Core 2.x SDK for Windows]
   - Install [Node.js][Node.js]
   - Install Core Tools package
      ```
      npm install -g azure-functions-core-tools
	  ```
   - Install the [Azure CLI][Azure CLI] (needed to publish and run in Azure)
   - Open a command prompt
   - Type (set variables)
      set SUBSCRIPTION_ID=``<your subscription id>``
      set RESOURCE_GROUP=``<your resource group>``
      set STORAGE_ACCOUNT=``<your storage account>``
      set APP_PLAN=``<your app plan>``
      set FUNCTION_APP=``<your function app>``
   - Type (create and activate a virtual environment)
      ```
      py -3.6 -m venv .env (Create and activate a virtual environment)
      .env\scripts\activate
      ```
- Create a Local Functions Project (contains your functions)
   - Type:
      ```
	  func init %FUNCTION_APP%
	  ```
   - Mouse down and select: **python (preview)**
   - Click: **Enter**
- Create, Deploy, and Test EchoName Function Locally
   - Type:
      ```
	  cd %FUNCTION_APP%
	  ```
   - Type: (create a new function)
      ```
	  func new
	  ```
   - Choose template: **HTTP trigger**
   - Type: Function name: **EchoName**
   - Click: **Enter**
   - Type: **func host start** (start local functions)
   - Copy and paste URL in browser, and replace <yourname> with a name of your choosing:
      ```
      http://localhost:7071/api/EchoNameFunction?name=<yourname>
      ```
- Deploy and Test EchoName Function on Azure
   - Type:
      ```
	  az login
	  ```
   - Type: (set your subscription id)
      ```
	  az account set --subscription %SUBSCRIPTION_ID%
	  ```
   - Type: (show account)
      ```
	  az account show
	  ```
   - Type: (create a resource group)
      ```
	  az group create --name %RESOURCE_GROUP% --location eastus
	  ```
   - Type: (create a storage account)
      ```
      az storage account create --name %STORAGE_ACCOUNT% --location eastus --resource-group %RESOURCE_GROUP% --sku Standard_LRS
      ```
   - Type: (create an app service plan)
      ```
	  az appservice plan create -g %RESOURCE_GROUP% -n %APP_PLAN% --is-linux --number-of-workers 4 --sku S1
	  ```
   - Type: (Create a Python function app running on Linux that will contain the functions. This uses a consumption plan)
      ```
      az functionapp create --resource-group %RESOURCE_GROUP% --os-type Linux --consumption-plan-location eastus --runtime python --name %FUNCTION_APP% --storage-account %STORAGE_ACCOUNT%
      ```
   - Type: (Create a Python function app running on Linux that will contain the functions. This uses an existing app service plan)
      ```
      az functionapp create --resource-group %RESOURCE_GROUP% --os-type Linux --plan %APP_PLAN% --runtime python --name %FUNCTION_APP% --storage-account %STORAGE_ACCOUNT% --deployment-container-image-name azure-functions-python3.6:2.0
      ```
   - Type: (Deploy the function app project)
      ```
      func azure functionapp publish %FUNCTION_APP%
      ```
   - Expand: ``<function app>`` > **Functions** > **EchoName**
   - Click: **Get function URL** > **Copy**
   - Paste URL into browser, and add:
      ```
	  ?name=<your name>
	  ```
- Create, Deploy, and Test BatchScoring Function Locally
   - Change directory: **FunctionsProject**
   - Type: (create a new function)
      ```
	  func new
	  ```
   - Choose template: **HTTP trigger**
   - Type: Function name: **BatchScoringFunction**
   - Click: **Enter**
   - Type: (Add requests library)
      ```
      pip install requests
      ```
   - Edit __init__.py
      ```
      def main(req: func.HttpRequest) -> func.HttpResponse:
      logging.info('Python HTTP trigger function processed a request.')

      url = "<your endpoint>"
      headers = {"Content-Type": "application/json",
	      "Authorization": "<your token>"}
      body = {"ExperimentName": "batch_scoring", "ParameterAssignments": {"param_batch_size": 50}}
      r = requests.post(url, data=body, headers=headers)

      return func.HttpResponse(r.text)
      ```
   - Type: **func host start** (start local functions)
   - Copy and paste URL in browser:
      ```
	  http://localhost:7071/api/BatchScoringFunction
      ```
- Deploy and Test BatchScoring Function on Azure
   - Edit __init__.py
      ```
      import logging
      import requests
      import azure.functions as func

      def main(req: func.HttpRequest) -> func.HttpResponse:
         logging.info('Python HTTP trigger function processed a request..')    
         url = "<your function url>"
         headers = {"Content-Type": "application/json"}
         body = {"ExperimentName": "batch_scoring", "ParameterAssignments": {"param_batch_size": 50}}
         try:       
            response = str(requests.post(url, 
               headers=headers, 
               json=body))        
            return func.HttpResponse(response)
         except Exception as e:
            return func.HttpResponse("exception: " + str(e))
      ```
	- goto function app
	- click **Platform features** > **All Settings** > **Authentication/Authorization**
	- toggle: App Service Authentication: **On**
## Schedule using Pipeline Scheduling
   - Create a new schedule
      ```
      from azureml.pipeline.core.schedule import ScheduleRecurrence, Schedule

      SCHED_FREQUENCY = "<your time unit>"
      SCHED_INTERVAL = <number of time units>
      RESOURCE_GROUP_NAME = "<your resource group name>"
      experiment_name = "<your experiment name>"
      recurrence = ScheduleRecurrence(frequency=SCHED_FREQUENCY, interval=SCHED_INTERVAL)
      schedule = Schedule.create(
          workspace=ws,
          name="{}_sched".format(RESOURCE_GROUP_NAME),
          pipeline_id=published_id,
          experiment_name=experiment_name,
          recurrence=recurrence,
          description="{}_sched".format(RESOURCE_GROUP_NAME),
      )
   ```
   Disable the schedule (if needed)
      ```
	  schedule.disable()
      ```		   
## Schedule using LogicApps
- TODO

## Links
Web activity in Azure Data Factory
https://docs.microsoft.com/en-us/azure/data-factory/control-flow-web-activity
What is managed identities for Azure resources?
https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview
Services that support managed identities for Azure resources
https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/services-support-msi
Azure Data Factory service identity
https://docs.microsoft.com/en-us/azure/data-factory/data-factory-service-identity
Azure Storage Account CLI
https://docs.microsoft.com/en-us/cli/azure/storage/account?view=azure-cli-latest
Services that support managed identities for Azure resources
https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/services-support-msi#azure-services-that-support-managed-service-identity
Using Managed Service Identity (MSI) with an Azure App Service or an Azure Function
https://blogs.msdn.microsoft.com/benjaminperkins/2018/06/13/using-managed-service-identity-msi-with-and-azure-app-service-or-an-azure-function/ 
New-AzureADServiceAppRoleAssignment
https://docs.microsoft.com/en-us/powershell/module/azuread/new-azureadserviceapproleassignment?view=azureadps-2.0
Work with Azure Functions Core Tools
https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local
How to use managed identities for App Service and Azure Functions
https://docs.microsoft.com/en-us/azure/app-service/overview-managed-identity?toc=%2fazure%2fazure-functions%2ftoc.json

<!-- links -->

[machine-learning]: https://docs.microsoft.com/en-us/azure/machine-learning/
[machine-learning-service]: https://docs.microsoft.com/en-us/azure/machine-learning/service/
[samples]: https://docs.microsoft.com/en-us/azure/machine-learning/service/samples-notebooks
[aml-notebooks]: https://aka.ms/aml-notebooks
[how-to-use-azureml]: https://github.com/Azure/MachineLearningNotebooks/tree/master/how-to-use-azureml
[machine-learning-pipelines]: https://github.com/Azure/MachineLearningNotebooks/tree/master/how-to-use-azureml/machine-learning-pipelines
[pipeline-batch-scoring]: https://github.com/Azure/MachineLearningNotebooks/tree/master/how-to-use-azureml/machine-learning-pipelines
[setup-dsvm]: https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-configure-environment#dsvm
[functions-create-scheduled-function]: https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-scheduled-function
[functions-create-first-function-python]: https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-first-function-python
[install-python]: https://www.python.org/downloads/
[install-functions-core-tools]: https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local#v2
[.NET Core 2.x SDK for Windows]: https://www.microsoft.com/net/download/windows
[Node.js]: https://docs.npmjs.com/getting-started/installing-node#osx-or-windows
[Azure CLI]: https://docs.microsoft.com/cli/azure/install-azure-cli
[functions-reference-python]: https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python
