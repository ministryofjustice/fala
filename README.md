# Find a Legal Adviser

This repository holds the code for the "Find a legal aid adviser or family mediator" application. The service helps members of the public in England and Wales to search for a legal adviser or family mediator with a legal aid contract.

The website address is https://find-legal-advice.justice.gov.uk/.

## Public API

The website uses the LAA Legal Adviser API. The code is hosted at https://github.com/ministryofjustice/laa-legal-adviser-api.

## Dependencies
- [docker](https://www.docker.com/)

## Prerequisites
- [Playwright](https://playwright.dev/python/) 

## Installation for development

### .env

We need to do this for our developer settings, so please copy this file over if it doesn't exist and/or you're not using Docker. 

You can use this command in your terminal or manually create a `.env` file: 

`cp .env.example .env` 

### Playwright

Playwright is a tool for automating web browsers. It allows developers to write scripts to control web browsers and 
interact with web pages programmatically. It's often used for automated testing, web scraping, and 
browser automation tasks. We use it to test our end to end user journeys.

For local development and when using Playwright for the first time, run:

`playwright install`

This will install all required browser support required for Playwright to run. 

We've configured Playwright to run with the rest of the app's tests i.e. by running `./manage.py test`. If you'd like to edit
any of the Playwright test settings for debugging purposes, for example running a headed browser, you can configure this in the setup file.

### Docker

Please ensure your internet network such as your VPN does not interfere with your build.

To run container:

`./run_local.sh`

This shell script contains commands that build and runs the fala app.

If you're not using `Docker Desktop`, you may want to have two terminals open.

### Tips for developing with docker containers

Code editing - You can edit the code on your local disk, with a local editor, as normal. (You don't have to edit the 
files inside the Docker container, because your local directory is mounted into container.) When you save a file, it 
becomes present in the container immediately, and the server restarts.

Browsing the app - Point your local browser at http://localhost:8013/

Log output - watch the output generated by the running app using: `docker logs fala -f` or `docker attach fala`

To `exec` into the Fala docker container, start a new terminal and perform the following:

`docker exec -it fala bash`

From the shell inside the container you can run some tests e.g.

`python manage.py test`

Alternatively, some editors have functionality to hook into running containers, such as VS Code's 'Dev Containers' 
extension. Docker Desktop offers a UI version of looking through logs, exec and many other interactions. 

### Debugging
Depending on how you're running the project, via `venv` or Docker you can perform the following debugging:

You can insert a breakpoint with the `breakpoint()` function at any position in your code.

If you're using a docker contain to run your project locally, you can run `docker attach fala` to view the output in 
your chosen terminal.

When breakpoint() is reached, you will be able to debug from the command line.

https://docs.python.org/3/library/pdb.html

## Deploying to Staging and Production

The service uses `helm` to deploy to Cloud Platform Environments via CircleCI. This can be installed using:

`brew install helm`

To view helm deployments in a namespace the command is:

`helm -n <namespace> ls --all`

e.g. `helm -n laa-fala-staging ls --all`

Deployments can be deleted by running:

`helm delete <name-of-deployment>`

e.g. `helm -n  laa-fala-staging delete el-123-fee-change`

It is also possible to manually deploy to an environment from the command line, the structure of the command can be found in `bin/deploy.sh`


## CHECK referrals

As part of improvement works to 'Check if you can get legal aid and Find a legal advisor' (CHECK) in February 2025, a new set of pages & urls were created that would allow users to be sent from CHECK to FALA. Epic for the work can be viewed [here](https://dsdmoj.atlassian.net/browse/EL-1891).

- A user would find their category of law on CHECK
- CHECK would then populate a referral link to FALA with the category pre-populated in the URL
- The user would then enter a postcode on FALA, on the bespoke landing page for that category

All possible URL params are described in the below table:

| **Category**                           | **URL params sent by CHECK**       | **Resolved URL in FALA**                            |
| -------------------------------------- | ---------------------------------- | --------------------------------------------------- |
| Claims against public authorities      | `aap`<br>/check?categories=aap     | {HOST}/check/claims-against-public-authorities      |
| Clinical Negligence                    | `med`<br>/check?categories=med     | {HOST}/check/clinical-negligence                    |
| Community Care                         | `com`<br>/check?categories=com     | {HOST}/check/community-care                         |
| Crime                                  | `crm`<br>/check?categories=crm     | {HOST}/check/crime                                  |
| Debt                                   | `deb`<br>/check?categories=deb     | {HOST}/check/debt                                   |
| Discrimination                         | `disc`<br>/check?categories=disc   | {HOST}/check/discrimination                         |
| Education                              | `edu`<br>/check?categories=edu     | {HOST}/check/education                              |
| Family                                 | `mat`<br>/check?categories=mat     | {HOST}/check/family                                 |
| Family Mediation                       | `fmed`<br>/check?categories=fmed   | {HOST}/check/family-mediation                       |
| Housing                                | `hou`<br>/check?categories=hou     | {HOST}/check/housing                                |
| Housing Loss Prevention Advice Service | `hlpas`<br>/check?categories=hlpas | {HOST}/check/housing-loss-prevention-advice-service |
| Immigration or Asylum                  | `immas`<br>/check?categories=immas | {HOST}/check/immigration-or-asylum                  |
| Mental Health                          | `mhe`<br>/check?categories=mhe     | {HOST}/check/mental-health                          |
| Modern Slavery                         | `mosl`<br>/check?categories=mosl   | {HOST}/check/modern-slavery                         |
| Prison Law                             | `pl`<br>/check?categories=pl       | {HOST}/check/prison-law                             |
| Public Law                             | `pub`<br>/check?categories=pub     | {HOST}/check/public-law                             |
| Welfare Benefits                       | `wb`<br>/check?categories=wb       | {HOST}/check/welfare-benefits                       |


There are also some scenarios in which users coming from CHECK will need to be shown multiple categories. The way the Check search in FALA is set up allows for any combination of categories to be selected. The title of the search is determined by which category is put first in the URL. 

The below URLs are some of the main examples which are used by CHECK:

| **Main Category**   | **Sub Category**     | **URL params sent by CHECK**                             | **Resolved URL in FALA**                    |
| ------------------- | -------------------- | -------------------------------------------------------- | ------------------------------------------- |
| Mental health       | Clinical Negligence  | `mhe` & `med` <br>/check?categories=mhe&sub-category=med | {HOST}/check/mental-health?sub-category=med |

## Documentation
* [Installation via virtualenv](docs/virtual-env.md)
* [Using Kubernetes](docs/kubernetes.md)
* [Releasing](https://github.com/ministryofjustice/laa-civil-legal-aid-documentation/blob/master/releasing/kubernetes.md)
(opens in https://github.com/ministryofjustice/laa-civil-legal-aid-documentation)
* [Requirements files](requirements/README.md)
