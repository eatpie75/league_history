child_process	= require('child_process')
colors			= require('colors')
express			= require('express')
http			= require('http')
path			= require('path')
routes			= require('./routes')

clients=[]

_log=(msg)->
	blank='                                                 '
	d=new Date()
	time=" #{d.getFullYear()}/#{d.getMonth()+1}/#{d.getDate()} #{d.getHours()}:#{if d.getMinutes()< 10 then '0'+d.getMinutes() else d.getMinutes()}:#{if d.getSeconds()< 10 then '0'+d.getSeconds() else d.getSeconds()}".white
	info=(msg.server+time+blank).slice(0,49)
	console.log(info+" | "+msg.text)

bind_events=(server)->
	server.on('exit', (code, signal)->
		console.log(code, signal)
	).on('message', (msg)->
		if msg.event=='log'
			_log(msg)
	)

af_app=JSON.parse(process.env.VCAP_APPLICATION)
instance=af_app.instance_index

servers=require('./servers.json')

for server, options of servers
	tmp=child_process.fork('bridge.js')
	tmp.send({'event':'connect', 'options':options, 'id':server})
	bind_events(tmp)
	clients.push(tmp)


app=express()
app.configure(->
	app.set('port', process.env.VCAP_APP_PORT || 3000)
	app.use(express.logger('dev'))
	app.use(express.bodyParser())
	app.use(express.methodOverride())
	app.use(express.compress())
	app.use(app.router)
)
app.configure('development', ->
	app.use(express.errorHandler())
)

app.get('/', (req, res)->res.send(fs.readdirSync("#{process.env.HOME}/app/")))
app.get(/\/(\d+)\/([\s\S]*)/, routes.index)
console.log app.settings.port
http.createServer(app).listen(app.settings.port)
