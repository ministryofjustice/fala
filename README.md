# Find a Legal Adviser

This repository holds the code for the "Find a legal aid adviser or family mediator" application. The service helps members of the public in England and Wales to search for a legal adviser or family mediator with a legal aid contract.

The website address is https://find-legal-advice.justice.gov.uk/.

## Public API

The website uses the LAA Legal Adviser API. The code is hosted at https://github.com/ministryofjustice/laa-legal-adviser-api.

The REST API is https://prod.laalaa.dsd.io/.

## Dependencies
- [docker](https://www.docker.com/)

## Installation for development

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

When pdb.set_trace() is reached, you will be able to debug from the command line.

https://docs.python.org/3/library/pdb.html


## Documentation
* [Installation via virtualenv](docs/virtual-env.md)
* [Using Kubernetes](docs/kubernetes.md)
* [Releasing](https://github.com/ministryofjustice/laa-civil-legal-aid-documentation/blob/master/releasing/kubernetes.md)
(opens in https://github.com/ministryofjustice/laa-civil-legal-aid-documentation)
* [Requirements files](requirements/README.md)
