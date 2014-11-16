// Generated by CoffeeScript 1.8.0
(function() {
  $(document).ready(function() {
    window.connect_items = function() {
      return $('div.item.sprite,img.item.sprite').each(function() {
        var el, item;
        el = $(this);
        item = el.data('item').slice(1);
        if (item in window.items) {
          item = window.items[item];
          return el.popover({
            'html': true,
            'content': item.description,
            'title': item.name,
            'placement': 'auto top',
            'trigger': 'hover',
            'animation': false
          });
        }
      });
    };
    return window.connect_items();
  });

}).call(this);
