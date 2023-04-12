# Installation

## Dependencies

- [Virtualenv](http://www.virtualenv.org/en/latest/)
- [Python 3](http://www.python.org/) (Can be installed using `brew install python3`)
- [nodejs.org](http://nodejs.org/) (v8.12 - can be installed using [nvm](https://github.com/creationix/nvm))
- [docker](https://www.docker.com/) - Only required for running application from Docker

## Manual Installation

Clone the repository:
```
git clone git@github.com:ministryofjustice/fala.git
```
Next, create the environment and start it up:

```
cd fala
virtualenv -p python3 env
source env/bin/activate

pip install -r requirements/generated/requirements-production.txt
# We cannot directly call npm install because some packages have not update how they bring in their dependencies as the 
# unauthenticated git:// no longer works see https://github.blog/2021-09-01-improving-git-protocol-security-github/#no-more-unauthenticated-git for more details
./npm_install_wrapper.sh
npm run build
```

Create a ``local.py`` settings file from the example file:

```
cp fala/settings/local.example.py fala/settings/local.py
```

Next, run the Django server with:

```
python3 ./manage.py runserver
```
