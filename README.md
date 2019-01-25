# Getting started with AML

Learn how to use Azure Machine Learning services for experimentation and model management.

- Browse: [how-to-use-azureml][how-to-use-azureml]
   - Set up [DSVM][setup-dsvm]
      - Create DSVM
         - Prerequisites: an Azure subscription and a resource group
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

   - Set up AML Workspace

<!-- links -->

[how-to-use-azureml]: https://github.com/Azure/MachineLearningNotebooks/tree/master/how-to-use-azureml
[setup-dsvm]: https://docs.microsoft.com/en-us/azure/machine-learning/service/how-to-configure-environment#dsvm
