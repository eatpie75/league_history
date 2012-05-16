colors		= require('colors')
events		= require('events')
qs			= require('querystring')
lol_client	= require('./lol-client')
models		= require('./lib/models')

_log=(text)->
		d=new Date()
		time="#{d.getFullYear()}/#{d.getMonth()+1}/#{d.getDate()} #{d.getHours()}:#{d.getMinutes()}".white
		time=(time+'                          ').slice(0,26)
		console.log(time+" | "+text)
has_key=(obj, key)->obj.hasOwnProperty(key)

class GetNames
	constructor:(query, local_client, ev, request, response)->
		@client=local_client
		@ev=ev
		@request=request
		@response=response
		@summoners=qs.parse(query)['ids'].split(',').map(Number)
	go:=>
		names=new models.PlayerNames({client:@client})
		names.on('finished', (result)=>
			data=status:200, body:result
			@ev.emit('finished', data, @request, @response)
		)
		names.get(@summoners)
		return false

class MassUpdate
	constructor:(query, local_client, ev, request, response)->
		@client=local_client
		@ev=ev
		@request=request
		@response=response
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
		@ev.on('next', @_next)
	go:=>
		@ev.emit('next')
	_next:=>
		if @running_queries<5 and @queue.length>0
			@running_queries+=1
			key=@queue.shift()
			summoner=new models.Summoner({client:@client})
			playerstats=new models.PlayerStats({client:@client})
			summoner.on('finished', (result)=>
				if not has_key(@data.body.accounts, summoner.account_id)
					@data.body.accounts[summoner.account_id]={}
				@data.body.accounts[summoner.account_id].profile=result
				playerstats.get(summoner.account_id)
				if @games
					games=new models.RecentGames({client:@client})
					@running_queries+=1
					games.on('finished', (result)=>
						@data.body.accounts[games.account_id].games=result
						@running_queries-=1
						@ev.emit('next')
					)
					games.get(summoner.account_id)
			)
			playerstats.on('finished', (result)=>
				@data.body.accounts[summoner.account_id].stats=result
				@running_queries-=1
				@ev.emit('next')
			)
			summoner.get(key)
		else if @running_queries==0 and @queue.length==0
			@ev.emit('finished', @data, @request, @response)
			@ev.removeAllListeners('fetched').removeAllListeners('next')

class RecentGames
	constructor:(query, local_client, ev, request, response)->
		@client=local_client
		@ev=ev
		@request=request
		@response=response
		@query=qs.parse(query)
		@account=Number(@query['account'])
		@data={}
	go:=>
		_log('Fetching games'.yellow)
		games=new models.RecentGames({client:@client})
		games.on('finished', (result)=>
			data=status:200, body:result
			@ev.emit('finished', data, @request, @response)
		)
		games.get(@account)
		return false

class GetSummonerData
	constructor:(query, local_client, ev, request, response)->
		@client=local_client
		@ev=ev
		@request=request
		@response=response
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
			@ev.emit('finished', @data, @request, @response)
		)
		summoner_data.get(@key)

views=
	'/get_names/'		: GetNames
	'/mass_update/'		: MassUpdate
	'/recent_games/'	: RecentGames
	'/get_data/'		: GetSummonerData

module.exports=views
