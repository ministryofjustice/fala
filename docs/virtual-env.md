# Virtual-env install

This describes installing fala locally for development purposes.

## Dependencies

### Python & pyenv

"pyenv" is the tool we use to install and use the correct version of Python. (Other CLA repos need different python versions, and we've settled on pyenv as the best way to easily switch versions, depending on the repo you're in.)

1. Install pyenv with brew:

       brew install pyenv

2. Set up your shell for pyenv. Make the changes to `~/.zshrc` described here: [Set up your shell for pyenv](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv) (This is so that pyenv's python binary can be found in your path)

3. To make the shell changes take effect:

       exec "$SHELL"

    (or alternatively, restart your shell)

4. Install into pyenv the python version this repo uses (which is defined in `.python-version`):

       pyenv install 3.12 --skip-existing

When you're in this repo's directory, pyenv will automatically use the version defined in `.python-version`:
```
$ cd fala
$ python --version
3.12
```

If you have the wrong python version in your virtual environment, then it's easiest to delete it and re-create it with the right python version:
```
rm -rf venv
pyenv use
python --version  # check the version is now correct
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/generated/requirements-dev.txt
# etc
```

### NodeJS

It's suggested to use 'nvm' to install this old version of Node.

1. Install NVM: https://github.com/nvm-sh/nvm#install--update-script

2. Install the NodeJS version:

   nvm install 10.24

You can check your NodeJS version:

node --version

## Installation

1. Clone the repository:

       git clone git@github.com:ministryofjustice/fala.git

2. Check your Python version:

       $ cd fala
       $ python --version
       3.12

3. Create the python environment, activate it and install the requirements:

       python3 -m venv venv
       source venv/bin/activate
       pip install -r requirements/generated/requirements-dev.txt

4. Build the assets:

       nvm use
       npm install
       npm run build
       ./manage.py collectstatic --noinput

5. Create a ``local.py`` settings file from the example file:

       cp fala/settings/local.example.py fala/settings/local.py

## Running

Run the Django server with:
```
./manage.py runserver
```

## Assets

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

## Running tests
```
python3 ./manage.py tests 
```

## Lint and pre-commit hooks

To lint with Black and flake8, install pre-commit hooks:
```
source venv/bin/activate
pip install -r requirements/generated/requirements-dev.txt
pre-commit install
```

To run them manually:
```
pre-commit run --all-files
```
