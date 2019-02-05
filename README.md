# Creating real-time scoring pipeline

## Prerequisites
- An Azure subscription
- A resource group

## Terms
- DSVM = Data Science Virtual Machine
- AML = Azure Machine Learning
- ACI = Azure Container Instance
- ARM = Azure Resource Manager

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
- Select: **Data Science Virtual Machine - Windows 2016**
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
  - Save: locally
  - Double click: ``<your RDP file>``
  - Click: **OK** > **Connect**
  - Click: **More choices**
  - Select: **Use a different account**
  - Type: User name: ``<your user name>``
  - Type: Password: ``<your password>``
  - Click: **OK** > **Yes**
- Double click: **Jupyter**

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
- Insert new cell to see if your subscription is registered with ACI
   ```python
   !az provider show -n Microsoft.ContainerInstance -o table
   ```
   if not, insert new cell and run
   ```python
   !az provider register -n Microsoft.ContainerInstance
   ```

## Create AML workspace

### Using Jupyter Notebook on Dev Environment
- Replace default values in second cell and run to set workspace parameters
   ```python
   import os

   subscription_id = os.getenv("SUBSCRIPTION_ID", default="<my-subscription-id>")
   resource_group = os.getenv("RESOURCE_GROUP", default="<my-resource-group>")
   workspace_name = os.getenv("WORKSPACE_NAME", default="<my-workspace-name>")
   workspace_region = os.getenv("WORKSPACE_REGION", default="eastus2")
   ```
- Run fourth cell to create new workspace

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
- Replace default values in second cell and run to set workspace parameters
   ```python
   import os

   subscription_id = os.getenv("SUBSCRIPTION_ID", default="<my-subscription-id>")
   resource_group = os.getenv("RESOURCE_GROUP", default="<my-resource-group>")
   workspace_name = os.getenv("WORKSPACE_NAME", default="<my-workspace-name>")
   workspace_region = os.getenv("WORKSPACE_REGION", default="eastus2")
   ```

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
- Click: **Automation options**
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
- Run: 
```
az group deployment create -g ``<your resource group>`` --subscription ``<your subscription id>`` --template-file template.json --parameters @parameters.json
```
- Replace default values in second cell and run to set workspace parameters
   ```python
   import os

   subscription_id = os.getenv("SUBSCRIPTION_ID", default="<my-subscription-id>")
   resource_group = os.getenv("RESOURCE_GROUP", default="<my-resource-group>")
   workspace_name = os.getenv("WORKSPACE_NAME", default="<my-workspace-name>")
   workspace_region = os.getenv("WORKSPACE_REGION", default="eastus2")
   ```

### Create Compute Cluster Using Jupyter Notebook on Dev Environment

- Run: fifth cell to create CPU cluster
- Run: sixth cell to create GPU cluster (optional)

## Create and Deploy Model Using Jupyter Notebook on Dev Environment
- Expand: **how-to-use-azureml** > **machine-learning-pipelines** > **pipeline-batch-scoring**
- Click:  **pipeline-batch-scoring.ipynb**
- Run each cell individually (the first experiment run takes about 20 minutes, the second about 11 minutes, then drops to about 5 seconds)

## Test using REST Client
- Open: RESTClient Firefox plugin
- Method: POST
- URL: ``<your endpoint>``
- Header: Key: **Authorization**, Value: ``<your bearer token>``
- Header: Key: **Content-Type**, Value: **application/json**
- Body: {"ExperimentName": "batch_scoring", "ParameterAssignments": {"param_batch_size": 50}}
- Click: **Send**

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
   - Click: **Validate**
   - Click: **Publish All**
   - Click: **Trigger** > **Trigger Now**
   
## Schedule using [AzureFunction][functions-create-first-function-python]
- Prerequisites
   - To build and test locally
      - Install [Python 3.6][install-python]
         - Install [Azure Functions Core Tools]
         - Install [.NET Core 2.x SDK for Windows][.NET Core 2.x SDK for Windows]
         - Install [Node.js][Node.js]
         - Install Core Tools package
            npm install -g azure-functions-core-tools
         - to publish and run in Azure
            - Install the [Azure CLI][Azure CLI]
         - Create and activate a virtual environment
             - Type:
                ```powershell
                py -3.6 -m venv .env
                .env\scripts\activate
                ```
         - Create a local Functions project
            - Type: func init MyFunctionProj
            - Mouse down and select: **python (preview)**
            - cd MyFunctionProj
         - Echo name function
            - Create a function
               - Type: func new
               - Choose template: **HTTP trigger**
               - Choose Function name: **HTTP Trigger**
            - Run the functions locally
               - Type: **func host start** (remember to do this in the function projects folder)
               - Copy URL and paste in browser:
               ```
               http://localhost:7071/api/HttpTrigger?name=<yourname>
               ```
            - Deploy to Azure
               - Type: **az login**
               - Create a Resource Group
               - Create an Azure Storage account
                  Type:
                  ```
                  az storage account create --name <storage name> --location <location> --resource-group <resource group name> --sku Standard_LRS
                  ```
              - Create a Python function app running on Linux
                 Type:
                 ```
                 az functionapp create --resource-group myResourceGroup --os-type Linux \
                 --consumption-plan-location westeurope  --runtime python \
                 --name <app_name> --storage-account  <storage_name>
                 ```
              - Deploy the function app project
                 Type:
                 ```
                 func azure functionapp publish <app_name>
                 ```
              - Test the function
                 Browse:
                 ```
                 https://<app_name>.azurewebsites.net/api/MyHttpTrigger?name=<yourname>
                 ```
         - CallBatchScoring function
            - Create a function
               - Type: func new
               - Choose template: **HTTP trigger**
               - Choose Function name: **CallBatchScoring**
            - Add requests library
               - Type:
                  ```
                  pip install requests
                  ```
            - Run the functions locally
               - Type: **func host start** (remember to do this in the function projects folder)
               - Copy URL and paste in browser:
               ```
               http://localhost:7071/api/CallBatchScoring?name=<yourname>
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
