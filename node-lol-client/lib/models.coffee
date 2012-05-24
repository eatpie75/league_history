ev		= require('events').EventEmitter
json	= require('JSON2').stringify

#_log=(text)->
#		process.send({event:'log', server:"#{options.region}:#{options.username}", text:text})
# _log=(text)->
# 	d=new Date()
# 	time="#{d.getFullYear()}/#{d.getMonth()+1}/#{d.getDate()} #{d.getHours()}:#{if d.getMinutes()< 10 then '0'+d.getMinutes() else d.getMinutes()}:#{if d.getSeconds()< 10 then '0'+d.getSeconds() else d.getSeconds()}".white
# 	time=(time+'                             ').slice(0,29)
# 	console.log(time+" | "+text)
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
	get:(args)=>
		#console.log(args)
		@summoners=args.summoners
		@client.getSummonerName(@summoners, (err, result)=>
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
	get:(args)=>
		account_id=args.account_id
		@client.getSummonerStats(account_id, (err, result)=>
			if err?
				data=err
			else
				@org=result.object
				@account_id=@org.userId.value
				@parse()
			@emit('finished', @data, {account_id:@account_id})
		)
	toJSON:=>
		return json(@data)

class RecentGames extends ev
	constructor:(options)->
		#_log('Parsing games'.yellow)
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
				'game_map'			:game.gameMapId
				'game_mode'			:game.gameMode
				'game_type'			:game.gameType
				'team'				:if game.teamId.value==100 then 'blue' else 'purple'
				'afk'				:game.afk
				'leaver'			:game.leaver
				'ip_earned'			:game.ipEarned.value
				'xp_earned'			:game.experienceEarned.value
				'boost_ip'			:game.boostIpEarned.value
				'boost_xp'			:game.boostXpEarned.value
				'champion'			:game.championId.value
				'date'				:game.createDate
				'players'			:(player.object.summonerId.value for player in game.fellowPlayers.data)
				'summoner_level'	:game.level.value
				'premade_size'		:game.premadeSize
				'premade_team'		:game.premadeTeam
				'skin_index'		:game.skinIndex
				'skin_name'			:game.skinName
				'summoner_spell_one':game.spell1.value
				'summoner_spell_two':game.spell2.value
				'queue_length'		:game.timeInQueue
				'queue_type'		:game.queueType
				'ping'				:game.userServerPing
				'stats'				:{}
			}
			#current.players.push(game.userId.value)
			for stat in game.statistics.data
				current['stats'][stat.object.statType.toLowerCase()]=stat.object.value.value
			for key in [
				'num_deaths', 'champions_killed', 'assists', 'largest_critical_strike', 'largest_killing_spree', 'largest_multi_kill',
				'item0', 'item1', 'item2', 'item3', 'item4', 'item5',
				'minions_killed', 'gold_earned', 'physical_damage_dealt_player', 'magic_damage_dealt_player',
				'physical_damage_taken', 'magic_damage_taken', 'total_heal', 'total_time_spent_dead', 'neutral_minions_killed', 'turrets_killed',
				'inhibitors_destroyed', 'lose', 'win'#, 'nodes_neutralised', 'node_neutralisation_assists', 'nodes_captured',
				#'victory_points', 'objectives', 'total_score', 'objective_score', 'combat_score', 'rank', 'damage_taken'
			]
				if not has_key(current.stats, key)
					current.stats[key]=0
			current.stats.damage_taken=current.stats.physical_damage_taken+current.stats.magic_damage_taken
			current.stats.damage_dealt=current.stats.physical_damage_dealt_player+current.stats.magic_damage_dealt_player
			@data.push(current)
			@data.sort((a,b)->if a.id>b.id then -1 else if a.id<b.id then 1 else  0)
		return @data
	get:(args)=>
		account_id=args.account_id
		@client.getMatchHistory(account_id, (err, result)=>
			if err?
				consolg.log('Error'.red+err)
				data=err
			else
				@org=result.object
				@account_id=@org.userId.value
				@parse()
			@emit('finished', @data, {account_id:@account_id})
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
			'level'				:@org.object.summonerLevelAndPoints.object.summonerLevel.value
			'profile_icon'		:@summoner.profileIconId
			'season_one_tier'	:@summoner.seasonOneTier
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
				@emit('finished', @data)
			)
		)
		if has_key(args, 'account_id')
			@account_id=args.account_id
			@emit('found_account_id')
		else if has_key(args, 'name')
			@client.getSummonerByName(args.name, (err, result)=>
				if err?
					@data=err
					@emit('finished', @data)
				else
					@account_id=result.object.acctId.value
					@emit('found_account_id')
			)
	toJSON:=>
		return json(@data)

class Search extends ev
	constructor:(options)->
		if options?
			if has_key(options, 'client') then @client=options.client
			if has_key(options, 'search')
				@search=options.search
				@account_id=@search.account_id
		@data={}
	parse:=>
		@data={}
		current={
			'account_id'		:@search.acctId.value
			'summoner_id'		:@search.summonerId.value
			'internal_name'		:@search.internalName
			'name'				:@search.name
			'profile_icon'		:@search.profileIconId
		}
		@data=current
		return @data
	get:(args)=>
		name=args.name
		@client.getSummonerByName(name, (err, result)=>
			if err?
				@data=err
				@emit('finished', @data)
			else if err==null and result==null
				@data={'null':'null'}
			else
				# console.log(err, result)
				@account_id=result.object.acctId.value
				@search=result.object
				@parse()
			@emit('finished', @data)
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
exports.Search		=Search

exports.get		={'PlayerNames':exports.PlayerNames, 'PlayerStats':exports.PlayerStats, 'RecentGames':exports.RecentGames, 'Summoner':exports.Summoner, 'RunePage':exports.RunePage, 'Search':exports.Search}
