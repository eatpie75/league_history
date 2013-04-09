fs			= require('fs')
path		= require('path')
{exec}		= require('child_process')
async		= require('../clientemu/node_modules/async')
uglifyjs	= require('../clientemu/node_modules/uglify-js')
uglifycss	= require('../clientemu/node_modules/uglifycss')

Cakefile		= 'Cakefile'
BASE			= 'lol'
COFFEEINDIR		= "#{BASE}/static/coffee"
COFFEEOUTDIR	= "#{BASE}/static/debug"
JSOUTDIR		= "#{BASE}/static/js"
JSTOCOMBINE	= [
	'items.js'
	'core.js'
	'player.js'
	'game.js'
	# 'champions.js'
	'graph.js'
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
	fs.mkdirSync(TMPDIR)
	console.log(">coffee -o #{COFFEEOUTDIR}/ -c #{COFFEEINDIR}/")
	# exec("coffee -o #{COFFEEOUTDIR}/ -c #{COFFEEINDIR}/", (err, stdout, stderr)->
	exec("coffee -o #{COFFEEOUTDIR}/ -c #{COFFEEINDIR}/", (err, stdout, stderr)->
		if stderr or err then console.log(err, stderr)
		cb(null)
	)
compress_js=(cb)->
	js=[]
	size=0
	for file in JSTOCOMBINE
		tmp=fs.readFileSync("#{COFFEEOUTDIR}/#{file}", 'utf8')
		# js+=tmp
		size+=tmp.length
		# fs.unlinkSync("#{TMPDIR}/#{file}")
		js.push("#{COFFEEOUTDIR}/#{file}")
	# console.log("Compressing #{file}")
	# ast=uglifyjs.parser.parse(js)
	# ast=uglifyjs.uglify.ast_mangle(ast)
	# ast=uglifyjs.uglify.ast_squeeze(ast)
	# result=uglifyjs.uglify.gen_code(ast)
	result=uglifyjs.minify(js)
	fs.writeFileSync("#{JSOUTDIR}/main.js", result.code)
	console.log("main.js >> Before:#{size} After:#{result.code.length} Diff:#{result.code.length-size}")
	cb(null)
compile_less=(cb)->
	OPENCHILDREN=0
	for file in LESSINFILES
		OPENCHILDREN+=1
		console.log(">lessc #{LESSINDIR}/#{file[0]} #{LESSOUTDIR}/#{file[1]}")
		exec("lessc #{LESSINDIR}/#{file[0]} #{LESSOUTDIR}/#{file[1]}", (err, stdout, stderr)->
			if stderr or err then console.log(err, stderr)
			OPENCHILDREN-=1
			if OPENCHILDREN==0
				cb(null)
		)
compress_css=(cb)->
	for file in LESSINFILES
		# console.log("Compressing #{file[1]}")
		tmp=fs.readFileSync("#{LESSOUTDIR}/#{file[1]}", 'utf8')
		plength=tmp.length
		tmp=uglifycss.processString(tmp, {uglyComments:true})
		fs.writeFileSync("#{LESSOUTDIR}/#{file[1]}", tmp)
		console.log("#{file[1]} >> Before:#{plength} After:#{tmp.length} Diff:#{tmp.length-plength}")
	cb(null)
compile_sprites=(cb)->
	OPENCHILDREN=0
	for dir in fs.readdirSync(SPRITEINDIR)
		OPENCHILDREN+=1
		console.log(">glue #{SPRITEINDIR}/#{dir}/ --css=#{TMPDIR}/ --img=#{SPRITEIMGOUTDIR}/ --url=../img/sprites/ --ignore-filename-paddings")
		exec("glue #{SPRITEINDIR}/#{dir}/ --css=#{TMPDIR}/ --img=#{SPRITEIMGOUTDIR}/ --url=../img/sprites/ --ignore-filename-paddings", (err, stdout, stderr)->
			if stderr or err then console.log(err, stderr)
			OPENCHILDREN-=1
			if OPENCHILDREN==0
				cb(null)
		)
compress_sprites=(cb)->
	tmp=''
	for file in fs.readdirSync(TMPDIR)
		if path.extname("#{TMPDIR}/#{file}")!='.css' then continue
		tmp+=fs.readFileSync("#{TMPDIR}/#{file}")
		fs.unlinkSync("#{TMPDIR}/#{file}")
	ptmp=tmp.length
	tmp=uglifycss.processString(tmp)
	console.log("#{SPRITEOUTFILE} >> Before:#{ptmp} After:#{tmp.length} Diff:#{tmp.length-ptmp}")
	fs.writeFileSync("#{SPRITECSSOUTDIR}/#{SPRITEOUTFILE}", tmp)
	cb(null)
clean_build=(cb)->
	for file in fs.readdirSync(TMPDIR)
		fs.unlinkSync("#{TMPDIR}/#{file}")
	fs.rmdirSync(TMPDIR)
	cb(null)

task('build', ->
	async.waterfall([
		compile_coffee
		compress_js
		compile_less
		compress_css
		clean_build
	], (err, results)->
		console.log('Build Complete.')
	)
)

task('all', ->
	invoke('clean')
	# fs.mkdirSync(TMPDIR)
	async.waterfall([
		compile_coffee
		compress_js
		compile_less
		compress_css
		compile_sprites
		compress_sprites
		clean_build
	], (err, results)->
		console.log('Build Complete.')
	)
)

task('clean', ->
	for file in fs.readdirSync(LESSOUTDIR)
		if file='morris.css' then continue
		console.log("Deleting #{LESSOUTDIR}/#{file}")
		fs.unlinkSync("#{LESSOUTDIR}/#{file}")
	for file in fs.readdirSync(SPRITEIMGOUTDIR)
		console.log("Deleting #{SPRITEIMGOUTDIR}/#{file}")
		fs.unlinkSync("#{SPRITEIMGOUTDIR}/#{file}")
)
