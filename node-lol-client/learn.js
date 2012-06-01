// Generated by CoffeeScript 1.3.3
(function() {
  var RequestHandler, buffer, child_process, client, client_restart, colors, ev, events, fs, h, heartbeat_interval, http, initial, json, json2, nopt, options, qs, start_client, status, url, util, views, zlib, _log,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

  buffer = require('buffer').Buffer;

  child_process = require('child_process');

  colors = require('colors');

  events = require('events');

  fs = require('fs');

  http = require('http');

  json = require('JSON2').stringify;

  json2 = require('JSON2');

  nopt = require('nopt');

  qs = require('querystring');

  url = require('url');

  util = require('util');

  zlib = require('zlib');

  views = require('./views');

  ev = new events.EventEmitter();

  options = {};

  status = {
    total_requests: 0,
    reconnects: 0
  };

  _log = function(text) {
    return process.send({
      event: 'log',
      server: "" + options.region + ":" + options.username,
      text: text
    });
  };

  RequestHandler = (function() {

    function RequestHandler(views, local_client) {
      this.send = __bind(this.send, this);

      this.respond = __bind(this.respond, this);

      this.next = __bind(this.next, this);

      this.request = __bind(this.request, this);
      this.views = views;
      this.client = local_client;
      this.connections = 0;
      this.current = 0;
      this.queue = [];
      ev.on('finished', this.respond).on('send', this.send);
    }

    RequestHandler.prototype.request = function(request, response) {
      var path, view, _ref;
      path = url.parse(request.url);
      if (_ref = path.pathname, __indexOf.call(Object.keys(this.views), _ref) >= 0) {
        status.total_requests += 1;
        if (this.connections === 0) {
          this.connections += 1;
          view = new this.views[path.pathname](path.query, this.client, ev, request, response);
          view.go();
          view = null;
        } else {
          this.queue.push({
            path: path,
            request: request,
            response: response
          });
        }
      } else if (path.pathname === '/status/') {
        response.writeHead(200);
        response.write(json({
          views: this.views,
          connections: this.connections,
          current: this.current,
          queue: this.queue,
          total_requests: total_requests
        }));
        response.end();
      } else {
        _log(("" + path.pathname).cyan + " >> Status:" + "404".red);
        response.writeHead(404);
        response.write('404');
        response.end();
      }
      return false;
    };

    RequestHandler.prototype.next = function() {
      var view;
      if (this.current === 0) {
        this.current = this.queue.shift();
      } else {
        console.log('###########');
        console.log(this.current);
        console.log('###########');
        console.log(this);
        console.log('###########');
      }
      this.connections += 1;
      view = new this.views[this.current.path.pathname](this.current.path.query, this.client, ev, this.current.request, this.current.response);
      view.go();
      return view = null;
    };

    RequestHandler.prototype.respond = function(data, request, response) {
      var body, obj;
      body = json(data.body);
      obj = {
        'status': data.status,
        'body': body,
        'headers': {
          'Content-Type': 'application/json; charset=UTF-8'
        },
        'path': url.parse(request.url).pathname
      };
      if (request.headers['accept-encoding'].toLowerCase().indexOf('gzip') !== -1) {
        obj['headers']['Content-Encoding'] = 'gzip';
        return zlib.gzip(obj['body'], function(e, r) {
          return ev.emit('send', response, obj, {
            'body': r
          });
        });
      } else {
        return ev.emit('send', response, obj);
      }
    };

    RequestHandler.prototype.send = function(response, data, args) {
      var content_length, k, v;
      if (args != null) {
        for (k in args) {
          v = args[k];
          data[k] = v;
        }
      }
      content_length = new buffer(data['body']).length;
      data['headers']['Content-Length'] = content_length;
      response.writeHead(data.status, data.headers);
      response.write(data.body);
      response.end();
      this.connections -= 1;
      this.current = 0;
      if (this.queue.length > 0) {
        this.next();
      }
      return _log(("" + data.path).cyan + " >> Status:" + ("" + data.status).green + " >> Length:" + ("" + content_length).magenta);
    };

    return RequestHandler;

  })();

  _log("Preparing to connect".grey);

  client = {};

  heartbeat_interval = 0;

  initial = 1;

  h = {};

  start_client = function() {
    client = child_process.fork('client.js');
    client.on('message', function(msg) {
      var server;
      if (msg.event === 'connected' && initial === 1) {
        initial = 0;
        _log("Connected".green);
        h = new RequestHandler(views, client);
        server = http.createServer(h.request);
        server.listen(options.listen_port || 8081);
        return heartbeat_interval = setInterval(function() {
          return client.send({
            event: 'keepalive'
          });
        }, 600000);
      } else if (msg.event === 'connected' && initial === 0) {
        _log('Reconnected'.green);
        h.client = client;
        return h.connections = 0;
      } else if (msg.event === 'throttled') {
        return _log("THROTTLED".red);
      } else if (msg.event === 'log') {
        return _log(msg.text);
      }
    }).on('exit', function(code, signal) {
      clearInterval(heartbeat_interval);
      if (code === 3 || code === 5) {
        console.log(code, signal);
        console.log(h.current);
        console.log(h.queue);
        console.log(h.connections);
        return setTimeout(client_restart, 2000);
      } else {
        return console.log(code, signal);
      }
    });
    return client.send({
      event: 'connect',
      options: options
    });
  };

  client_restart = function() {
    client.removeAllListeners();
    start_client();
    return status.reconnects += 1;
  };

  process.on('message', function(msg) {
    if (msg.event === 'connect') {
      options = msg.options;
      return start_client();
    } else if (msg.event === 'status') {
      return process.send({
        event: 'status',
        data: {
          connections: h.connections,
          total_requests: status.total_requests,
          reconnects: status.reconnects
        },
        server: "" + options.region + ":" + options.username
      });
    }
  });

}).call(this);
