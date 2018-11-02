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
virtualenv -p python3 venv
source env/bin/activate

pip install -r requirements/base.txt
npm install
npm run build
```

Create a ``local.py`` settings file from the example file:

```
fala/settings/local.example.py fala/settings/local.py
```

Next, run the Django server with:

```
python3 ./manage.py runserver
```
