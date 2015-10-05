var $ = require('jquery');
var bindAll = require('lodash/function/bindAll');
var compact = require('lodash/array/compact');
var zipObject = require('lodash/array/zipObject');
var map = require('lodash/collection/map');
var forOwn = require('lodash/object/forOwn');

Mojular.Modules.LabelSelect = {
  el: '.block-label, .radio-inline',

  init: function () {
    bindAll(this, 'render');
    this.cacheEls();
    this.bindEvents();
    this.processQueryString();
  },

  bindEvents: function () {
    this.$options
      .on('change label-select', function () {
        var $el = $(this),
          $parent = $el.parent('label');

        // clear out all other selections on radio elements
        if ($el.attr('type') === 'radio') {
          $('[name=' + $el.attr('name') + ']').parent('label').removeClass('s-selected');
        }

        // set s-selected state on check
        if ($el.is(':checked')) {
          $parent.addClass('s-selected');
        } else {
          $parent.removeClass('s-selected');
        }
      });
    Mojular.Events.on('render LabelSelect.render', this.render);
  },

  cacheEls: function () {
    this.$options = $(this.el).find('input[type=radio], input[type=checkbox]');
  },

  processQueryString: function () {
    var queryStringPairs = location.search.slice(1).split('&');
    queryStringPairs = map(function (item) {
      if (item) {
        var pair = item.split('=');
        return pair[1] ? pair : '';
      }
    });
    queryStringPairs = compact(queryStringPairs);

    var queryStringObject = zipObject(queryStringPairs);

    // Select fields found in query string
    forOwn(queryStringObject, function (value, key) {
      if (value) {
        $('[name="' + key + '"][value="' + value + '"]').click();
      }
    });
  },

  render: function () {
    this.$options.filter(':checked').each(function () {
      $(this).parent().addClass('s-selected');
    });
  }
};
