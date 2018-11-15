# Development

Assets reside in `fala/assets-src` directory and compiled in `fala/assets` directory upon running build tasks.

FALA is using [Gulp](http://gulpjs.com/) for build tasks. The following Gulp tasks are used in development:

- `build` builds and minifies all assets and does all of the following
- `sass` builds the SCSS and generates source maps
- `serve` watches the files for changes and reloads the browser using [BrowserSync](http://www.browsersync.io/)

:memo: It is also possible to use `npm run build` and `npm run serve` instead of gulp directly.


Serve task will create a proxy server on port 3000 that goes via Django’s server on port 8000 enhancing it with
additional features provided by [Browsersync](http://www.browsersync.io/), such as CSS/JS reload, interaction
synchronisation and much more.

## Running Nginx and Django locally
You must refer to the name of the `webapp` container in `nginx.conf.

Update `nginx.conf`:

```
upstream webapp {
    server localhost:8000;
}
```
to:
```
upstream webapp {
    server webapp:8000;
}
```

Then run:

```
docker-compose up
```

and visit http://localhost:8002
