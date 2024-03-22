# Installation

## Dependencies

### Pyenv, python3

"pyenv" is used to provide python3. (Other CLA repos need different versions, so good to be able to .)

1. Install pyenv with brew:

        brew install pyenv

2. Set up your shell for pyenv. Make the changes to `~/.zshrc` described here: [Set up your shell for pyenv](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv) (This is so that pyenv's python binary can be found in your path)

3. To make the shell changes take effect:

        exec "$SHELL"

    (or alternatively, restart your shell)

4. Install into pyenv the python version this repo uses (which is defined in `.python-version`):

        pyenv install 3.12 --skip-existing

### NodeJS v10.x

It's suggested to use 'nvm' to install this old version of Node.

1. Install NVM: https://github.com/nvm-sh/nvm#install--update-script

2. Install the NodeJS version:

   nvm install 10.24

You can check your NodeJS version:

node --version

## Manual Installation

Clone the repository:
```
git clone git@github.com:ministryofjustice/fala.git
```
Next, create the environment and start it up. Ensure you are in the top level folder:

```
python3 -m venv venv
source venv/bin/activate
```
Install the requirements for this project

```
pip install -r requirements/generated/requirements-dev.txt
```

Assets reside in `fala/assets-src` directory and compiled in `fala/assets` directory upon running build tasks.

FALA uses [Gulp](http://gulpjs.com/) for build tasks. The following Gulp tasks are used in development:

- `build` builds and minifies all assets and does all of the following
- `sass` builds the SCSS and generates source maps
- `serve` watches the files for changes and reloads the browser using [BrowserSync](http://www.browsersync.io/)

:memo: It is also possible to use `npm run build` and `npm run serve` instead of gulp directly.

Before running this command, make sure you are using the correct version of node. 
This can be changed using nvm

The following commands will import the assets including CSS into your local environment:
```
npm install
npm run build
./manage.py collectstatic --noinput      
```

Create a ``local.py`` settings file from the example file:

```
cp fala/settings/local.example.py fala/settings/local.py
```

LAALAA_API_HOST has to be set to a valid host running laa-laa-api, otherwise the Django server doesn't start

Next, run the Django server with:

```
python3 ./manage.py runserver
```

## Running tests
```
python3 ./manage.py tests 
```

## Lint and pre-commit hooks

To lint with Black and flake8, install pre-commit hooks:
```
. venv/bin/activate
pip install -r requirements/generated/requirements-dev.txt
pre-commit install
```

To run them manually:
```
pre-commit run --all-files
```
