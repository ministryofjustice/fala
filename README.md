# Find a Legal Adviser

## Install Python 3 with Virtualenv (OSX)

```
brew install python3
virtualenv -p python3 venv
source venv/bin/activate
```

## Development

:memo: The application assumes Node.js 8 to be installed.

Install NPM dependencies (Gulp, Mojular etc.):

```
npm install
```

Install Python depencenies:

```
pip install -r requirements/base.txt
```

Run Django server:

```
python3 ./manage.py runserver
```

Run Gulp tasks (default task is `build`):

```
gulp serve
```

Serve task will create a proxy server on port 3000 that goes via Django’s server on port 8000 enhancing it with
additional features provided by [Browsersync](http://www.browsersync.io/), such as CSS/JS reload, interaction
synchronisation and much more.
