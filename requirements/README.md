# Requirements files

This policy covers how we manage this repo's "requirements" files.

We want the dependencies to be up-to-date as we can, for security and maintainability reasons. This policy aims to best facilitate upgrading being easy and frequent, but with protections against upgrading to incompatible versions.

## Source vs generated

**Source** requirements files:

* Which are: requirements/source/requirements*.in
* These list the "direct dependencies" of the app. For example the app imports "django", so that is listed
* These are edited by humans (not automated)
* The versions are not "pinned" to an exact version usually - that occurs instead that is done just in the 'Generated' files - see below. This makes it easier to keep the versions up to date - see "Updating dependencies". Pinning in the source files makes it harder to flag if something can't be upgraded, or just hasn't been yet.
* We do add a constraint to guard against major upgrades. For example `boto3` currently on version 1.34 should be specified as `boto3<2`, so that when v2.0 comes out, our next run of pip-compile will stick with the latest of the 1.x series. Major upgrades can be handled separately. (We don't bother constraining dev tools, because backwards incompatibilities are rarely an issue.)
* Occasionally we'll add a tighter constraint, such as `<1.35`, if we know our app is not currently compatible with version 1.35 onwards. A comment is also helpful, to explain the issue. Obviously we try to overcome not upgrading before too long.

**Generated** requirements files:

* Which are: requirements/source/requirements*.txt
* These list the all dependencies of the app - both "direct dependencies" and "transitive dependencies", which are the dependencies of the "direct dependencies". For example, "django" imports "asgiref", so the latter is a transitive dependency.
* The versions are exact - i.e. "pinned"
* When we `pip install` we always use generated dependencies. This ensures we all run the same versions of everything - for development, in CI/CD tests, and on the production server.

## Updating dependencies

### Automated updates - Dependabot or Snyk

These automated tools generally increment the Generated files to the latest. The PRs they create should be tested, and if they work they can be merged.

Note: These automated tools don't look at the .in source files, so the constraints we put in them aren't taken account of. So test well! If the tests fail, then the human can look in the source file's constraint to see if that already records a reason for not being able to upgrade.

### Manual updates

We should occasionally run `pip-compile --upgrade`, to update the generated files with the latest available versions:

```
pip-compile --upgrade --output-file=requirements/generated/requirements-dev.txt requirements/source/requirements-dev.in
pip-compile --upgrade --output-file=requirements/generated/requirements-lint.txt requirements/source/requirements-lint.in
pip-compile --upgrade --output-file=requirements/generated/requirements-pre-commit.txt requirements/source/requirements-pre-commit.in
pip-compile --upgrade --output-file=requirements/generated/requirements-production.txt requirements/source/requirements-production.in
```

Note: Check in case something has been **downgraded**. This is possible because Dependabot/Snyk don't take account of the constraints in the source file. If this happens, then it suggests the constraint should be loosened to include the later version. Test to see what versions are ok.

This method is superior than the Dependabot/Snyk automation, because it does take account of the constraints contained in the source files. So it avoids major breaking changes and known incompatibilities. And it's good for updates across all the dependencies at once. And during testing you find out if new versions are problematic, which require constraints adding to the source files.
