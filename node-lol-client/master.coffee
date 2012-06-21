buffer			= require('buffer').Buffer
child_process	= require('child_process')
colors			= require('colors')
events			= require('events')
http			= require('http')
json			= require('JSON2').stringify
url				= require('url')
zlib			= require('zlib')

ev=events.EventEmitter
_log=(msg)->
	blank='                                                 '
	d=new Date()
	time=" #{d.getFullYear()}/#{d.getMonth()+1}/#{d.getDate()} #{d.getHours()}:#{if d.getMinutes()< 10 then '0'+d.getMinutes() else d.getMinutes()}:#{if d.getSeconds()< 10 then '0'+d.getSeconds() else d.getSeconds()}".white
	info=(msg.server+time+blank).slice(0,49)
	console.log(info+" | "+msg.text)

class RequestHandler extends ev
	constructor:(local_clients)->
		@clients=local_clients
		@on('finished', @respond).on('send', @send)
	request:(request, response)=>
		_this=@
		path=url.parse(request.url)
		if path.pathname=='/status/'
			data=[]
			_add_data=(msg)->
				if msg.event=='status'
					data.push({server:msg.server, data:msg.data})
				if data.length==_this.clients.length
					_this.emit('finished', {status:200, body:data}, request, response)
				@removeListener('message', _add_data)
			for client in @clients
				client.on('message', _add_data)
				client.send({event:'status'})
		else
			response.writeHead(404)
			response.write('404')
			response.end()
		return false
	respond:(data, request, response)=>
		_this=@
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
				_this.emit('send', response, obj, {'body':r})
			)
		else
			@emit('send', response, obj)
	send:(response, data, args)=>
		if args?
			for k,v of args
				data[k]=v
		content_length=new buffer(data['body']).length
		data['headers']['Content-Length']=content_length
		response.writeHead(data.status, data.headers)
		response.write(data.body)
		response.end()

bind_events=(server)->
	server.on('exit', (code, signal)->
		console.log(code, signal)
	).on('message', (msg)->
		if msg.event=='log'
			_log(msg)
	)

servers=[
	{username:'dotaesnumerouno', password:'penis2', region:'na', listen_port:8081, version:'1.61.12_06_18_11_51'}
	{username:'thosebananas', password:'penis2', region:'na', listen_port:8082, version:'1.61.12_06_18_11_51'}
	{username:'trondamener', password:'penis2', region:'na', listen_port:8085, version:'1.61.12_06_18_11_51'}
	{username:'dotaesnumerouno', password:'penis2', region:'euw', listen_port:8083, version:'1.60.12_05_22_19_12'}
	# # {username:'dotaesnumerouno', password:'penis2', region:'eune', port:8084}
]
clients=[]

for server in servers
	# tmp=child_process.fork('learn.js', ['--username', server.username, '--password', server.password, '--region', server.region, '--port', server.port, '--version', server.version])
	tmp=child_process.fork('learn.js')
	tmp.send({event:'connect', options:server})
	bind_events(tmp)
	clients.push(tmp)

h=new RequestHandler(clients)
server=http.createServer(h.request)
server.listen(8080, 'localhost')
