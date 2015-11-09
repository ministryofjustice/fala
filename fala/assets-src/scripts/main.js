var Mojular = require('mojular');

Mojular
  .use([
    require('mojular-govuk-elements'),
    require('mojular-moj-elements/modules/devs'),
    require('./find-legal-adviser')
  ])
  .init();
