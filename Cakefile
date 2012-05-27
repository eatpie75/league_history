fs		= require ('fs')
{exec}	= require('child_process')
colors	= require('./node-lol-client/node_modules/colors')

Cakefile		= 'Cakefile'
BASE			= 'unknown/lol'
COFFEEINDIR		= "#{BASE}/static/coffee"
COFFEEOUTDIR	= "#{BASE}/static/js"
LESSINDIR		= "#{BASE}/static/less"
LESSINFILES		= [
	['bootstrap/bootstrap.less','bootstrap.css']
	['main.less','main.css']
]
LESSOUT			= "#{BASE}/static/css"
SPRITEINDIR		= "#{BASE}/static/sprites"
SPRITEIMGOUTDIR	= "#{BASE}/static/img/sprites"
SPRITECSSOUTDIR	= "#{BASE}/static/css"
SPRITEOUTFILE	= 'sprites.css'
TMPDIR			= 'tmp'

OPENCHILDREN	= 0

task('build', ->
	# invoke('clean')
	# fs.mkdirSync(TMPDIR)
	console.log(">coffee -o #{COFFEEOUTDIR}/ -c #{COFFEEINDIR}/".yellow)
	exec("coffee -o #{COFFEEOUTDIR}/ -c #{COFFEEINDIR}/", (err, stdout, stderr)->
		if stderr or err then console.log(err, stderr)
	)
	for file in LESSINFILES
		console.log(">lessc #{LESSINDIR}/#{file[0]} #{LESSOUT}/#{file[1]}".yellow)
		exec("lessc #{LESSINDIR}/#{file[0]} #{LESSOUT}/#{file[1]}", (err, stdout, stderr)->
			if stderr or err then console.log(err, stderr)
		)
	# for dir in fs.readdirSync(SPRITEINDIR)
	# 	OPENCHILDREN+=1
	# 	console.log(">glue #{SPRITEINDIR}/#{dir}/ --css=#{TMPDIR}/ --img=#{SPRITEIMGOUTDIR}/ --url=../img/sprites/ --ignore-filename-paddings".yellow)
	# 	exec("glue #{SPRITEINDIR}/#{dir}/ --css=#{TMPDIR}/ --img=#{SPRITEIMGOUTDIR}/ --url=../img/sprites/ --ignore-filename-paddings", (err, stdout, stderr)->
	# 		if stderr or err then console.log(err, stderr)
	# 		OPENCHILDREN-=1
	# 		if OPENCHILDREN==0
	# 			tmp=''
	# 			for file in fs.readdirSync(TMPDIR)
	# 				tmp+=fs.readFileSync("#{TMPDIR}/#{file}")
	# 				fs.unlinkSync("#{TMPDIR}/#{file}")
	# 			ptmp=tmp.length
	# 			tmp=require('./node-lol-client/node_modules/recess/lib/min').compressor.cssmin(tmp)
	# 			console.log("#{SPRITEOUTFILE} >> Before:"+"#{ptmp}".cyan+" After:"+"#{tmp.length}".green+" Diff:"+"#{tmp.length-ptmp}".magenta)
	# 			fs.writeFileSync("#{SPRITECSSOUTDIR}/#{SPRITEOUTFILE}", tmp)
	# 			fs.rmdirSync(TMPDIR)
	# 			console.log('Build Complete.'.green)
	# 	)
)

task('all', ->
	invoke('clean')
	fs.mkdirSync(TMPDIR)
	console.log(">coffee -o #{COFFEEOUTDIR}/ -c #{COFFEEINDIR}/".yellow)
	exec("coffee -o #{COFFEEOUTDIR}/ -c #{COFFEEINDIR}/", (err, stdout, stderr)->
		if stderr or err then console.log(err, stderr)
	)
	for file in LESSINFILES
		console.log(">lessc #{LESSINDIR}/#{file[0]} #{LESSOUT}/#{file[1]}".yellow)
		exec("lessc #{LESSINDIR}/#{file[0]} #{LESSOUT}/#{file[1]}", (err, stdout, stderr)->
			if stderr or err then console.log(err, stderr)
		)
	for dir in fs.readdirSync(SPRITEINDIR)
		OPENCHILDREN+=1
		console.log(">glue #{SPRITEINDIR}/#{dir}/ --css=#{TMPDIR}/ --img=#{SPRITEIMGOUTDIR}/ --url=../img/sprites/ --ignore-filename-paddings".yellow)
		exec("glue #{SPRITEINDIR}/#{dir}/ --css=#{TMPDIR}/ --img=#{SPRITEIMGOUTDIR}/ --url=../img/sprites/ --ignore-filename-paddings", (err, stdout, stderr)->
			if stderr or err then console.log(err, stderr)
			OPENCHILDREN-=1
			if OPENCHILDREN==0
				tmp=''
				for file in fs.readdirSync(TMPDIR)
					tmp+=fs.readFileSync("#{TMPDIR}/#{file}")
					fs.unlinkSync("#{TMPDIR}/#{file}")
				ptmp=tmp.length
				tmp=require('./node-lol-client/node_modules/recess/lib/min').compressor.cssmin(tmp)
				console.log("#{SPRITEOUTFILE} >> Before:"+"#{ptmp}".cyan+" After:"+"#{tmp.length}".green+" Diff:"+"#{tmp.length-ptmp}".magenta)
				fs.writeFileSync("#{SPRITECSSOUTDIR}/#{SPRITEOUTFILE}", tmp)
				fs.rmdirSync(TMPDIR)
				console.log('Build Complete.'.green)
		)
)

task('clean', ->
	for file in fs.readdirSync(LESSOUT)
		console.log("Deleting #{LESSOUT}/#{file}".red)
		fs.unlinkSync("#{LESSOUT}/#{file}")
	for file in fs.readdirSync(SPRITEIMGOUTDIR)
		console.log("Deleting #{SPRITEIMGOUTDIR}/#{file}".red)
		fs.unlinkSync("#{SPRITEIMGOUTDIR}/#{file}")
)
