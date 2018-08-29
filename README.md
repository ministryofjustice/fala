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

Create `fala/settings/local.py`:
```
cp fala/settings/local.example.py fala/settings/local.py
```

Run Django server:

```
python3 ./manage.py runserver
```

Build assets:
```
gulp build
```

Or run Gulp tasks (default task is `build`):

```
gulp serve
```

Serve task will create a proxy server on port 3000 that goes via Django’s server on port 8000 enhancing it with
additional features provided by [Browsersync](http://www.browsersync.io/), such as CSS/JS reload, interaction
synchronisation and much more.

## Releasing

### Releasing to non-production

> Currently, `staging` is the only non-production environment.

1. Wait for [the Docker build to complete on CircleCI](https://circleci.com/gh/ministryofjustice/fala) for the feature branch.
1. Copy the `feature_branch.<sha>` reference from the `build` job's "Push Docker image" step. Eg:
    ```
    Pushing tag for rev [3e1a4ef9ecf6] on {https://registry.service.dsd.io/v1/repositories/fala/tags/github-config.843dcc7}
    ```
1. [Deploy `feature_branch.<sha>`](https://ci.service.dsd.io/job/DEPLOY-fala/build?delay=0sec).
    * `ENVIRONMENT` is the target environment, select "staging".
    * `DEPLOY_BRANCH` is the branch that needs to be released (`github-config` in the above example).
    * `VERSION` is either `latest` for the last successful build on that branch, or a specific 7-character prefix of the Git SHA (`843dcc7` in the above example).


### Releasing to production

1. Please make sure you tested on a non-production environment before merging.
1. Merge your feature branch pull request to `master`.
1. Wait for [the Docker build to complete on CircleCI](https://circleci.com/gh/ministryofjustice/fala/tree/master) for the `master` branch.
1. Copy the `master.<sha>` reference from the `build` job's "Push Docker image" step. Eg:
    ```
    Pushing tag for rev [ec16b48c493d] on {https://registry.service.dsd.io/v1/repositories/fala/tags/master.2d889b5}
    ```
1. [Deploy `master.<sha>` to **prod**uction](https://ci.service.dsd.io/job/DEPLOY-fala/build?delay=0sec).

:tada: :shipit: