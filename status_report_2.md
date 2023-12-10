# Status Report 2 - 11/17/2023

## Table of Contents

- [Accomplishments](#accomplishments)
- [Team Contributions](#team-contributions)
- [Additional Project Scope](#additional-project-scope)
- [Next Steps](#next-steps)
- [Retrospective](#retrospective)

## Accomplishments

The following work has been accomplished so far in setting up a DevOps infrastructure for the coffee project:

### Docker Image

- We created the [docker image](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/coffee-project/Dockerfile) required to run the coffee-project as container.

- We also created the GitHub Packages repository in GitHub.com as it wasn't supported in GitHub.ncsu.edu, where we publish our docker images to be consumed during deployment.

### Branch Protection Rules

We currently have the following [branch protection rules](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/settings/branch_protection_rules/1603) in place for the master branch:

1. A minimum of one reviewer required
2. The build-test step should succeed before the pull request can be merged

### Build, Test & Publish

<img width="625" alt="image" src="https://media.github.ncsu.edu/user/26488/files/bbfe1857-cdc4-48e7-aa58-b4e4a2b3210e">

Workflow: [build-test-publish.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/.github/workflows/build-test-publish.yml)

This workflow has 2 stages:

1. [build-test](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/actions/runs/74797/job/153096): This installs the required dependencies and runs the following checks:

    - Application Lint: We added eslint configuration to the existing coffee project to run the eslint checks on the code base. The existing application has many errors that are printed in [deployment logs](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/actions/runs/74797/job/153096) but it currently has continue-on-error parameter set as true which lets the step pass even with errors as we currently do not intend to fix these errors.

    - [Unit Tests and Coverage](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/actions/runs/74797/job/153096): We run the existing unit tests in the coffee-project app and ensure the test coverage is greater than 90% to pass the step.

    - [Ansible Lint](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/actions/runs/74797/job/153096): We run ansible linting checks for the anible playbooks in the repository. We currently have 4 errors but we haven't fixed them just to showcase how the errors show up in the summary of workflow as [annotations](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/actions/runs/74797). We will fix this before the final submission.

2. [publish](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/actions/runs/74797/job/153097): This builds the docker image of the coffee-project and publishes it to GitHub Packages. 

    - Here we have 2 identical steps of build and publish, this is because we run the [Master publish](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/.github/workflows/build-test-publish.yml#L62) with tag latest only when the pipeline is run from master branch, but when run from any other branch it deploys with tag dev. This tag is used during the deployment stage, i.e. the docker image with tag dev is deployed in the development environment while the latest tag is used to deploy in all other environments. This provides an opportunity for developers to see their changes in a deployment environment similar to production.

    - This step doesn't run when this pipeline is run as part of a PR as we don't want the docker image to build and publish unnecessarily for every PR. This we have ensured by following if conditions in the publish step: 
    
        `if: github.ref == 'refs/heads/master' || github.ref == 'refs/heads/development' || github.event_name == 'workflow_dispatch'`

### Deploy

<img width="1021" alt="image" src="https://media.github.ncsu.edu/user/26488/files/2f654674-36e6-40ff-b828-4c3dddfc4bd7">

#### Workflows: 

1. [deploy.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/.github/workflows/run-ansible.yml)
2. [deploy-template.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/.github/workflows/deploy-template.yml)

#### Ansible Playbooks:

1. [setup-docker.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/playbooks/setup-docker.yml) - This is responsible for setting up the infrastructure in the vcl, i.e. required packages and docker
2. [deploy-application.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/playbooks/deploy-application.yml) - This is responsible for pulling the docker image from GitHub packages and deploying it onto the host
3. [open-port.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/playbooks/open-port.yml) - This is responsible for opening up port 3000 so that the website is accessible over the internet.

### Machines:

In total, we plan to have 8 VCL machines for the entire project for the following purposes:

1. Control Node and GitHub Runner
2. DEV environment
3. QA environment
4. UAT environment
5. Baking environment
6. PRD environment load balancer
7. PRD machine 1
8. PRD machine 2

#### Highlights

The deployment workflow is responsible for deploying the coffee-project onto the following environments:
1. [DEV](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/deployments/activity_log?environment%253Ddev)
2. [QA](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/deployments/activity_log?environment%253Dqa)
3. [UAT](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/deployments/activity_log?environment%253Duat)
4. [Baking](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/deployments/activity_log?environment%253Dbaking)
5. PRD - Work in Progress

We have made use of the following GitHub features and some custom-developed features to make the workflows reusable and efficient:

1. Variable groups: We created a github action [set-variable](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/.github/actions/set-variable/action.yml), which allows us to have different [variable groups](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/tree/master/.github/variables) for different environments and this action converts those variables into environment variables for workflow to use.

2. Workflow Templates: We created one [template](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/.github/workflows/deploy-template.yml) to set up an infrastructure and deploy the coffee project and used it across the environment with input variables to allow it to deploy across environments. This template is consumed in the main workflow [deploy.yml](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/.github/workflows/run-ansible.yml).

3. Environments: We created [environments](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/settings/environments) to allow for easy tracking of deployments and also add manual approvals for certain environments. We also output the deployed website URL in the pipeline run for ease of access for developers with the help of environments in the workflow. (See the blue hyperlinks below each stage: https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/actions/runs/74800)

#### Stages

1. DEV: In this stage, we only set up infra and deploy the app in the development environment.

2. QA: Once the dev succeeds, we deploy the app in the QA environment and thus we run the following tests:

    <img width="621" alt="image" src="https://media.github.ncsu.edu/user/26488/files/5bc4a9b8-fb81-44b6-b9b0-78be6399eb66">

    - [Integration Tests](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/coffee-project/test/integration-tests/integration.test.js): We wrote integration tests for the coffee-project which invokes the deployed APIs and ensured the orders are placed successfully.

    - [UI Tests](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/coffee-project/test/ui-tests/ui.test.js): We wrote UI tests that open up the webpage, clicks on the order button and then ensures a popup is visible with Ordered text.

    - Security Tests: We perform an OWASP ZAP scan on the deployed application and publish the output as an [artifact](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/suites/74991/artifacts/170) with results. We currently let it continue even if security vulnerabilities are detected as we don't have a plan to fix all issues currently.

3. UAT: Once QA and all its tests succeed we deploy to the UAT environment and run load tests as a [python script](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/blob/master/performance-metrics/load-test.py), by invoking the website 1000 times parallelly and getting the average response time and ensure it is below the acceptable threshold which for now we have set as 3 seconds.

4. Baking: To initiate deployment to this environment we have added a manual approval check-in [environment settings](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/settings/environments/3548/edit), i.e. we want someone to manually approve the deployment from UAT to Baking. In baking, we intend to get more performance metrics related to the deployed environment i.e. the VCL in our case, i.e. monitor its CPU and Memory and ensure it's below the threshold.

### Team Contributions:

1. Ameya (agvaicha)
- All Commits: https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/commits?author=agvaicha
- Primary Contributions: Ansible Playbooks, VCL setup and configuration, Deployment Workflow, Integration Tests ([commit](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/commit/f01de1a8e9ec299d20c56d9bf82acc317070e30f))

2. Deep (dmmehta2)
- All Commits: https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/commits?author=dmmehta2 + (Commits in name Deep Mehta)
- Primary Contributions: Linting, Code Coverage, Workflow Templates, Variable Group Action, UI & OWASP Tests, Environment Setup ([commit](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/pull/20))

3. Subodh (sgujar)
- All Commits: https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/commits?author=sgujar
- Primary Contributions: Build, Test, Publish Workflow, GitHub Packages Setup, Ansible Playbooks, Load Testing Script ([commit](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/commit/e9a4f2c340c062ff50c4ae413a9ba4f5051afe7a))

## Additional Project Scope

1. Implementing a Multi-Stage Deployment Process encompassing key environments: Quality Assurance, User Acceptance, Baking, and Production. [Completed]

2. Conducting comprehensive tests at each stage to evaluate different facets of the application. Successful tests lead to progression to the next stage, accompanied by user notifications in case of failures. [Completed]

3. Orchestrating a Production environment with three VCL machines, featuring one as a load balancer and the remaining two as application instances.  [In-progress]

4. Configuration of a GitHub template to facilitate application deployment across diverse environments, ensuring the reusability of the pipeline. [Completed]

5. Adding a security aspect in the QA environment to identify and address vulnerabilities within the application. [Completed]

6. Implementation of integration testing and UI testing in the QA environment. [Completed]

7. Integration of a load testing script in the UAT environment to monitor the application's performance. [Completed]

8. Implementation of monitoring mechanisms in the Baking and Production environments, focusing on CPU utilization and memory usage metrics before initiating production deployment. [In-progress]

9. Adoption of a Blue-Green Deployment strategy for production releases, based on the metrics discussed in [8]. [Next Sprint]

10. Incorporating a robust rollback mechanism to revert to the previous release in the event of production errors post-deployment, within a predefined time slot. [Next Sprint]
  

## Next Steps

1. Ameya (agvaicha)
- Develop a script to determine performance metrics in the baking and production environment.
- This will take about 40 hours of work as it involves determining how to collect app metrics how to measure environment metrics, and the thresholds for the same.

2. Deep (dmmehta2)
- Integrate the rollback mechanism into the deployment workflow if the production environment metrics aren't meeting the standards.
- This will take about 30-40 hours of work as it involves writing another step in the deployment workflow after the production deployment that runs after a certain wait time and then runs the script created by Ameya. If the script fails, then the previous docker image will have to be pulled and deployed using Ansible, for this the Ansible playbooks need to be modified.

3. Subodh (sgujar)
- Implement load balancing setup for the production environment and allowing for blue/green deployment by using a load balancer and two prod servers.
- This will take about 40 hours of work as it involves setting up the Ansible playbook for the load balancer and setting up the appropriate algorithm for the same. Also, another important part is to determine how the blue-green deployment can be made possible in the current workflow.

## Retrospective

### What worked
1. Equal distribution of tasks such as load testing script, integration testing, and UI testing.
2. Planning before implementation of the pipeline for execution of the above tests in different environments.

### What did not work
1. The use of a single self-hosted runner led to bottlenecks, requiring waiting for other jobs to complete and slowing down the verification process for each change.
2. For load testing we need to use asynchronous programming for gathering response times which was challenging and time-consuming for a small task.

### Things to do differently
1. Set up two or three GitHub Actions runners so multiple jobs can run at the same time. This means less waiting and getting things done faster.
2. Learn more about asynchronous programming which will be required for monitoring script for comparison of baking and production environment.
