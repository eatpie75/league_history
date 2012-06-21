LolClient = require('./lol-client')
util = require('util')

# Config stuff
options =
  region: 'na' # Lol Client region, one of 'na', 'euw' or 'eune'
  username: 'thosebananas' # must be lowercase!
  password: 'penis2'
  version: '1.60.12_05_22_19_12' # Lol Client version - must be "current" or it wont work. This is correct as at 21/03/2012

summoner = {
  name: 'eatpie75', # summoners name
}

client = new LolClient(options)
a=[]
# Listen for a successful connection event
# client.on 'connection', ->
#   #console.log 'Connected'
  
#   # Now do stuff!
#   #client.getSummonerByName summoner.name, (err, result) ->
#   #  console.log '#######################'
#   #  console.log result.object.name
#   client.getSummonerName [115259], (err, result)->
#     console.log '#######################'
#     console.log(err)
#     console.log '#######################'
#     #util.inspect(result.object, false, null, true)
#     console.log(result.object)
#     a=result
#     console.log '#######################'
#     #util.format('%j', result.object.gameStatistics)
#     return null

client.connect() # Perform connection

module.exports=client