buffer			= require('buffer').Buffer
child_process	= require('child_process')
colors			= require('colors')
events			= require('events')
fs				= require('fs')
http			= require('http')
json			= require('JSON2').stringify
json2			= require('JSON2')
nopt			= require('nopt')
qs				= require('querystring')
url				= require('url')
util			= require('util')
zlib			= require('zlib')
views			= require('./views')

ev=new events.EventEmitter()
options={}
status=
	total_requests:0
	reconnects:0

_log=(text)->
		process.send({event:'log', server:"#{options.region}:#{options.username}", text:text})
# _log=(text)->
# 	d=new Date()
# 	time="#{d.getFullYear()}/#{d.getMonth()+1}/#{d.getDate()} #{d.getHours()}:#{if d.getMinutes()< 10 then '0'+d.getMinutes() else d.getMinutes()}:#{if d.getSeconds()< 10 then '0'+d.getSeconds() else d.getSeconds()}".white
# 	time=(time+'                             ').slice(0,29)
# 	console.log(time+" | "+text)

class RequestHandler
	constructor:(views, local_client)->
		@views=views
		@client=local_client
		@connections=0
		@current=0
		@queue=[]
		ev.on('finished', @respond).on('send', @send)
	request:(request, response)=>
		path=url.parse(request.url)
		if path.pathname in Object.keys(@views)
			status.total_requests+=1
			if @connections==0
				@connections+=1
				view=new @views[path.pathname](path.query, @client, ev, request, response)
				view.go()
				view=null
			else
				@queue.push({path:path, request:request, response:response})
		else if path.pathname=='/status/'
			# console.log(@)
			response.writeHead(200)
			response.write(json({views:@views, connections:@connections, current:@current, queue:@queue, total_requests:total_requests}))
			response.end()
		else
			_log("#{path.pathname}".cyan+" >> Status:"+"404".red)
			response.writeHead(404)
			response.write('404')
			response.end()
		return false
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
		view=new @views[@current.path.pathname](@current.path.query, @client, ev, @current.request, @current.response)
		view.go()
		view=null
	respond:(data, request, response)=>
			body=json(data.body)
			obj={
				'status'	:data.status
				'body'		:body
				'headers'	:{
					'Content-Type'		: 'application/json; charset=UTF-8'
				}
				'path'		:url.parse(request.url).pathname
			}
			if request.headers['accept-encoding'].toLowerCase().indexOf('gzip')!=-1
				obj['headers']['Content-Encoding']='gzip'
				zlib.gzip(obj['body'], (e,r)->
					ev.emit('send', response, obj, {'body':r})
				)
			else
				ev.emit('send', response, obj)
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

# options=
# 	region: 'euw' # Lol Client region, one of 'na', 'euw' or 'eune'
# 	username: 'dotaesnumerouno' # must be lowercase!
# 	password: 'penis2'
# 	version: '1.59.12_04_30_11_00' # Lol Client version - must be "current" or it wont work. This is correct as at 21/03/2012

#console.log(options)
client={}
heartbeat_interval=0
initial=1
h={}
start_client=->
	client=child_process.fork('client.js')
	client.on('message', (msg)->
		#console.log(msg)
		if msg.event=='connected' and initial==1
			initial=0
			_log("Connected".green)
			h=new RequestHandler(views, client)
			server=http.createServer(h.request)
			server.listen(options.listen_port||8081)
			heartbeat_interval=setInterval(->
				client.send({event:'keepalive'})
			, 600000)
		else if msg.event=='connected' and initial==0
			_log('Reconnected'.green)
			h.client=client
			h.connections=0
			#h.next()
		else if msg.event=='throttled'
			_log("THROTTLED".red)
		else if msg.event=='log'
			_log(msg.text)
	).on('exit', (code, signal)->
		clearInterval(heartbeat_interval)
		if code in [3, 5]
			console.log(code, signal)
			console.log(h.current)
			console.log(h.queue)
			console.log(h.connections)
			setTimeout(client_restart, 2000)
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
		process.send({event:'status', data:{connections:h.connections, total_requests:status.total_requests, reconnects:status.reconnects}, server:"#{options.region}:#{options.username}"})
)
