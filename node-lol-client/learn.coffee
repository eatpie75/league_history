buffer		= require('buffer').Buffer
colors		= require('colors')
events		= require('events')
http		= require('http')
json		= require('JSON2').stringify
qs			= require('querystring')
url			= require('url')
util		= require('util')
zlib		= require('zlib')
lol_client	= require('./lol-client')
views		= require('./views')

ev=new events.EventEmitter()

_log=(text)->
		d=new Date()
		time="#{d.getFullYear()}/#{d.getMonth()+1}/#{d.getDate()} #{d.getHours()}:#{d.getMinutes()}".white
		time=(time+'                          ').slice(0,26)
		console.log(time+" | "+text)

class RequestHandler
	constructor:(views, local_client)->
		@views=views
		@client=local_client
		ev.on('finished', @respond).on('send', @send)
	request:(request, response)=>
		path=url.parse(request.url)
		if path.pathname in Object.keys(@views)
			view=new @views[path.pathname](path.query, @client, ev, request, response)
			view.go()
			view=null
		else
			_log("#{path.pathname}".cyan+" >> Status:"+"404".red)
			response.writeHead(404)
			response.write('404')
			response.end()
		return false
	respond:(data, request, response)=>
			body=json(data.body)
			obj={
				'status'	:data.status
				'body'		:body
				'headers'	:{
					'Content-Type'		: 'application/json'
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
		_log("#{data.path}".cyan+" >> Status:"+"#{data.status}".green+" >> Length:"+"#{content_length}".magenta)

options=
	region: 'na' # Lol Client region, one of 'na', 'euw' or 'eune'
	username: 'dotaesnumerouno' # must be lowercase!
	password: 'penis2'
	version: '1.59.12_04_30_11_00' # Lol Client version - must be "current" or it wont work. This is correct as at 21/03/2012

_log("Preparing to connect".grey)

client=new lol_client(options)

client.on('connection', ->
	_log("Connected".green)
	h=new RequestHandler(views, client)
	server=http.createServer(h.request)
	server.listen(8081)
	setInterval(->
		client.keepAlive((err, result)->
			_log("Heartbeat".magenta)
		)
	, 360000)
)

client.connect()
