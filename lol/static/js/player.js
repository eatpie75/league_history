// Generated by CoffeeScript 1.4.0
(function() {
  var ChampionSort, PlayerGamePageHandler, StatFilter, draw_bgchart, force_update, querystring;

  PlayerGamePageHandler = (function() {

    function PlayerGamePageHandler() {
      this.page = 1;
      this.account_id = window.account_id;
      this.region = window.region;
      this._bind();
      this.qs = querystring(window.location.hash.slice(1));
      if ('page' in this.qs) {
        this.change_page(qs.page);
      }
    }

    PlayerGamePageHandler.prototype._bind = function() {
      var _this_;
      _this_ = this;
      $('.page_link').bind('click', function(e) {
        return _this_.change_page($(this));
      });
      return window.connect_items();
    };

    PlayerGamePageHandler.prototype.change_page = function(el) {
      var page,
        _this = this;
      if (el == null) {
        el = 1;
      }
      if (typeof el === 'object') {
        page = el.data('page');
      } else {
        page = el;
      }
      return $.ajax({
        type: 'GET',
        url: "" + window.AJAX_BASE + "ajax/summoner_games/" + this.region + "/" + this.account_id + "/?page=" + page,
        dataType: "html",
        success: function(msg) {
          $('#games').html(msg);
          _this._bind();
          return _this.page = page;
        }
      });
    };

    return PlayerGamePageHandler;

  })();

  ChampionSort = (function() {

    function ChampionSort() {
      var qs;
      this.column = $('.table-sort.active:first');
      this.column_str = this.column.data('column');
      this.direction = 1;
      this.icon = this.column.children('span').children('i');
      this._icons = {
        '-1': 'icon-arrow-up',
        '1': 'icon-arrow-down'
      };
      this._bind();
      qs = querystring(window.location.hash.slice(1));
      if ('sort' in qs) {
        if ('direction' in qs) {
          this.direction = Number(qs.direction);
        }
        this.change($('.table-sort').filter(function(e) {
          return $(this).data('column') === qs['sort'];
        }).first(), true);
      }
    }

    ChampionSort.prototype._bind = function() {
      var _this_;
      _this_ = this;
      return $('.table-sort').bind('click', function(e) {
        return _this_.change($(this));
      });
    };

    ChampionSort.prototype.change = function(el, init) {
      var qs;
      if (init == null) {
        init = false;
      }
      if (init) {
        this.icon.removeClass(this._icons["" + 1]);
      }
      if (this.column_str === el.data('column')) {
        this.icon.removeClass(this._icons["" + this.direction]).addClass(this._icons["" + (this.direction * -1)]);
        this.direction *= -1;
      } else {
        this.column.removeClass('active');
        this.icon.removeClass(this._icons["" + this.direction]);
        if (init === false) {
          this.direction = 1;
        }
        this.column = el;
        this.column_str = this.column.data('column');
        this.icon = this.column.children('span').children('i');
        this.column.addClass('active');
        this.icon.addClass(this._icons["" + this.direction]);
      }
      this.sort(el.data('column'), el.data('spec-order'));
      qs = querystring(window.location.hash.slice(1));
      qs['sort'] = el.data('column');
      if (this.direction === -1) {
        qs['direction'] = this.direction;
      } else {
        delete qs.direction;
      }
      return window.location.hash = $.param(qs);
    };

    ChampionSort.prototype.sort = function(column, spec_order) {
      var pregex, _base, _sort,
        _this = this;
      if (spec_order == null) {
        spec_order = null;
      }
      pregex = new RegExp('(\\d+)%', 'i');
      _base = function(value_1, value_2, total_1, total_2) {
        if (value_1 > value_2) {
          return -1 * _this.direction;
        } else if (value_1 === value_2) {
          if (total_1 > total_2) {
            return -1 * _this.direction;
          } else {
            return 1 * _this.direction;
          }
        } else {
          return 1 * _this.direction;
        }
      };
      _sort = function(a, b) {
        var lower_min, minimum, total_1, total_2, value_1, value_2, _ref, _ref1, _ref2, _ref3;
        _ref = [$(a), $(b)], a = _ref[0], b = _ref[1];
        value_1 = a.children("." + column).text();
        value_2 = b.children("." + column).text();
        if ((spec_order != null) && spec_order === 'swin') {
          _ref1 = [Number(value_1.match(pregex)[1]), Number(value_2.match(pregex)[1])], value_1 = _ref1[0], value_2 = _ref1[1];
          minimum = Math.round(window.num_games * 0.04);
          lower_min = Math.round(window.num_games * 0.01);
          total_1 = Number(a.children(".total").text());
          total_2 = Number(b.children(".total").text());
          if (total_1 >= minimum) {
            if (total_2 >= minimum) {
              return _base(value_1, value_2, total_1, total_2);
            } else {
              return -1 * _this.direction;
            }
          } else {
            if (total_2 >= minimum) {
              return 1 * _this.direction;
            } else {
              if (total_1 >= lower_min) {
                if (total_2 >= lower_min) {
                  return _base(value_1, value_2, total_1, total_2);
                } else {
                  return -1 * _this.direction;
                }
              } else {
                return _base(value_1, value_2, total_1, total_2);
              }
            }
          }
        } else if (!isNaN(Number(value_1)) && !isNaN(Number(value_2))) {
          _ref2 = [Number(value_1), Number(value_2)], value_1 = _ref2[0], value_2 = _ref2[1];
          if (value_1 > value_2) {
            return -1 * _this.direction;
          } else if (value_1 === value_2) {
            return 0;
          } else {
            return 1 * _this.direction;
          }
        } else if (pregex.test(value_1) && pregex.test(value_2)) {
          _ref3 = [Number(value_1.match(pregex)[1]), Number(value_2.match(pregex)[1])], value_1 = _ref3[0], value_2 = _ref3[1];
          if (value_1 > value_2) {
            return -1 * _this.direction;
          } else if (value_1 === value_2) {
            return 0;
          } else {
            return 1 * _this.direction;
          }
        } else {
          if (value_1 > value_2) {
            return 1 * _this.direction;
          } else if (value_1 === value_2) {
            return 0;
          } else {
            return -1 * _this.direction;
          }
        }
      };
      $('.cbody').append($('.cbody .sort').sort(_sort));
      return this.current_column = column;
    };

    return ChampionSort;

  })();

  StatFilter = (function() {

    function StatFilter() {
      this._bind();
    }

    StatFilter.prototype._bind = function() {
      var _this_;
      _this_ = this;
      return $('#stat-filter').bind('change', function() {
        var el, params;
        el = $(this);
        params = {};
        if (el.children('#id_game_map').val() !== '-1') {
          params.game_map = el.children('#id_game_map').val();
        }
        if (el.children('#id_game_mode').val() !== '-1') {
          params.game_mode = el.children('#id_game_mode').val();
        }
        return window.location.search = $.param(params);
      });
    };

    return StatFilter;

  })();

  querystring = function(oqs) {
    var obj, option, qs, _i, _len;
    oqs = oqs.split('&');
    qs = {};
    for (_i = 0, _len = oqs.length; _i < _len; _i++) {
      option = oqs[_i];
      obj = option.split('=');
      if (obj[0] === '' && obj.length === 1) {
        break;
      }
      qs[decodeURI(obj[0])] = decodeURI(obj[1]);
    }
    return qs;
  };

  force_update = function(e) {
    var _update_status,
      _this = this;
    _update_status = function() {
      var _this = this;
      return $.ajax({
        type: 'GET',
        url: "" + window.AJAX_BASE + "ajax/force_update_status/" + window.region + "/" + window.account_id + "/",
        dataType: "json",
        success: function(msg) {
          if (msg.status === 'QUEUE') {
            return setTimeout(_update_status, msg.delay);
          } else if (msg.status === 'DONE') {
            return $('#last-updated').text(msg.msg);
          }
        }
      });
    };
    $('#last-updated-block').html("<small id='last-updated'>WORKING...</small>");
    return $.ajax({
      type: 'GET',
      url: "" + window.AJAX_BASE + "ajax/force_update/" + window.region + "/" + window.account_id + "/",
      dataType: "json",
      success: function(msg) {
        $('#last-updated').text("LAST UPDATED:" + msg.msg);
        if (msg.status === 'QUEUE') {
          return setTimeout(_update_status, msg.delay);
        }
      }
    });
  };

  draw_bgchart = function(data, y, aoptions, data_parse) {
    var container, date, day, defaults, now, options, parsed, _i, _j, _k, _len, _len1, _len2;
    if (y == null) {
      y = 'rating';
    }
    if (aoptions == null) {
      aoptions = {};
    }
    if (data_parse == null) {
      data_parse = 'default';
    }
    container = document.getElementById("elo-graph");
    defaults = {
      colors: ['#3269b4', '#C0D800', '#CB4B4B', '#4DA74D', '#9440ED'],
      subtitle: 'ELO GRAPH',
      shadowSize: 0,
      xaxis: {
        mode: 'time',
        noTicks: 10
      },
      yaxis: {
        autoscale: true,
        autoscaleMargin: 1
      },
      mouse: {
        track: true,
        trackFormatter: function(obj) {
          return "" + (Flotr.Date.format(obj.x, '%y-%m-%d')) + ": " + (Math.round(obj.y));
        },
        sensiblility: 3,
        lineColor: '#fff',
        relative: true
      },
      lines: {
        fill: true,
        show: true
      },
      points: {
        show: true,
        lineWidth: 1,
        radius: 2,
        fillColor: '#9D261D'
      },
      grid: {
        color: '#000',
        verticalLines: false,
        outline: ''
      }
    };
    options = $.extend({}, defaults);
    $.extend(true, options, aoptions);
    if (data_parse === 'default') {
      parsed = [];
      for (_i = 0, _len = data.length; _i < _len; _i++) {
        day = data[_i];
        if (day[1][y] < 10) {
          continue;
        }
        parsed.push([new Date(day[0]), day[1][y]]);
      }
    } else if (data_parse === 'chistorywr') {
      parsed = [];
      for (_j = 0, _len1 = data.length; _j < _len1; _j++) {
        day = data[_j];
        date = new Date(day[0]);
        now = new Date();
        if (day[1]['champions'][y]['count'] < 10) {
          continue;
        }
        parsed.push([date, (day[1]['champions'][y]['won'] / day[1]['champions'][y]['count']) * 100]);
      }
    } else if (data_parse === 'chistorypop') {
      parsed = [];
      for (_k = 0, _len2 = data.length; _k < _len2; _k++) {
        day = data[_k];
        if (day[1]['champions'][y]['count'] < 10) {
          continue;
        }
        parsed.push([new Date(day[0]), (day[1]['champions'][y]['won'] / day[1]['count']) * 100]);
      }
    }
    return Flotr.draw(container, [parsed], options);
  };

  $(document).ready(function() {
    if ($('.page_link').length > 0) {
      window.page_handler = new PlayerGamePageHandler();
    }
    if ($('.table-sort.active:first').length > 0) {
      window.champion_sort = new ChampionSort();
    }
    if ($('#stat-filter').length > 0) {
      window.stat_filter = new StatFilter();
    }
    window.draw_chart = draw_bgchart;
    $('#force-update').bind('click', force_update);
    if (window.bgchart != null) {
      draw_bgchart(window.data, window.bgchart);
    }
    return $('a[data-toggle="tab"]').click(function(e) {
      e.preventDefault();
      return $(this).tab('show');
    });
  });

}).call(this);
