# Find a Legal Adviser

This repository holds the code for the "Find a legal aid adviser or family mediator" application. The service helps members of the public in England and Wales to search for a legal adviser or family mediator with a legal aid contract.

The website address is https://find-legal-advice.justice.gov.uk/.

## Public API

The website uses the LAA Legal Adviser API. The code is hosted at https://github.com/ministryofjustice/laa-legal-adviser-api.

The REST API is https://prod.laalaa.dsd.io/.


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
interact with web pages programmatically.It's often used for automated testing, web scraping, and 
browser automation tasks.

Playwright will not work if FALA is not up and running as it interacts with its URL endpoints.

### PlayWright Testing Locally

PlayWright is used for browser based testing. Once you have performed * [Installation via virtualenv,](docs/virtual-env.md) Please perform the following below.

You'll likely have a terminal which is being used to run FALA, you'll need to open another terminal
and `source venv/bin/activate` within the new shell and copy and paste to install playwright browser plugins:

`playwright install`

This will install all required browsers support for playwright to work on. You will only need to do this once.

Using the same terminal from above, execute playwright tests:

`pytest playwright`

Note: The appended `playwright` is directory where to look for playwright related tests.

Note: Running pytest in FALA directory without going into the playwright directory will run every python test in the 
project. Ensure you are in the correct directory when running playwright tests.

### Docker

Please ensure your internet network such as your VPN does not interfere with your build.

To run container:

`./run_local.sh`

This shell script contains commands that build and runs the fala app.

If you're not using `Docker Desktop`, you may want to have two terminals open.

### PlayWright Testing with Docker

Playwright has its own Docker container. Tests are not executed in the FALA Docker container but instead inside a 
Playwright Docker container, which looks for FALA's URLs to test against.

You will need the FALA Docker container running in order for the tests to work, as the Playwright Docker container 
interacts with FALA's URLs. You can do this by doing the following:

`./run_local.sh`

To spin up the Playwright Docker container, do the following:
`docker-compose up -d --build playwright`

This Playwright Docker container executes playwright tests (Copied from the repo's playwright directory) 
against the FALA Dock container. It's important that you have set up your environment files correctly in your repo so
the connections can work.

The Playwright Docker container executes all Playwright tests within the playwright directory of the project. 
Once the tests are complete, the container will shut itself down.

### PlayWright Testing in Docker While Developing

If you want to keep the Playwright Docker container running and use it alongside your development environment, 
you can do the following:
`docker-compose run --entrypoint sh playwright`

Tip: Remember to type `bash` first when interacting with a Docker container.

This allows you to bash into the Playwright Docker container. From there, you can change the directory to `fala_local`:
`cd ../fala_local/playwright/`

`fala_local` directory reflects your local IDE changes in the Playwright container. Here, you can interact with the 
command line to run your tests as many times as you like without having to delete and rebuild the Playwright Docker 
container.

To run tests inside the bashed docker directory `fala_local/playwright/`, you can run:
`pytest`

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


## Documentation
* [Installation via virtualenv](docs/virtual-env.md)
* [Using Kubernetes](docs/kubernetes.md)
* [Releasing](https://github.com/ministryofjustice/laa-civil-legal-aid-documentation/blob/master/releasing/kubernetes.md)
(opens in https://github.com/ministryofjustice/laa-civil-legal-aid-documentation)
* [Requirements files](requirements/README.md)
