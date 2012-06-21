colors		= require('colors')
events		= require('events')
qs			= require('querystring')
util		= require('util')
uuid		= require('node-uuid')
models		= require('./lib/models')

_log=(text)->
		process.send({event:'log', server:"#{options.region}:#{options.username}", text:text})
has_key=(obj, key)->obj.hasOwnProperty(key)
sleep=(ms)->
	d=startTime=new Date().getTime()
	while d<startTime+ms
		d=new Date().getTime()
	return true

class GetNames
	constructor:(query, @client, @cb, @request, @response)->
		@uuid=uuid.v4()
		@summoners=qs.parse(query)['ids'].split(',').map(Number)
	go:=>
		@client.on('message', @get)
		@client.send({event:'get', model:'PlayerNames', query:{summoners:@summoners}, uuid:@uuid})
	get:(msg)=>
		if msg.event=="#{@uuid}__finished"
			data=status:200, body:msg.data
			@cb(data, @request, @response)
			@client.removeListener('message', @get)

class MassUpdate
	constructor:(query, @client, @cb, @request, @response)->
		@uuid=[uuid.v4(), uuid.v4(), uuid.v4()]
		@query=qs.parse(query)
		@data=
			status:200
			body:{errors:[], accounts:{}}
		@running_queries=0
		@queue=[]
		if @query['accounts']?
			@queue=@queue.concat(({account_id:account} for account in @query['accounts'].split(',')))
		if @query['names']?
			@queue=@queue.concat(({'name':name} for name in @query['names'].split(',')))
		if @query['games']? then @games=1 else @games=0
		@client.on('message', @get)
	go:=>
		@_next()
	get:(msg)=>
		if msg.event=="#{@uuid[0]}__finished"
			summoner=msg.data
			if not has_key(@data.body.accounts, summoner.account_id)
				@data.body.accounts[summoner.account_id]={}
			@data.body.accounts[summoner.account_id].profile=summoner
			@client.send({event:'get', model:'PlayerStats', query:{account_id:summoner.account_id}, uuid:@uuid[1]})
			if @games
				@running_queries+=1
				@client.send({event:'get', model:'RecentGames', query:{account_id:summoner.account_id}, uuid:@uuid[2]})
		else if msg.event=="#{@uuid[1]}__finished"
			@data.body.accounts[msg.extra.account_id].stats=msg.data
			@running_queries-=1
			@_next()
		else if msg.event=="#{@uuid[2]}__finished"
			@running_queries-=1
			@data.body.accounts[msg.extra.account_id].games=msg.data
			@_next()
		else if msg.event in ['throttled','timeout']
			@throttled()
		else
			console.log(msg)
	_next:=>
		if @running_queries<3 and @queue.length>0
			@running_queries+=1
			key=@queue.shift()
			console.log(key)
			try
				@client.send({event:'get', model:'Summoner', query:key, uuid:@uuid[0]})
			catch error
				console.log(error)
				console.log('oh god')
		else if @running_queries==0 and @queue.length==0
			@cb(@data, @request, @response)
			@client.removeListener('message', @get)
	throttled:=>
		@client.removeListener('message', @get)
		@queue=[]
		@response.writeHead(500)
		@response.end()

class RecentGames
	constructor:(query, @client, @cb, @request, @response)->
		@query=qs.parse(query)
		@account=Number(@query['account'])
		@data={}
	go:=>
		_log('Fetching games'.yellow)
		games=new models.RecentGames({client:@client})
		games.on('finished', (result)=>
			@data=status:200, body:result
			@cb(@data, @request, @response)
		)
		games.get(@account)
		return false

class GetSummonerData
	constructor:(query, @client, @cb, @request, @response)->
		@query=qs.parse(query)
		if @query['account']?
			@key={account_id:Number(@query['account'])}
		else if @query['name']?
			@key={name:@query['name']}
		if @query['runes']? then @runes=1 else @runes=0
		@data={}
	go:=>
		summoner_data=new models.Summoner({client:@client})
		summoner_data.on('finished', (result)=>
			@data=status:200, body:result
			if @runes
				@data.body['runes']=new models.RunePage(summoner_data.org.object.spellBook.object).parse()
			@cb(@data, @request, @response)
		)
		summoner_data.get(@key)

class Search
	constructor:(query, @client, @cb, @request, @response)->
		@uuid=uuid.v4()
		@name=qs.parse(query)['name']
	go:=>
		@client.on('message', @get)
		@client.send({event:'get', model:'Search', query:{name:@name}, uuid:@uuid})
	get:(msg)=>
		if msg.event=="#{@uuid}__finished"
			data=status:200, body:msg.data
			@cb(data, @request, @response)
			@client.removeListener('message', @get)

class GetSpectatorInfo
	constructor:(query, @client, @cb, @request, @response)->
		@uuid=uuid.v4()
		@query=qs.parse(query)
		@name=@query['name']
		if @query['link']? then @link=true else @link=false
	go:=>
		@client.on('message', @get)
		@client.send({event:'get', model:'SpectatorInfo', query:{name:@name}, uuid:@uuid})
	get:(msg)=>
		errors='OB-1':'No game', 'OB-2':'Game not observable', 'OB-3':'Game not started yet'
		# console.log(msg)
		if msg.event=="#{@uuid}__finished"
			data=status:200
			if msg.data.error?
				data.body=errors[msg.data.error]
			else
				if @link
					data.body="<a href='lolspectate://ip=#{msg.data.ip}&port=#{msg.data.port}&game_id=#{msg.data.game_id}&region=#{msg.data.region}&key=#{msg.data.key}'>#{@name}</a>"
					data.html=true
				else
					data.body=msg.data
			@cb(data, @request, @response)
			@client.removeListener('message', @get)

views=
	'/get_names/'		: GetNames
	'/mass_update/'		: MassUpdate
	# '/recent_games/'	: RecentGames
	# '/get_data/'		: GetSummonerData
	'/search/'			: Search
	'/spectate/'		: GetSpectatorInfo

module.exports=views
