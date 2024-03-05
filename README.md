
# Demo Devops Python

  

This is a simple application to be used in the technical test of DevOps.

  

## Getting Started

  

### Prerequisites

  

- Python 3.11.3

  

### Installation

  

Clone this repo.

  

```bash

git  clone  https://bitbucket.org/devsu/demo-devops-python.git

```

  

Install dependencies.

  

```bash

pip  install  -r  requirements.txt

```

  

Migrate database

  

```bash

py  manage.py  makemigrations

py  manage.py  migrate

```

  

### Database

  

The database is generated as a file in the main path when the project is first run, and its name is `db.sqlite3`.

  

Consider giving access permissions to the file for proper functioning.

  

## Usage

  

To run tests you can use this command.

  

```bash

py  manage.py  test

```

  

To run locally the project you can use this command.

  

```bash

py  manage.py  runserver

```

  

Open http://localhost:8000/api/ with your browser to see the result.

  

### Features

  

These services can perform,

  

#### Create User

  

To create a user, the endpoint **/api/users/** must be consumed with the following parameters:

  

```bash

Method:  POST

```

  

```json

{

"dni": "dni",

"name": "name"

}

```

  

If the response is successful, the service will return an HTTP Status 200 and a message with the following structure:

  

```json

{

"id": 1,

"dni": "dni",

"name": "name"

}

```

  

If the response is unsuccessful, we will receive status 400 and the following message:

  

```json

{

"detail": "error"

}

```

  

#### Get Users

  

To get all users, the endpoint **/api/users** must be consumed with the following parameters:

  

```bash

Method:  GET

```

  

If the response is successful, the service will return an HTTP Status 200 and a message with the following structure:

  

```json

[

{

"id": 1,

"dni": "dni",

"name": "name"

}

]

```

  

#### Get User

  

To get an user, the endpoint **/api/users/<id>** must be consumed with the following parameters:

  

```bash

Method:  GET

```

  

If the response is successful, the service will return an HTTP Status 200 and a message with the following structure:

  

```json

{

"id": 1,

"dni": "dni",

"name": "name"

}

```

  

If the user id does not exist, we will receive status 404 and the following message:

  

```json

{

"detail": "Not found."

}

```

## DevOps Technical Test

This is part of the DevOps Technical Test.

### General information
This repo is connected to an Azure DevOps pipeline. Any updates to the main branch triggers the pipeline to test, build and deploy the image to a Kubernetes cluster using AKS offering from Microsoft Azure.

The diagram of the application is detailed below:
![Django demo app diagram](https://github.com/ngonsoto/demo-devops-python/blob/main/images/django-demo-app-diagram.png)

### Application containerization
The containerization process is detailed on the `dockerfile` file on the root of the directory.

Use the following command to build it:

     docker build -t demo-devops-python:0.0.1 .

To run it locally, use the following command:

    docker run -it -p 8000:8000 demo-devops-python:latest


### CI Pipeline
  The CI pipeline is detailed on the `azure-pipelines.yml` file on the root of the directory. The process consist in preparing the test environment, run the corresponding tests, build and publish the image to an Azure Container Registry.

The testing phase covers the following:

 - Unit tests.
 - Static code analysis
 - Code coverage

To run the pipeline, ensure that the Azure DevOps (ADO) project has access to this repo, and either push a new version to the `main` branch or run the pipeline manually from ADO.

![Unit testing result](https://github.com/ngonsoto/demo-devops-python/blob/main/images/testingResult.png)

![Code coverage result](https://github.com/ngonsoto/demo-devops-python/blob/main/images/codeCoverageResult.png)

### CD Pipeline
The CD Pipeline is triggered everytime a new image is pushed onto the Azure Container Registry. The image is then pushed to an Azure Kubernetes Service using the manifests on the `k8s` folder of this repository. The pipeline automatically pushes the new version to a DEV environment and after that, manual approving is required to do the same onto a PRD environment.

The following resources are pushed onto the Kubernetes cluster as part of this pipeline:

 - Deployment with 2 pods.
 - LoadBalancer service.
 - Horizontal pod autoscaler.
 - Storage class for Azure Files.
 - Persisten volume claim.

To apply them manually, use the following command:

    kubectl apply -f k8s/deployment.yaml

On AKS cluster we just create a `LoadBalancer` and Azure assigns a PIP for the service. On a local machine, using minikube for example, this approach wouldn't work. Instead we create a service of type `ClusterIP` and then create and Nginx Ingress to allow external traffic. Additional manifests are included on `k8s/ingress.yaml` and `k8s/service2.yaml` to achieve this however the **Load Balancer method remain as the main method for this pipeline**.

The commands for the ingress method are detailed below:

    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm install nginx-ingress ingress-nginx/ingress-nginx
    kubectl apply -f k8s/service2.yaml
    kubectl apply -f k8s/ingress.yaml

![Release pipeline result](https://github.com/ngonsoto/demo-devops-python/blob/main/images/releasePipeline.png)
![Release pipeline tasks result](https://github.com/ngonsoto/demo-devops-python/blob/main/images/releasePipelineTasks.png)


### Access the application
The Django application was deployed onto a public AKS, the URL is detailed below:

 - django-4-157-8-231.eastus.cloudapp.azure.com
   
### Test horizontal autoscaling
To test horizontal pod autoscaling (HPA), use the following command:

    kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://django-4-157-8-231.eastus.cloudapp.azure.com; done"

  HPA is configured to scale up to 6 pods when overall CPU usage is above 50%. The command above should trigger the HPA approximately 1 to 2 minutes after running it.

![HPA scaling after detecting sustained 50% cpu usage](https://github.com/ngonsoto/demo-devops-python/blob/main/images/autoscaling.png)
  
### To do / Things to add or change

 - Environment variables are not being properly managed in this release. While the pipelines have different for the different environments, currently secrets are shared between environments. Dockerfile is probably copying the .env file into the container in the build process and thus all environments share the same credentials.
 - CI pipeline does not run any other test after building process is complete. It would be nice to run a vulnerability scan and a smoke test but is not implemented at the moment.
 - SQLite Database is being shared with Azure Files between pods of the same deployment. However, SQLite is not an optimal database for horizontal scaling as it requires to lock the file to add data to it. I tried to minimize application modification for this test, however in a PRD environment it would be better to make the migrations to a MySQL/PostgreSQL database and run it as a separate container from the app pods.
 - IaC is not implemented on this release. Process would have been implementing the Resource Group, AKS and ACR in Azure through Terraform.

## License

  

Copyright © 2023 Devsu. All rights reserved.
