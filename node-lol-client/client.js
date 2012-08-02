// Generated by CoffeeScript 1.3.3
(function() {
  var client, colors, keepalive, lol_client, models, options, _keepalive, _log;

  colors = require('colors');

  lol_client = require('./lol-client');

  models = require('./lib/models');

  _log = function(text) {
    return process.send({
      event: 'log',
      text: text
    });
  };

  _keepalive = function() {
    var timer,
      _this = this;
    timer = setTimeout(function() {
      client.emit('timeout');
      return console.log('wtf keepalive timeout');
    }, 10000);
    return client.keepAlive(function(err, result) {
      clearTimeout(timer);
      if (Math.random() >= 0.75) {
        return _log("Heartbeat".magenta);
      }
    });
  };

  options = {};

  client = {};

  keepalive = {};

  process.on('message', function(msg) {
    var model, query, query_options,
      _this = this;
    if (msg.event === 'connect') {
      options = {
        region: msg.options.region || 'na',
        username: msg.options.username || 'dotaesnumerouno',
        password: msg.options.password || 'penis2',
        version: msg.options.version || '1.60.12_05_22_19_12'
      };
      client = new lol_client(options);
      client.on('connection', function() {
        process.send({
          event: 'connected'
        });
        return keepalive = setInterval(function() {
          return _keepalive();
        }, 120000);
      }).on('throttled', function() {
        process.send({
          event: 'throttled'
        });
        return process.exit(3);
      }).on('timeout', function() {
        process.send({
          event: 'timeout'
        });
        return process.exit(5);
      });
      return client.connect();
    } else if (msg.event === 'get') {
      query = msg.query;
      query_options = {
        client: client
      };
      if (msg.extra != null) {
        query_options['extra'] = msg.extra;
      }
      model = new models.get[msg.model](function(data, extra) {
        if (extra == null) {
          extra = {};
        }
        extra.region = options.region;
        return process.send({
          event: "" + msg.uuid + "__finished",
          data: data,
          extra: extra
        });
      }, query_options);
      return model.get(query);
    }
  });

}).call(this);
