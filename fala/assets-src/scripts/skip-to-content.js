var $ = require('jquery');

Mojular.Modules.SkipToContent = {
  init: function() {
    $('body').on('click', '.skip-link', function(e) {
      e.preventDefault();

      $($(e.target).attr('href'))
        .attr('tabindex', -1)
        .focus()
        .blur(function() {
          $(this).removeAttr('tabindex');
        });
    });
  }
};
