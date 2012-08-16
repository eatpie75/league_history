class PlayerGamePageHandler
	constructor:()->
		@page=1
		@account_id=window.account_id
		@region=window.region
		@_bind()
	_bind:->
		_this_=@
		$('.page_link').bind('click', (e)->
			_this_.change_page($(@))
		)
		window.connect_items()
	change_page:(el=1)->
		if typeof(el)=='object' then page=el.data('page') else page=el
		$.ajax(
			type: 'GET',
			url: "#{window.AJAX_BASE}ajax/summoner_games/#{@region}/#{@account_id}/?page=#{page}",
			dataType: "html",
			success: (msg)=>
				$('#games').html(msg)
				@_bind()
		)

class ChampionSort
	constructor:()->
		@column=$('.table-sort.active:first')
		if @column.length>0
			@column_str=@column.data('column')
			@direction=1
			@icon=@column.children('span').children('i')
			@_icons={'-1':'icon-arrow-up', '1':'icon-arrow-down'}
			@_bind()
			qs=querystring(window.location.hash.slice(1))
			if 'sort' of qs
				if 'direction' of qs
					@direction=Number(qs.direction)
				@change($('.table-sort').filter((e)->
					$(@).data('column')==qs['sort']
				).first(), true)
	_bind:->
		_this_=@
		$('.table-sort').bind('click', (e)->
			_this_.change($(@))
		)
	change:(el, init=false)->
		if init
			@icon.removeClass(@_icons["#{1}"])
		if @column_str==el.data('column')
			@icon.removeClass(@_icons["#{@direction}"]).addClass(@_icons["#{@direction*-1}"])
			@direction*=-1
		else
			@column.removeClass('active')
			@icon.removeClass(@_icons["#{@direction}"])
			@direction=1 if init==false
			@column=el
			@column_str=@column.data('column')
			@icon=@column.children('span').children('i')
			@column.addClass('active')
			@icon.addClass(@_icons["#{@direction}"])
		@sort(el.data('column'))
		qs=querystring(window.location.hash.slice(1))
		qs['sort']=el.data('column')
		if @direction==-1 then qs['direction']=@direction else delete qs.direction
		window.location.hash=$.param(qs)
	sort:(column)->
		_sort=(a,b)=>
			pregex=new RegExp('(\\d+)%', 'i')
			c=$(a).children(".#{column}").text()
			d=$(b).children(".#{column}").text()
			if not isNaN(Number(c)) and not isNaN(Number(d))
				[c,d]=[Number(c), Number(d)]
				if c>d then -1*@direction else if c==d then 0 else 1*@direction
			else if pregex.test(c) and pregex.test(d)
				[c,d]=[Number(c.match(pregex)[1]), Number(d.match(pregex)[1])]
				if c>d then -1*@direction else if c==d then 0 else 1*@direction
			else
				if c>d then 1*@direction else if c==d then 0 else -1*@direction
		$('.cbody').append($('.cbody .sort').sort(_sort))
		@current_column=column

class StatFilter
	constructor:->
		@_bind()
	_bind:->
		_this_=@
		$('#stat-filter').bind('change', ->
			el=$(@)
			params={}
			params.game_map=el.children('#id_game_map').val() if el.children('#id_game_map').val()!='-1'
			params.game_mode=el.children('#id_game_mode').val() if el.children('#id_game_mode').val()!='-1'
			window.location.search=$.param(params)
		)

querystring=(oqs)->
	oqs=oqs.split('&')
	qs={}
	for option in oqs
		obj=option.split('=')
		if obj[0]=='' and obj.length==1 then break
		qs[decodeURI(obj[0])]=decodeURI(obj[1])
	qs

force_update=(e)->
	_update_status=()->
		$.ajax(
			type: 'GET',
			url: "#{window.AJAX_BASE}ajax/force_update_status/#{window.region}/#{window.account_id}/",
			dataType: "json",
			success: (msg)=>
				if msg.status=='QUEUE'
					setTimeout(_update_status, msg.delay)
				else if msg.status=='DONE'
					$('#last-updated').text(msg.msg)
		)
	$('#last-updated-block').html("<small id='last-updated'>WORKING...</small>")
	$.ajax(
		type: 'GET',
		url: "#{window.AJAX_BASE}ajax/force_update/#{window.region}/#{window.account_id}/",
		dataType: "json",
		success: (msg)=>
			$('#last-updated').text("LAST UPDATED:#{msg.msg}")
			if msg.status=='QUEUE'
				setTimeout(_update_status, msg.delay)
	)

draw_bgchart=(data, y='rating', aoptions={}, data_parse='default')->
	# console.log data
	container=document.getElementById("elo-graph")
	defaults={
		# subtitle:'ELO GRAPH'
		# fontColor:'#fff'
		# shadowSize:0
		xaxis: {
			mode:'time'
			showLabels:false
		}
		yaxis: {
			autoscale: true
			autoscaleMargin:1
			showLabels:false
			tickFormatter:(num)->"#{num}%"
		}
		mouse: {
			track:true
			trackFormatter:(obj)->"#{Flotr.Date.format(obj.x, '%y-%m-%d')}: #{Math.round(obj.y)}"
			sensiblility:3
			lineColor:'#fff'
			relative:true
		}
		lines: {
			fill:true
			show:true
		}
		points: {
			show:true
			lineWidth:1
			radius:2
			fillColor:'#00A8F0'
		}
		grid: {
			color:'#fff'
			verticalLines:false
			horizontalLines:false
			outline:''
		}
	}

	options=$.extend({}, defaults)
	$.extend(true, options, aoptions)
	# console.log options

	if data_parse=='default'
		parsed=[]
		for day in data
			if day[1][y]<10
				continue
			parsed.push([new Date(day[0]), day[1][y]])
	else if data_parse=='chistorywr'
		parsed=[]
		for day in data
			date=new Date(day[0])
			now=new Date()
			if day[1]['champions'][y]['count']<10# or (date.getUTCMonth()!=now.getUTCMonth()|date.getUTCFullYear()!=now.getUTCFullYear())
				continue
			parsed.push([date, (day[1]['champions'][y]['won']/day[1]['champions'][y]['count'])*100])
	else if data_parse=='chistorypop'
		parsed=[]
		for day in data
			if day[1]['champions'][y]['count']<10
				continue
			parsed.push([new Date(day[0]), (day[1]['champions'][y]['won']/day[1]['count'])*100])

	Flotr.draw(container, [parsed], options)

$(document).ready(->
	window.page_handler=new PlayerGamePageHandler()
	window.champion_sort=new ChampionSort()
	window.stat_filter=new StatFilter()
	window.draw_chart=draw_bgchart
	$('#force-update').bind('click', force_update)
	if window.bgchart? then draw_bgchart(window.data, window.bgchart)
	$('a[data-toggle="tab"]').click((e)->
		e.preventDefault()
		$(@).tab('show')
	)
)
