# Getting started with AML

Learn how to use Azure Machine Learning services for experimentation and model management.

- Browse: [how-to-use-azureml][how-to-use-azureml] > [machine-learning-pipelines][machine-learning-pipelines] > [pipeline-batch-scoring][pipeline-batch-scoring]
   - Prerequisites
      - Azure subscription
      - Resource Group
         - Type: ``**<your name>**``
      - AML workspace
         - Type: **azure machine learning**
         - Click: **Machine Learning service workspace** > **Create**
         - Type: ``<your AML workspace name>``
         - Select: ``<your subscription>``
         - Select: ``<your resource group>``
         - Select: ``<your location>``
         - Click: **Create**
   - Set up [DSVM][setup-dsvm] (bootstrap environment)
      - Create DSVM
         - Browse: **portal.azure.com**
         - Select: ``<your resource group>``
         - Click: **+ Add**
         - Type: **dsvm**
         - Click: **Data Science Virtual Machine for Linux (Ubuntu)** > **Create**
         - Select: ``<your subscription>``
         - Select: ``<your resource group>``
         - Type: Virtual machine name: ``<your vm name>``
         - Select: ``<your vm region>``
         - Select: **Authentication**
         - Type: **Password**
         - Type: Username: ``<your user name>``
         - Type: Password: ``<your password>``
         - Click: **Review + create** > **Create**
      - Setup DSVM
         - SSH into DSVM
         - Clone repo
            - Type **git clone https://github.com/Azure/MachineLearningNotebooks.git**
         - Activate Conda environment
            - Type **conda activate py36**
         - Verify SDK access and version
            - Type: **python**
            ```python
            import azureml.core
            print(azureml.core.VERSION)
            ```
            - Should see something like: **output: 1.0.2**
         - Install additional libraries
            - Type: **conda install -y matplotlib tqdm scikit-learn**
      - Connect to Jupyter notebook
         - Setup port forwarding (to access Jupyter Notebook locally)
            - Expand: **Connection** > **SSH** > **Tunnels**
            - Type: Source port: **8000**
            - Type: Destination: **localhost:8000**
            - Click: **Add** > **Save**
            - SSH into DSVM
         - Browse: https://localhost:8000
         - Login using VM's username/password
      - Run Configuration Notebook
         - Click: **AzureML** > **configuration.ipynb**
         - Run: first cell (verify SDK version)
            - Should see something like version 1.0.2
         - From SSH command line:
            - Type: **az login**
               - Copy link and paste in code
               - Login
            - Type: **az provider show -n Microsoft.ContainerInstance -o table**
            - If not registered, type: **az provider register -n Microsoft.ContainerInstance**
         - Replace default values in second cell and run
         - Run: third cell to access workspace
         - Run: fifth cell to create CPU cluster (skip fourth cell, which creates AML workspace. Also skip sixth cell, which created GPU cluster)
      - Run batch scoring notebook
         - Click: **AzureML** > **how-to-use-azureml** > **machine-learning-pipelines** > **pipeline-batch-scoring** > **pipeline-batch-scoring.ipynb**
         - Run: first cell for imports
         - Run: second cell for settings
         - Run: third cell to create data store
         - Run: fourth cell to create default data store
         - Run: fifth cell to configure data references
         - Run: sixth cell to create and attach compute targets
         - Run: seventh cell to create directory for model
         - Run: eighth cell to download model as tar
         - Run: ninth cell to register model with workspace
         - Run: tenth cell to specify environment to run the script
         - Run: eleventh cell to specify parameters
         - Run: twelfth cell to create the pipeline step
         - Run: thirteenth cell to run the pipeline
         - Run: fourteenth cell to monitor the run
         - Run: fifteenth cell to wait for completion (takes about 20 minutes)
         - Run: sixteenth cell to download output
         - Run: seventeenth cell to sample the output
         - Run: eighteenth cell to create a published pipeline
         - Run: nineteenth cell to get AAD token
         - Run: twentieth cell to run published pipeline (with specified batch size)
         - Run: twenty first cell to monitor the new run (takes about 11 minutes)
      - Call from REST Client
         - Open: RESTClient Firefox plugin
         - Method: POST
         - URL: ``<your endpoint>``
         - Header: Key: **Authorization**, Value: ``<your bearer token>``
         - Header: Key: **Content-Type**, Value: **application/json**
         - Body: {"ExperimentName": "batch_scoring", "ParameterAssignments": {"param_batch_size": 50}}
         - Click: **Send**
      - Schedule using ADF
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
      - Schedule using AzureFunction
         - Browse: **portal.azure.com**
         - Select: ``<your resource group>``
         - Click: **+ Add**
         - Type: **function**

<!-- links -->

[how-to-use-azureml]: https://github.com/Azure/MachineLearningNotebooks/tree/master/how-to-use-azureml
[machine-learning-pipelines]: https://github.com/Azure/MachineLearningNotebooks/tree/master/how-to-use-azureml/machine-learning-pipelines
[pipeline-batch-scoring]: [https://github.com/Azure/MachineLearningNotebooks/tree/master/how-to-use-azureml/machine-learning-pipelines]
[setup-dsvm]: https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-configure-environment#dsvm
[functions-create-scheduled-function][https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-scheduled-function]
