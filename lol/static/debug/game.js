// Generated by CoffeeScript 1.6.3
(function() {
  var TellMeMore,
    __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  TellMeMore = (function() {
    function TellMeMore() {
      this.game = window.game_pk;
      this.cache = {};
      this.bind();
    }

    TellMeMore.prototype.bind = function() {
      var _this_;
      _this_ = this;
      return $('.player_expand').click(function(e) {
        return _this_.expand($(this));
      });
    };

    TellMeMore.prototype.bind_toggle = function(el, extra, expand) {
      var _this_;
      if (expand == null) {
        expand = 1;
      }
      _this_ = this;
      el.unbind();
      return $(el).click(function(e) {
        if (expand) {
          return _this_.expand($(this));
        } else {
          return _this_.collapse($(this), extra);
        }
      });
    };

    TellMeMore.prototype.info_template = function(args) {
      var key, result, stat;
      result = "<td colspan=10>";
      for (key in args) {
        stat = args[key];
        result += "			<div class='col-md-3'>				<b>" + (key.toUpperCase().replace('_', ' ', 'mg')) + "</b><br>				" + stat + "			</div>";
      }
      result += "</td>";
      return result;
    };

    TellMeMore.prototype.get_info = function(player) {
      var _ref,
        _this = this;
      if (_ref = "" + player, __indexOf.call(Object.keys(this.cache), _ref) < 0) {
        $.ajax({
          type: 'GET',
          async: false,
          url: "" + window.AJAX_BASE + "ajax/player_info/" + player + "/",
          dataType: "json",
          success: function(msg) {
            return _this.cache[player] = msg;
          }
        });
      }
      return this.cache[player];
    };

    TellMeMore.prototype.expand = function(el) {
      var extra, info, player,
        _this = this;
      player = el.data('player');
      info = this.get_info(player);
      extra = $("<tr class='drop-stats'></tr>").insertAfter(el.closest('tr'));
      extra.css('height');
      extra.css('height', '100px');
      setTimeout(function() {
        return extra.html(_this.info_template(info));
      }, 210);
      return this.bind_toggle(el, extra, 0);
    };

    TellMeMore.prototype.collapse = function(el, extra) {
      var _this = this;
      extra.html('');
      extra.css('height', '0px');
      setTimeout(function() {
        return extra.remove();
      }, 500);
      return this.bind_toggle(el);
    };

    return TellMeMore;

  })();

  $(document).ready(function() {
    return window.tell_me_more = new TellMeMore();
  });

}).call(this);
