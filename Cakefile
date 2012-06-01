fs			= require ('fs')
{exec}		= require('child_process')
async		= require('./node-lol-client/node_modules/async')
colors		= require('./node-lol-client/node_modules/colors')
uglifyjs	= require('./node-lol-client/node_modules/uglify-js')
uglifycss	= require('./node-lol-client/node_modules/uglifycss')

Cakefile		= 'Cakefile'
BASE			= 'unknown/lol'
COFFEEINDIR		= "#{BASE}/static/coffee"
COFFEEOUTDIR	= "#{BASE}/static/js"
JSTOCOMPRESS	= [
	'player.js'
	'game.js'
	'items.js'
	'champions.js'
]
LESSINDIR		= "#{BASE}/static/less"
LESSINFILES		= [
	['bootstrap/bootstrap.less','bootstrap.css']
	['main.less','main.css']
]
LESSOUTDIR		= "#{BASE}/static/css"
SPRITEINDIR		= "#{BASE}/static/sprites"
SPRITEIMGOUTDIR	= "#{BASE}/static/img/sprites"
SPRITECSSOUTDIR	= "#{BASE}/static/css"
SPRITEOUTFILE	= 'sprites.css'
TMPDIR			= 'tmp'


compile_coffee=(cb)->
	console.log(">coffee -o #{COFFEEOUTDIR}/ -c #{COFFEEINDIR}/".yellow)
	exec("coffee -o #{COFFEEOUTDIR}/ -c #{COFFEEINDIR}/", (err, stdout, stderr)->
		if stderr or err then console.log(err, stderr)
		cb(null)
	)
compress_js=(cb)->
	for file in JSTOCOMPRESS
		console.log("Compressing #{file}".yellow)
		ast=uglifyjs.parser.parse(fs.readFileSync("#{COFFEEOUTDIR}/#{file}", 'utf8'))
		ast=uglifyjs.uglify.ast_mangle(ast)
		ast=uglifyjs.uglify.ast_squeeze(ast)
		result=uglifyjs.uglify.gen_code(ast)
		fs.writeFileSync("#{COFFEEOUTDIR}/#{file}", result)
	cb(null)
compile_less=(cb)->
	OPENCHILDREN=0
	for file in LESSINFILES
		OPENCHILDREN+=1
		console.log(">lessc #{LESSINDIR}/#{file[0]} #{LESSOUTDIR}/#{file[1]}".yellow)
		exec("lessc #{LESSINDIR}/#{file[0]} #{LESSOUTDIR}/#{file[1]}", (err, stdout, stderr)->
			if stderr or err then console.log(err, stderr)
			OPENCHILDREN-=1
			if OPENCHILDREN==0
				cb(null)
		)
compress_css=(cb)->
	for file in LESSINFILES
		# console.log("Compressing #{file[1]}".yellow)
		tmp=fs.readFileSync("#{LESSOUTDIR}/#{file[1]}", 'utf8')
		plength=tmp.length
		tmp=uglifycss.processString(tmp, {uglyComments:true})
		fs.writeFileSync("#{LESSOUTDIR}/#{file[1]}", tmp)
		console.log("#{file[1]} >> Before:"+"#{plength}".cyan+" After:"+"#{tmp.length}".green+" Diff:"+"#{tmp.length-plength}".magenta)
	cb(null)
compile_sprites=(cb)->
	OPENCHILDREN=0
	for dir in fs.readdirSync(SPRITEINDIR)
		OPENCHILDREN+=1
		console.log(">glue #{SPRITEINDIR}/#{dir}/ --css=#{TMPDIR}/ --img=#{SPRITEIMGOUTDIR}/ --url=../img/sprites/ --ignore-filename-paddings".yellow)
		exec("glue #{SPRITEINDIR}/#{dir}/ --css=#{TMPDIR}/ --img=#{SPRITEIMGOUTDIR}/ --url=../img/sprites/ --ignore-filename-paddings", (err, stdout, stderr)->
			if stderr or err then console.log(err, stderr)
			OPENCHILDREN-=1
			if OPENCHILDREN==0
				cb(null)
		)
compress_sprites=(cb)->
	tmp=''
	for file in fs.readdirSync(TMPDIR)
		tmp+=fs.readFileSync("#{TMPDIR}/#{file}")
		fs.unlinkSync("#{TMPDIR}/#{file}")
	ptmp=tmp.length
	tmp=uglifycss.processString(tmp)
	console.log("#{SPRITEOUTFILE} >> Before:"+"#{ptmp}".cyan+" After:"+"#{tmp.length}".green+" Diff:"+"#{tmp.length-ptmp}".magenta)
	fs.writeFileSync("#{SPRITECSSOUTDIR}/#{SPRITEOUTFILE}", tmp)
	fs.rmdirSync(TMPDIR)
	cb(null)
clean_build=(cb)->
	cb(null)

task('build', ->
	async.waterfall([
		compile_coffee
		# compress_js
		compile_less
		compress_css
	], (err, results)->
		console.log('Build Complete.'.green)
	)
)

task('all', ->
	invoke('clean')
	fs.mkdirSync(TMPDIR)
	async.waterfall([
		compile_coffee
		compress_js
		compile_less
		compress_css
		compile_sprites
		compress_sprites
		# clean_build
	], (err, results)->
		console.log('Build Complete.'.green)
	)
)

task('clean', ->
	for file in fs.readdirSync(LESSOUTDIR)
		console.log("Deleting #{LESSOUTDIR}/#{file}".red)
		fs.unlinkSync("#{LESSOUTDIR}/#{file}")
	for file in fs.readdirSync(SPRITEIMGOUTDIR)
		console.log("Deleting #{SPRITEIMGOUTDIR}/#{file}".red)
		fs.unlinkSync("#{SPRITEIMGOUTDIR}/#{file}")
)
