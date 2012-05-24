child_process	= require('child_process')
colors			= require('colors')
events			= require('events')

_log=(msg)->
	blank='                                                 '
	d=new Date()
	time=" #{d.getFullYear()}/#{d.getMonth()+1}/#{d.getDate()} #{d.getHours()}:#{if d.getMinutes()< 10 then '0'+d.getMinutes() else d.getMinutes()}:#{if d.getSeconds()< 10 then '0'+d.getSeconds() else d.getSeconds()}".white
	info=(msg.server+time+blank).slice(0,49)
	console.log(info+" | "+msg.text)

servers=[
	{username:'dotaesnumerouno', password:'penis2', region:'na', port:8081, version:'1.60.12_05_22_19_12'}
	{username:'thosebananas', password:'penis2', region:'na', port:8082, version:'1.60.12_05_22_19_12'}
	{username:'dotaesnumerouno', password:'penis2', region:'euw', port:8083, version:'1.59.12_05_04_10_59'}
	# {username:'dotaesnumerouno', password:'penis2', region:'eune', port:8084}
]


bind_events=(server)->
	server.on('exit', (code, signal)->
		#console.log(@)
		console.log(code, signal)
	).on('message', (msg)->
		if msg.event=='log'
			#console.log(msg)
			_log(msg)
	)


for server in servers
	#console.log(server)
	tmp=child_process.fork('learn.js', ['--username', server.username, '--password', server.password, '--region', server.region, '--port', server.port, '--version', server.version])
	#tmp.stdout.pipe(process.stdout, {end:false})
	#console.log(tmp)
	bind_events(tmp)
