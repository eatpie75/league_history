ev		= require('events').EventEmitter
json	= require('JSON2').stringify

_log=(text)->
		d=new Date()
		time="#{d.getFullYear()}/#{d.getMonth()+1}/#{d.getDate()} #{d.getHours()}:#{d.getMinutes()}".white
		time=(time+'                          ').slice(0,26)
		console.log(time+" | "+text)
has_key=(obj, key)->obj.hasOwnProperty(key)

class PlayerNames extends ev
	constructor:(options)->
		if options?
			if options.hasOwnProperty('client')
				@client=options.client
			if options.hasOwnProperty('summoners') then @summoners=summoners
		@data=[]
	parse:=>
		#
	get:(summoners)=>
		@client.getSummonerName(summoners, (err, result)=>
			if err?
				data=err
			else
				data=result.data
			@emit('finished', data)
		)

class PlayerStats extends ev
	constructor:(options)->
		if options?
			if options.hasOwnProperty('client') then @client=options.client
			if options.hasOwnProperty('stats')
				@org=options.stats
				@account_id=@org.userId.value
		@data=[]
	parse:=>
		@data=[]
		for game_type in @org.playerStatSummaries.object.playerStatSummarySet.data
			stats=game_type.object
			current={
				'game_type'			:stats.playerStatSummaryTypeString
				'rating'			:stats.rating
				'rating_max'		:stats.maxRating
				'wins'				:stats.wins
				'losses'			:stats.losses
				'leaves'			:stats.leaves
				'aggregated_stats'	:{}
			}
			for stat in stats.aggregatedStats.object.stats.data
				current['aggregated_stats'][stat.object.statType.toLowerCase()]=stat.object.value.value
			@data.push(current)
		return @data
	get:(account_id)=>
		@client.getSummonerStats(account_id, (err, result)=>
			if err?
				data=err
			else
				@org=result.object
				@account_id=@org.userId.value
				data=@parse()
			@emit('finished', data)
		)
	toJSON:=>
		return json(@data)

class RecentGames extends ev
	constructor:(options)->
		_log('Parsing games'.yellow)
		if options.hasOwnProperty('client') then @client=options.client
		if options.hasOwnProperty('games')
			@org=games
			@account_id=@org.userId.value
		@data=[]
	parse:=>
		@data=[]
		for ogame in @org.gameStatistics.data
			game=ogame.object
			current={
				#'account_id'		:game.userId.value
				'id'				:game.gameId.value
				'map'				:game.gameMapId
				'game_mode'			:game.gameMode
				'game_type'			:game.gameType
				'team'				:if game.teamId.value==100 then 'blue' else 'purple'
				'afk'				:game.afk
				'leaver'			:game.leaver
				'boost_ip'			:game.boostIpEarned.value
				'boost_xp'			:game.boostXpEarned.value
				'ip_earned'			:game.ipEarned.value
				'experience_earned'	:game.experienceEarned.value
				'champion'			:game.championId.value
				'date'				:game.createDate
				'players'			:(player.object.summonerId.value for player in game.fellowPlayers.data)
				'level'				:game.level.value
				'premade_size'		:game.premadeSize
				'premade_team'		:game.premadeTeam
				'skin_index'		:game.skinIndex
				'skin_name'			:game.skinName
				'summoner_one'		:game.spell1.value
				'summoner_two'		:game.spell2.value
				'queue_length'		:game.timeInQueue
				'ping'				:game.userServerPing
				'stats'				:{}
			}
			current.players.push(game.userId.value)
			for stat in game.statistics.data
				current['stats'][stat.object.statType.toLowerCase()]=stat.object.value.value
			@data.push(current)
			@data.sort((a,b)->if a.id>b.id then -1 else if a.id<b.id then 1 else  0)
		return @data
	get:(account_id)=>
		@client.getMatchHistory(account_id, (err, result)=>
			if err?
				_log('Error'.red+err)
				data=err
			else
				@org=result.object
				@account_id=@org.userId.value
				data=@parse()
			@emit('finished', data)
		)
	toJSON:=>
		return json(@data)

class Summoner extends ev
	constructor:(options)->
		if options?
			if options.hasOwnProperty('client') then @client=options.client
			if options.hasOwnProperty('summoner')
				@summoner=options.summoner
				@account_id=@summoner.acctId.value
		@data={}
	parse:=>
		@data={}
		current={
			'account_id'		:@summoner.acctId.value
			'summoner_id'		:@summoner.sumId.value
			'internal_name'		:@summoner.internalName
			'name'				:@summoner.name
			'profile_icon'		:@summoner.profileIcon
			'season_one_tier'	:@summoner.seasoneOneTier
		}
		@data=current
		return @data
	get:(args)=>
		@on('found_account_id', =>
			@client.getSummonerData(@account_id, (err, result)=>
				if err?
					@data=err
				else
					@org=result
					@summoner=result.object.summoner.object
					@account_id=@summoner.acctId.value
					@parse()
				@emit('finished', @data, @request, @response)
			)
		)
		if has_key(args, 'account_id')
			@account_id=args.account_id
			@emit('found_account_id')
		else if has_key(args, 'name')
			@client.getSummonerByName(args.name, (err, result)=>
				if err?
					@data=err
					@emit('finished', @data, @request, @response)
				else
					@account_id=result.object.acctId.value
					@emit('found_account_id')
			)
	toJSON:=>
		return json(@data)

class RunePage
	constructor:(runepage, client)->
		if client?
			@client=client
		@runepage=runepage
		@data=[]
	parse:=>
		@data=[]
		for opage in @runepage.bookPages.data
			page=opage.object
			current={
				'id'		:page.pageId.value
				'name'		:page.name
				'created'	:page.createDate
				'slots'		:[]
			}
			for orune in page.slotEntries.data
				rune=orune.object
				tmp={
					'slot'	:rune.runeSlotId
					'id'	:rune.runeId
				}
				current['slots'].push(tmp)
			@data.push(current)
		return @data
	toJSON:=>
		return json(@data)

exports.PlayerNames	=PlayerNames
exports.PlayerStats	=PlayerStats
exports.RecentGames	=RecentGames
exports.Summoner	=Summoner
exports.RunePage	=RunePage
