child_process	= require('child_process')
colors			= require('colors')
util			= require('util')

express			= require('express')
routes			= require('./routes')
http			= require('http')
path			= require('path')

id=''
options={}
client={}
initial=true
status=
	login_errors:0
	total_requests:0
	reconnects:0
	connected:false
af_app=JSON.parse(process.env.VCAP_APPLICATION)
instance=af_app.instance_index

_log=(text)->
	console.log text


lolclient_middleware=(req, res, next)->
	req.lolclient=app.settings.lolclient
	next()
bridge_status_middleware=(req, res, next)->
	req.bridge_status=status
	next()

app=express.createServer()
app.configure(->
	app.use(express.logger('dev'))
	app.use(express.bodyParser())
	app.use(express.methodOverride())
	app.use(express.compress())
	app.use(app.router)
)
app.configure('development', ->
	app.use(express.errorHandler())
)

app.get('/status/', bridge_status_middleware, routes.status)
app.get('/mass_update/', lolclient_middleware, routes.mass_update)
app.get('/get_names/', lolclient_middleware, routes.get_names)
app.get('/search/', lolclient_middleware, routes.search)
app.get('/spectate/', lolclient_middleware, routes.spectate)
app.get('/masterybook/', lolclient_middleware, routes.masterybook)

app.get('/', (req, res)->res.send(JSON.stringify(process.env)))

_log("Preparing to connect".grey)


start_client=->
	if not initial
		options=require('./servers.json')[instance]
	client=child_process.fork('client.js')
	client.on('message', (msg)->
		#console.log(msg)
		if msg.event=='connected' and initial
			initial=false
			_log("Connected".green)
			status.login_errors=0
			status.connected=true
			app.set('lolclient', client)
			app.listen(app.settings.port)
		else if msg.event=='connected' and not initial
			_log('Reconnected'.green)
			status.login_errors=0
			status.connected=true
			app.set('lolclient', client)
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
			setTimeout(client_restart, 2000)
		else if code in [1,4]
			get_time=()=>
				if status.login_errors*500+1000<=6000
					_log("restarting client in #{status.login_errors*500+1000}ms")
					status.login_errors*500+1000
				else if 10<status.login_errors<20
					_log('restarting client in 10s')
					10000
				else if 20<=status.login_errors<30
					_log('restarting client in 1m')
					60000
				else if 30<=status.login_errors<40
					_log('restarting client in 5m')
					300000
				else if 40<=status.login_errors
					_log('restarting client in 10m')
					600000
			status.login_errors+=1
			setTimeout(client_restart, get_time())
		else
			console.log(code, signal)
	)
	client.send({event:'connect', options:options})
client_restart=->
	client.removeAllListeners()
	client=null
	start_client()
	status.reconnects+=1

# process.on('message', (msg)->
# 	if msg.event=='connect'
# 		id=msg.id
# 		options=msg.options
# 		app.set('port', options.listen_port)
# 		start_client()
# 	else if msg.event=='status'
# 		process.send({event:'status', data:{connected:status.connected, total_requests:status.total_requests, reconnects:status.reconnects}, server:"#{id}"})
# 	else
# 		msg=null
# )

options=require('./servers.json')[instance]
id="#{options.region}:#{options.username}"
status.id=id
app.set('port', process.env.VCAP_APP_PORT)
start_client()
