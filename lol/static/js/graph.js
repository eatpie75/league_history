// Generated by CoffeeScript 1.4.0
(function() {
  var draw_chart;

  draw_chart = function(data, y, aoptions, data_parse, container) {
    var date, day, defaults, now, options, parsed, _i, _j, _k, _len, _len1, _len2;
    if (y == null) {
      y = 'rating';
    }
    if (aoptions == null) {
      aoptions = {};
    }
    if (data_parse == null) {
      data_parse = 'default';
    }
    if (container == null) {
      container = 'elo-graph';
    }
    defaults = {
      element: container,
      xkey: 'x',
      ykeys: 'y',
      labels: ['ELO'],
      ymax: 'auto',
      ymin: 'auto',
      hideHover: true,
      lineColors: ['#3269b4', '#C0D800', '#CB4B4B', '#4DA74D', '#9440ED']
    };
    options = $.extend({}, defaults);
    $.extend(true, options, aoptions);
    parsed = [];
    if (data_parse === 'default') {
      for (_i = 0, _len = data.length; _i < _len; _i++) {
        day = data[_i];
        if (day[1][y] < 10) {
          continue;
        }
        parsed.push({
          'x': day[0],
          'y': day[1][y]
        });
      }
    } else if (data_parse === 'chistorywr') {
      for (_j = 0, _len1 = data.length; _j < _len1; _j++) {
        day = data[_j];
        date = new Date(day[0]);
        now = new Date();
        if (day[1]['champions'][y]['count'] < 10) {
          continue;
        }
        parsed.push({
          'x': day[0],
          'y': Math.round((day[1]['champions'][y]['won'] / day[1]['champions'][y]['count']) * 100)
        });
      }
    } else if (data_parse === 'chistorypop') {
      for (_k = 0, _len2 = data.length; _k < _len2; _k++) {
        day = data[_k];
        if (day[1]['champions'][y]['count'] < 10) {
          continue;
        }
        parsed.push({
          'x': day[0],
          'y': (day[1]['champions'][y]['won'] / day[1]['count']) * 100
        });
      }
    }
    options['data'] = parsed;
    return Morris.Line(options);
  };

  $(document).ready(function() {
    window.draw_chart = draw_chart;
    if (window.chart != null) {
      return draw_chart(window.data, window.bgchart);
    }
  });

}).call(this);
