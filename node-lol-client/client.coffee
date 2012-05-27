colors			= require('colors')
json			= require('JSON2').stringify
json2			= require('JSON2')
lol_client		= require('./lol-client')
models			= require('./lib/models')
nopt			= require('nopt')

_log=(text)->
		process.send({event:'log', server:"#{options.region}:#{options.username}", text:text})

options={}
client={}

process.on('message', (msg)->
	#console.log(msg)
	if msg.event=='connect'
		options=
			region:		msg.options.region		||'na'				# Lol Client region, one of 'na', 'euw' or 'eune'
			username:	msg.options.username	||'dotaesnumerouno'	# must be lowercase!
			password:	msg.options.password	||'penis2'			# guess
			version: 	msg.options.version		||'1.60.12_05_22_19_12'				# Lol Client version - must be "current" or it wont work. This is correct as at 21/03/2012
		client=new lol_client(options)
		client.on('connection', =>
			process.send({event:'connected'})
		).on('throttled', =>
			process.send({event:'throttled'})
			process.exit(3)
		)
		client.connect()
	else if msg.event=='get'
		query=msg.query
		model=new models.get[msg.model]({client:client})
		model.on('finished', (data, extra={})=>
			extra.region=options.region
			process.send({event:"#{msg.uuid}__finished", data:data, extra:extra})
		)
		model.get(query)
	else if msg.event=='keepalive'
		client.keepAlive((err, result)->
			_log("Heartbeat".magenta)
		)
)
