colors			= require('colors')
json			= require('JSON2').stringify
json2			= require('JSON2')
lol_client		= require('./lol-client')
models			= require('./lib/models')
nopt			= require('nopt')

_log=(text)->
		process.send({event:'log', server:"#{options.region}:#{options.username}", text:text})
# _log=(text)->
# 	d=new Date()
# 	time="#{d.getFullYear()}/#{d.getMonth()+1}/#{d.getDate()} #{d.getHours()}:#{if d.getMinutes()< 10 then '0'+d.getMinutes() else d.getMinutes()}:#{if d.getSeconds()< 10 then '0'+d.getSeconds() else d.getSeconds()}".white
# 	time=(time+'                             ').slice(0,29)
# 	console.log(time+" | "+text)

args=nopt(
	{
		username:String
		password:String
		region:['na', 'euw', 'eune']
		# port:Number
		version:String
	},
	{},
	process.argv
)
# console.log(args)
options=
	region:		args.region		||'na'				# Lol Client region, one of 'na', 'euw' or 'eune'
	username:	args.username	||'dotaesnumerouno'	# must be lowercase!
	password:	args.password	||'penis2'			# guess
	version: 	args.version	||'1.60.12_05_22_19_12'				# Lol Client version - must be "current" or it wont work. This is correct as at 21/03/2012
# console.log(args)
# console.log(options)

client=new lol_client(options)

client.on('connection', =>
	process.send({event:'connected'})
).on('throttled', =>
	process.send({event:'throttled'})
	process.exit(3)
)

process.on('message', (msg)->
	#console.log(msg)
	if msg.event=='get'
		query=msg.query
		model=new models.get[msg.model]({client:client})
		model.on('finished', (data, extra={})=>
			extra.region=options.region
			process.send({event:"#{msg.uuid}__finished", data:data, extra:extra})
		)
		model.get(query)
	if msg.event=='keepalive'
		client.keepAlive((err, result)->
			_log("Heartbeat".magenta)
		)
)

client.connect()
