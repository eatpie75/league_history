LolClient = require('./lib/lol-client')
util = require('util')
fs = require('fs')
repl = require('repl')

options =
	region: 'na'
	username: 'unprojapina1'
	password: 'penis2'
	version: '1.64.12_07_27_15_01'

summoner=
	name: 'eatpie75'
	account_id:142098
	summoner_id:115259

client = new LolClient(options)
a=[]

client.on('connection', ()->
	con=repl.start({
		'prompt':'>'
		'useGlobal':true
	})
	con.context.client=client
	con.context.options=options
	con.context.summoner=summoner
)

console.log 'connecting'
client.connect()

module.exports=client