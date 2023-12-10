# Status Report 1

## Accomplishments

- [![Build, Test & Publish](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/actions/workflows/build-test-publish.yml/badge.svg)](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/actions/workflows/build-test-publish.yml) Setup which builds the coffee project, runs es lint checks and runs all the unit tests defined in the project and verify that code coverage is greater than 90%
- Publish workflow setup which build and publishes docker image of the application to GitHub packages.
- [![Deploy](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/actions/workflows/run-ansible.yml/badge.svg)](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/actions/workflows/run-ansible.yml) workflow setup with variables and templates to reduce repitions across environments. Currently deploys to only development environment.
- [GitHub environments](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/deployments) setup done 
- [Ansible playbooks](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/tree/master/playbooks) in place to setup infrastructure on host machine and deploy coffee project on host machine.

### Contributions

1. Ameya (agvaicha)
- All Commits: https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/commits?author=agvaicha
- Primary Contributions: Ansible Playbook and Deployment Workflow ([commit](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/commit/e0fa9e2f74cc6f31adc701b84064fbe6300d5e7b))

2. Deep (dmmehta2)
- All Commits: https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/commits?author=dmmehta2 + (Commits in name Deep Mehta)
- Primary Contributions: Linting, Code Coverage Checks and Deployment Templates (https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/pull/3)

3. Subodh (sgujar)
- All Commits: https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/commits?author=sgujar
- Primary Contributions: Build, Test, Publish Workflow and Deployment Workflow ([commit](https://github.ncsu.edu/CCDS-CSC-519/DevOps-Pipelines/commit/f2695da3e322135f14198ea6cf4b264f8ca47a3b))

## Next Steps 

1. Ameya (agvaicha)
- Add remianing environments in deployment pipeline, i.e. QA, UAT, Baking and Prod
- Include appropriate tests in each environment apart from deployment

2. Deep (dmmehta2)
- Add UI Tests in coffee-project for QA environment
- Add load testing script for UAT environment
- Create monitoring code for poduction deployment ( which will compare baking environment and production environment )

3. Subodh (sgujar)
- Add load balancer for production environment
- Add Release tagging for docker images
- Reduce repetitive steps in workflow


## Retrospective

### What Worked
1. Good Communication & collaboration
2. Distribution of workload

### What didn't Work
1. Due to Github enterprise we were facing multiple issues like installing docker
2. NCSU github didn't allow use of container registry. Need to find work-around to use personal ghcr.io for storing docker images
3. Not aloowed to use third party marketplace actions / plugin


### Things to do differently
1. Analyze github environment and access to it before creating workflow file.
2. Setup runner for passwordless access ssh and install docker on it before hand.
3. Reduce repetitive steps in workflow by analyzing and planning before implementing directly.


