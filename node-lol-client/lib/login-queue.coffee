u		= require('underscore')
http	= require('http')
https	= require('https')

class performQueueRequest
	constructor:(@host, @username, @password, @cb)->
		@options={
			host: host
			port: 443
			method: 'POST'
		}
		@_attempt_login()
	_next_check:=>
		remaining=Math.round((@target-@current)/@queue_rate)
		console.log("#{@username} in queue, postition:#{@current}/#{@target}, #{Math.floor(remaining/60)}:#{Math.round(remaining%60)} remaining")
		diff=@target-@current
		if diff<100
			delay=7000
		else if diff<1000
			delay=10000
		else if diff<10000
			delay=30000
		else
			delay=180000
		setTimeout(@_check_queue, delay)
	_check_queue:=>
		args={path:"/login-queue/rest/queue/ticker/#{@queue_name}"}
		@_request(args, null, (err, res)=>
			key=u.find(u.keys(res), (tmp)=>
				if Number(tmp)==@queue_node then true else false
			)
			@current=parseInt("0x#{res[key]}")
			if @current>=@target
				@_get_token()
			else
				@_next_check()
		)
	_get_token:=>
		args={path:"/login-queue/rest/queue/authToken/#{@user}"}
		console.log("#{@username} getting token")
		@_request(args, null, (err, res)=>
			if res.token?
				@_get_ip((ip)=>
					res.ip_address=ip
					@cb(null, res)
				)
			else
				@_next_check()
		)
	_get_ip:(cb)=>
		args={path:'/services/connection_info', host:'ll.leagueoflegends.com', port:80}
		@_request(args, null, (err, res)=>
			cb(res.ip_address)
		)
	_attempt_login:=>
		args={path:'/login-queue/rest/queue/authenticate'}
		data = "payload=user%3D#{@username}%2Cpassword%3D#{@password}"
		@_request(args, data, (err, res)=>
			if res.status=='LOGIN'
				@cb(null, res)
			else if res.status=='QUEUE'
				@user=res.user
				@queue_name=res.champ
				@queue_node=res.node
				@queue_rate=res.rate+0.0
				tmp=u.find(res.tickers, (ticker)=>
					if ticker.node==@queue_node then true else false
				)
				@target=tmp.id
				@current=tmp.current
				@_next_check()
		)
	_request:(kwargs, payload, cb)=>
		options=u.clone(@options)
		if kwargs? then u.extend(options, kwargs)
		if !payload? then options.method='GET'
		if options.port==443 then agent=https else agent=http
		req=agent.request(options, (res)->
			res.on('data', (d)->
				data=JSON.parse(d.toString('utf-8'))
				# console.log(data)
				cb(null, data)
			)
		)
		req.on('error', (err)->
			console.log err
			req.abort()
			process.exit(1)
		).on('socket', (socket)->
			socket.setTimeout(20000)
			socket.on('timeout', ()->
				console.log 'things are about to go poorly'
				req.abort()
				process.exit(1)
			)
		)
		if payload? then req.end(payload) else req.end()

module.exports = performQueueRequest
