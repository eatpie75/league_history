LolClient = require('./lol-client')
util = require('util')

# Config stuff
options =
	region: 'na' # Lol Client region, one of 'na', 'euw' or 'eune'
	username: 'dotaesnumerouno' # must be lowercase!
	password: 'penis2'
	version: '1.59.12_04_30_11_00' # Lol Client version - must be "current" or it wont work. This is correct as at 21/03/2012

client = new LolClient(options)
summoners=[]
#console.log(process.argv)
for summoner in process.argv[2..]
	summoners.push(summoner/1)
client.on 'connection', ->
	client.getSummonerName summoners, (err, result)->
		console.log(util.format('%j', result.data))
		process.exit()

client.connect() # Perform connection
