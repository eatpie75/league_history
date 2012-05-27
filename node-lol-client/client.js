// Generated by CoffeeScript 1.3.3
(function() {
  var client, colors, json, json2, lol_client, models, nopt, options, _log;

  colors = require('colors');

  json = require('JSON2').stringify;

  json2 = require('JSON2');

  lol_client = require('./lol-client');

  models = require('./lib/models');

  nopt = require('nopt');

  _log = function(text) {
    return process.send({
      event: 'log',
      server: "" + options.region + ":" + options.username,
      text: text
    });
  };

  options = {};

  client = {};

  process.on('message', function(msg) {
    var model, query,
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
        return process.send({
          event: 'connected'
        });
      }).on('throttled', function() {
        process.send({
          event: 'throttled'
        });
        return process.exit(3);
      });
      return client.connect();
    } else if (msg.event === 'get') {
      query = msg.query;
      model = new models.get[msg.model]({
        client: client
      });
      model.on('finished', function(data, extra) {
        if (extra == null) {
          extra = {};
        }
        extra.region = options.region;
        return process.send({
          event: "" + msg.uuid + "__finished",
          data: data,
          extra: extra
        });
      });
      return model.get(query);
    } else if (msg.event === 'keepalive') {
      return client.keepAlive(function(err, result) {
        return _log("Heartbeat".magenta);
      });
    }
  });

}).call(this);
