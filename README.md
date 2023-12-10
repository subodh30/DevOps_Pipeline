
# DevOps Project Overview

[![Build, Test & Publish](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/actions/workflows/build-test-publish.yml/badge.svg)](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/actions/workflows/build-test-publish.yml)

[![Deploy](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/actions/workflows/deploy.yml/badge.svg)](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/actions/workflows/deploy.yml)

###  "From Code Chaos to Deployment Symphony"

Software products rely on two main pillars: Development and Operations. In the past, these pillars had separate roles and worked in isolation. DevOps is the key to bridging this gap by making the developer who creates the feature also responsible for deploying it to production. This approach has proven to be very effective and popular in the industry and has been adopted by many large software companies.

The aim of this project is to design and implement DevOps automation using tools like GitHub Actions and Ansible, which enable developers to deliver their features with confidence and efficiency.

## Deliverables

1. [Project Proposal](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/wiki/Project-Proposal)
2. [Status Report 1](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/status-report-1.md)
3. [Status Report 2](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/status_report_2.md)
4. [Final Report](./Final_Report.pdf)

## Pipeline Design

![High Level Pipeline](https://media.github.ncsu.edu/user/26488/files/b3d5d640-4f3c-4dad-8188-c7bd5b2c9497)

![Deployment](https://media.github.ncsu.edu/user/26488/files/cbeded6a-edae-4c44-85c7-884c581d7405)

## Demo Video

https://media.github.ncsu.edu/user/26488/files/13035c98-db45-4ca0-9fb6-e985997730c4


## Work Done

### Coffee Project

- Added [Integration tests](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/coffee-project/test/integration-tests/integration.test.js)
- Added [UI tests](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/coffee-project/test/ui-tests/ui.test.js) with headless driver

### Ansible Playbooks

   - [setup-docker.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/playbooks/setup-docker.yml) - This is responsible for setting up the infrastructure in the vcl, i.e. required packages and docker
   - [deploy-application.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/playbooks/deploy-application.yml) - This is responsible for pulling the docker image from GitHub packages and deploying it onto the host
   - [open-port.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/playbooks/open-port.yml) - This is responsible for opening up port 3000 so that the website is accessible over the internet.
  - [comment_nginx.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/playbooks/comment_nginx.yml) - The playbook updates the NGINX configuration on the load balancer used by the blue-green deployment as well as rollback by commenting out a specific server line with the target IP and then restarting the NGINX service.
  - [uncomment_nginx.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/playbooks/uncomment_nginx.yml) - This reverts the NGINX configuration by uncommenting the server line in the NGINX default file.

  - [deploy-nginx.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/playbooks/deploy-nginx.yml) - This configures the vcl as an NGINX web server, exposes the port 80, restarts the server.
  - [deploy-production.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/playbooks/deploy-production.yml) - This orchestrates the deployment process for a production server, first removing it from the NGINX configuration, setting up Docker, deploying an application, opening a port, and then adding the production server back to the NGINX configuration.

- [hosts.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/playbooks/hosts.yml) - Inventory file with a list of IP addresses of all environments.

### Actions (Set-variable)

- [Variables](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/tree/master/.github/variables): This folder contains all the variable json files that are used in the workflows.

- [set-variables.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/.github/actions/set-variables.yml): This action is responsible for setting up the variables for the workflows. It takes the input as the environment name and sets up the variables for that environment.

### Workflows

- [Build and Publish](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/.github/workflows/build-test-publish.yml): This workflow builds aplications, perofrms unit testing, linting checks and uploades docker image to public github container registery.
- [deploy.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/.github/workflows/deploy.yml): This is the main deployment workflow that is responsible for invoking templates and deploying app to different environments.
- [deploy-template.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/.github/workflows/deploy-template.yml): This is a template workflow which plays an important role in ensuring consistent deployment across environments.
- [rollback.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/.github/workflows/rollback.yml): This workflow allows to deploy a previous stable docker image directly to production environment in case of emergencies when the new features might have caused issues in production environment.



## Mentors
- Prof. John-Paul Ore (jwore)
- Md Rayhanur Rahman (mrahman)

## Team Members
- Ameya Vaichalkar (agvaicha)
- Deep Mehta (dmmehta2)
- Subodh Gujar (sgujar)

## License
This project is licensed under the [MIT License](LICENSE).
