buffer			= require('buffer').Buffer
child_process	= require('child_process')
colors			= require('colors')
events			= require('events')
fs				= require('fs')
http			= require('http')
json			= require('JSON2').stringify
json2			= require('JSON2')
qs				= require('querystring')
url				= require('url')
util			= require('util')
zlib			= require('zlib')
views			= require('./views')

options={}
status=
	login_errors:0
	total_requests:0
	reconnects:0
	connected:false

_log=(text)->
	process.send({event:'log', server:"#{options.region}:#{options.username}", text:text})


class RequestHandler
	constructor:(@views, local_client)->
		@client=local_client
		@connections=0
		@current=0
		@queue=[]
	request:(request, response)=>
		path=url.parse(request.url)
		if path.pathname in Object.keys(@views)
			status.total_requests+=1
			if @connections==0
				@connections+=1
				view=new @views[path.pathname](path.query, @client, @respond, request, response)
				view.go()
				view=null
			else
				@queue.push({path:path, request:request, response:response})
		else if path.pathname=='/status/'
			response.writeHead(200)
			response.write(json({connected:status.connected, connections:h.connections, total_requests:status.total_requests, reconnects:status.reconnects}))
			response.end()
		else
			_log("#{path.pathname}".cyan+" >> Status:"+"404".red)
			response.writeHead(404)
			response.write('404')
			response.end()
		return @queue.length
	next:()=>
		if @current==0
			@current=@queue.shift()
		else
			console.log('###########')
			console.log(@current)
			console.log('###########')
			console.log(@)
			console.log('###########')
		@connections+=1
		view=new @views[@current.path.pathname](@current.path.query, @client, @respond, @current.request, @current.response)
		view.go()
		view=null
	respond:(data, request, response)=>
		if not data.html?
			body=json(data.body)
			mimetype='application/json'
		else
			body=data.body
			mimetype='text/html'
		obj={
			'status'	:data.status
			'body'		:body
			'headers'	:{
				'Content-Type'		: '#{mimetype}; charset=UTF-8'
			}
			'path'		:url.parse(request.url).pathname
		}
		if request.headers['accept-encoding'].toLowerCase().indexOf('gzip')!=-1
			obj['headers']['Content-Encoding']='gzip'
			zlib.gzip(obj['body'], (e,r)=>
				@send(response, obj, {'body':r})
			)
		else
			@send(response, obj)
	send:(response, data, args)=>
		if args?
			for k,v of args
				data[k]=v
		content_length=new buffer(data['body']).length
		data['headers']['Content-Length']=content_length
		response.writeHead(data.status, data.headers)
		response.write(data.body)
		response.end()
		@connections-=1
		@current=0
		if @queue.length>0
			@next()
		_log("#{data.path}".cyan+" >> Status:"+"#{data.status}".green+" >> Length:"+"#{content_length}".magenta)

_log("Preparing to connect".grey)


client={}
initial=1
h={}
start_client=->
	client=child_process.fork('client.js')
	client.on('message', (msg)->
		#console.log(msg)
		if msg.event=='connected' and initial==1
			initial=0
			_log("Connected".green)
			status.login_errors=0
			status.connected=true
			h=new RequestHandler(views, client)
			server=http.createServer(h.request)
			server.listen(options.listen_port||8081)
		else if msg.event=='connected' and initial==0
			_log('Reconnected'.green)
			status.login_errors=0
			status.connected=true
			h.client=client
			h.connections=0
		else if msg.event=='throttled'
			_log("THROTTLED".red)
		else if msg.event=='timeout'
			_log("TIMEOUT".red)
		else if msg.event=='log'
			_log(msg.text)
	).on('exit', (code, signal)->
		status.connected=false
		if code in [3, 5]
			console.log(code, signal)
			console.log(h.current)
			console.log(h.queue)
			console.log(h.connections)
			setTimeout(client_restart, 2000)
		if code==4
			get_time=()=>
				if status.login_errors*500+1000<=10000
					_log("restarting client in #{status.login_errors*500+1000}ms")
					status.login_errors*500+1000
				else
					_log('restarting client in 10000ms')
					10000
			status.login_errors+=1
			setTimeout(client_restart, get_time())
		else
			console.log(code, signal)
	)
	client.send({event:'connect', options:options})
client_restart=->
	client.removeAllListeners()
	start_client()
	status.reconnects+=1

process.on('message', (msg)->
	if msg.event=='connect'
		options=msg.options
		start_client()
	else if msg.event=='status'
		process.send({event:'status', data:{connected:status.connected, connections:h.connections, total_requests:status.total_requests, reconnects:status.reconnects}, server:"#{options.region}:#{options.username}"})
)
