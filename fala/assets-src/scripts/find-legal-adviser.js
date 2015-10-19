var $ = require('jquery');
var debounce = require('lodash/function/debounce');
var find = require('lodash/collection/find');
var reduce = require('lodash/collection/reduce');
var reject = require('lodash/collection/reject');

Mojular.Modules.FindLegalAdviser = {
  el: '#resultsMap',
  markers: [],
  searchLocationMarker: null,
  openInfoWindow: null,
  eventsBound: false,

  init: function() {
    this.cacheEls();

    this._handleMQTest();

    if(!this.$resultsMap.length) {
      $('#id_postcode').focus();
      return;
    }

    this.renderMap(this.$resultsMap.data('lat'), this.$resultsMap.data('lon'));
    this._prepareMarkers();

    $(window).resize(debounce($.proxy(this._handleMQTest, this), 500));
  },

  // Handle events which rely on media queries
  _handleMQTest: function() {
    if(window.Modernizr.mq('(min-width: 641px)')) {
      if(!this.eventsBound) {
        this.bindEvents();
      }
    } else if(this.eventsBound) {
      this._unbindEvents();
    }
  },

  bindEvents: function() {
    var self = this;
    // Replace result headings with hyperlinks for accessibility
    this.$organisationListItems.find('.org-summary').each(function() {
      $(this).replaceWith('<a class="' + this.className + '" aria-expanded="false" href="#">' + $(this).html() + '</a>');
    });

    // Make result items expandable
    this.$organisationListItems.on('click', '.org-summary', function(evt) {
      evt.preventDefault();
      self.$organisationListItems.find('.org-summary').attr('aria-expanded', false);
      $(this).attr('aria-expanded', true);
      self._handleItemHighlight(evt, $(this).closest('li'));
    });

    // Handle pagination
    this.$resultsPagination.on('click', 'a', function(evt) {
      evt.preventDefault();

      if(window.LABELS && window.LABELS.loading) {
        $(evt.target).replaceWith('<span>' + window.LABELS.loading + '</span>');
      }

      self._fetchPage(evt.target.href);

      if(window.history && history.pushState) {
        history.pushState(null, null, evt.target.href);
      }
    });

    // Handle form submission
    this.$findLegalAdviserForm.submit(function(evt) {
      evt.preventDefault();

      var formData = $(this).serializeArray();
      if(!formData.length) {
        return;
      }
      formData = reject(formData, 'value', '');
      var url = document.location.pathname + '?' + $.param(formData);
      self._fetchPage(url, true);

      // Update browser history
      if(window.history && history.pushState) {
        history.pushState(null, null, url);
      }

      $(this).find('#searchButton')
        .text(window.LABELS.loading)
        .attr('disabled', true);
    });

    // Handle URLs
    window.onpopstate = function() {
      self._fetchPage(document.location.href);
    };

    // Trigger search when checkboxes are changed
    $('.legal-adviser-search [type="checkbox"], select').on('change', function() {
      if (!self.$resultsMap.length) {
        return;
      }
      self.$findLegalAdviserForm.trigger('submit');
    });

    this.eventsBound = true;
  },

  _unbindEvents: function() {
    this.$organisationListItems
      .unbind('click')
      .find('.org-summary')
      .each(function() {
        $(this).replaceWith('<header class="' + this.className + '">' + $(this).html() + '</header>');
      });

    this.$resultsPagination.unbind('click');
    this.$findLegalAdviserForm.unbind('submit');
    window.onpopstate = null;

    this.eventsBound = false;
  },

  _fetchPage: function(url, scrollToResults) {
    var self = this;

    $.get(url)
      .success(function(data) {
        self.$findLegalAdviserContainer.replaceWith(data);
        self.markers = [];
        self.eventsBound = false;
        self.init();

        if(scrollToResults) {
          $('html, body').delay(300).animate({
            'scrollTop': self.$findLegalAdviserContainer.offset().top + 1
          }, 160);
        }

        $('.search-results-list').attr('tabindex', -1).focus();
      })
      .error();
  },

  _closeOpenInfoWindow: function() {
    if(this.openInfoWindow) {
      this.openInfoWindow.close();
    }
  },

  _prepareMarkers: function() {
    var organisations = $.map(this.$organisationListItems, function(item) {
      var $item = $(item);
      return {
        id: $item.data('id'),
        position: {
          lat: parseFloat($item.data('lat')),
          lng: parseFloat($item.data('lon'))
        },
        title: $item.find('.fn').text(),
        content: $item.html()
      };
    });

    this.addMarkers(organisations);
  },

  _fitAllMarkers: function() {
    var self = this;

    this.map.fitBounds(reduce(this.markers, function(bounds, marker) {
      return bounds.extend(marker.getPosition());
    }, new window.google.maps.LatLngBounds()));

    $.each(this.markers, function() {
      this.setMap(self.map);
    });
  },

  _handleHighlightedItemScroll: function($item, $container) {
    var itemHeight = $item.outerHeight();
    var containerHeight = $container.height();

    if(itemHeight + $item.position().top > containerHeight) {
      $container.scrollTop(containerHeight - itemHeight);
    }
  },

  _handleMarkersZooming: function(selectedMarkerId) {
    var markerOnMap = find(this.markers, { id: selectedMarkerId });

    $.each(this.markers, function() {
      this.setMap(null);
    });

    markerOnMap.setMap(this.map);

    var pairBounds = new window.google.maps.LatLngBounds();
    pairBounds.extend(markerOnMap.position);
    if(this.searchLocationMarker) {
      pairBounds.extend(this.searchLocationMarker.position);
    }

    this.map.fitBounds(pairBounds);

    if(!this.searchLocationMarker) {
      this.map.setZoom(this.map.getZoom() - 4);
    }
  },

  _handleItemHighlight: function(evt, $item) {
    var $container = $item.closest('.search-results-list');

    if($item.hasClass('s-highlighted')) {
      this._fitAllMarkers();
      return;
    }

    this.$organisationListItems.removeClass('s-highlighted');
    $item.addClass('s-highlighted');

    $item.find('.org-details').attr('tabindex', -1).focus();

    this._handleMarkersZooming($item.data('id'));
    this._handleHighlightedItemScroll($item, $container);
  },

  renderMap: function(lat, lng) {
    var self = this;

    var searchLocation = {
      lat: lat || 51.5,
      lng: lng || -0.2
    };

    var mapOptions = {
      center: searchLocation,
      zoom: 12,
      scrollwheel: false,
      panControl: false,
      streetViewControl: false
    };

    this.map = new window.google.maps.Map(this.$resultsMap[0], mapOptions);

    if(lat && lng) {
      this.searchLocationMarker = this.addMarker(searchLocation, {
        title: 'Search location',
        icon: 'icon-location-2x'
      });
    }
    window.google.maps.event.addListener(self.map, 'click', function() {
      self._closeOpenInfoWindow();
    });
  },

  addMarker: function(position, options) {
    var self = this;
    var image;
    options = options || {};

    if(options.icon) {
      image = {
        url: '/static/images/icons/' + options.icon + '.png',
        scaledSize: new window.google.maps.Size(16, 16),
        anchor: new window.google.maps.Point(8, 8)
      };
    } else if(options.id) {
      image = {
        url: '/static/images/icons/icon-numbered-markers-2x.png',
        size: new window.google.maps.Size(22, 40),
        scaledSize: new window.google.maps.Size(220, 40),
        origin: new window.google.maps.Point(22 * (options.id - 1), 0)
      };
    }

    var marker = new window.google.maps.Marker({
      position: position,
      id: options.id,
      title: options.title,
      map: this.map,
      icon: image
    });

    if(options.content) {
      window.google.maps.event.addListener(marker, 'click', function() {
        self._closeOpenInfoWindow();
        self.openInfoWindow = new window.google.maps.InfoWindow({
          content: options.content
        });
        self.openInfoWindow.open(self.map, marker);
      });
    }

    return marker;
  },

  addMarkers: function(points) {
    var self = this;

    $.each(points, function() {
      if(!(this.position)) {
        return;
      }
      self.markers.push(
        self.addMarker(this.position, {
          id: this.id,
          title: this.title,
          content: this.content
        })
      );
    });

    this._fitAllMarkers();
  },

  cacheEls: function() {
    this.$resultsMap = $(this.el);
    this.$findLegalAdviserContainer = $('.find-legal-adviser');
    this.$findLegalAdviserForm = $('.legal-adviser-search form');
    this.$organisationListItems = $('.search-results-list .vcard');
    this.$resultsPagination = $('.search-results-pagination');
  }
};
