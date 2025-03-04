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
pyenv local 3.12
python --version  # check the version is now correct
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/generated/requirements-dev.txt
# etc
```

### NodeJS

It's suggested to use 'nvm' to install Node.

1. Install NVM: https://github.com/nvm-sh/nvm#install--update-script

2. Install the NodeJS version (specified in `.nvmrc`):

        nvm install

Now when you run `nvm use` it'll modify your PATH to point to the NodeJS version specified in `.nvmrc`. So if you're swapping between repos with different Node versions, you'll need to rerun `nvm use` each time, or you can [automate it](https://github.com/nvm-sh/nvm?tab=readme-ov-file#deeper-shell-integration).

You can check your NodeJS version:
```
node --version
```

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

5. Create a ``.env`` file from the example file:

       `cp .env.example .env` 

## Running

Run the Django server with:
```
./manage.py runserver
```

## Assets

Frontend assets have their source in `fala/assets-src/` and the build outputs to: `fala/assets/`.

FALA uses [Gulp](http://gulpjs.com/) for this build. The following Gulp tasks are used in development:

- `build` builds and minifies all assets and does all of the following
- `sass` builds the SCSS and generates source maps
- `serve` watches the files for changes and reloads the browser using [BrowserSync](http://www.browsersync.io/)

Usage during frontend development:

1. Ensure you have the correct NodeJS version - see [NodeJS install](virtual-env.md#nodejs)

2. Run the build:

       nvm use
       npm install
       npm run build

3. Serve assets:

       npm run serve

## Running tests
```
python3 ./manage.py test
```

To run a single test, specify the app name, file structure to access the test, test class and test method name:
```
python3 ./manage.py test <app_folder>.<test_folder>.<test_file_name>.<test_class>.<test_method>
```

For example:
```
python3 ./manage.py test adviser.tests.test_results_view.ResultsPageWithBothOrgAndPostcodeTest.test_search_parameters_box_is_visible
```

You can also omit the test method from the command and run the whole class.

Your test files and methods must be prefixed with the word 'test' e.g. `def test_search_parameters_box_is_visible`

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

## Translations and Internalisations

Django is our web-framework, Jinja2 is our templating language, and i18n is an acronym which stands for internationalization. As we are not using Django's template engine, we have to add an extension to the Jinja2 set-up in order to use it's i18n features, enabling the use of translation functions (`_()` or `gettext`) within the Jinja templates.

Typical workflow for creating translations in this project:

- Create/update the `django.po` file with translatable strings (these `-i` flags, ignore folders where we don't want to translate):

```bash
python manage.py makemessages -l cy -i locale -i venv
```

- Add translations in `django.po` file

- Compile the translated `django.po` file into the optimised `django.mo` file:
```bash
python manage.py compilemessages -l cy
``` 

Django will use the `django.mo` file to display translations.

### **To Note**

The `makemessages` command in Django doesn’t understand the syntax of Jinja2 components and is designed to work with Django's default template engine. Therefore any strings in the Jinja2 components that need to be translated, have to be set as Jinja2 variables, within the templates. 

There has been exploration in configuring this app to use `babel`, in order to translate the strings inside Jinja2 components, but the benefits in doing so did not outweigh the current implementation;
- Django’s [documentation](https://docs.djangoproject.com/en/5.1/topics/i18n/translation/#localization-how-to-create-language-files) lacks clear instructions on integrating Babel.
- Babel setup requires extra configuration (e.g., babel.cfg, manual extraction, compilation).
- Using Django’s gettext system from views works well enough without the added complexity.