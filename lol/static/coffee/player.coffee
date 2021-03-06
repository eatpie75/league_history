class PlayerGamePageHandler
	constructor:()->
		@page=1
		@account_id=window.account_id
		@region=window.region
		@_bind()
		@qs=querystring(window.location.hash.slice(1))
		if 'page' of @qs
			@change_page(qs.page)
	_bind:->
		_this_=@
		$('.page_link').bind('click', (e)->
			_this_.destroy_items()
			_this_.change_page($(@))
		)
		window.connect_items()
	destroy_items:()->
		$('div.item.sprite').each(->
			$(@).popover('destroy')
		)
	change_page:(el=1)->
		if typeof(el)=='object' then page=el.data('page') else page=el
		$.ajax(
			type: 'GET',
			url: "#{window.AJAX_BASE}ajax/summoner_games/#{@region}/#{@account_id}/?page=#{page}",
			dataType: "html",
			success: (msg)=>
				$('#games').html(msg)
				@_bind()
				@page=page
				# @qs['page']=@page
				# window.location.hash=$.param(@qs)
		)

class ChampionSort
	constructor:()->
		@column=$('.table-sort.active:first')
		@column_str=@column.data('column')
		@direction=1
		@icon=@column.children('span').children('small')
		@_icons={'-1':'glyphicon glyphicon-arrow-up', '1':'glyphicon glyphicon-arrow-down'}
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
			@icon.removeClass(@_icons['1'])
		if @column_str==el.data('column')
			@icon.removeClass(@_icons["#{@direction}"]).addClass(@_icons["#{@direction*-1}"])
			@direction*=-1
		else
			@column.removeClass('active')
			@icon.removeClass(@_icons["#{@direction}"])
			@direction=1 if init==false
			@column=el
			@column_str=@column.data('column')
			@icon=@column.children('span').children('small')
			@column.addClass('active')
			@icon.addClass(@_icons["#{@direction}"])
		@sort(el.data('column'), el.data('spec-order'))
		qs=querystring(window.location.hash.slice(1))
		qs['sort']=el.data('column')
		if @direction==-1 then qs['direction']=@direction else delete qs.direction
		window.location.hash=$.param(qs)
	sort:(column, spec_order=null)->
		pregex=new RegExp('(\\d+)%', 'i')
		_base=(value_1, value_2, total_1, total_2)=>
			if value_1>value_2
				return -1*@direction
			else if value_1==value_2
				if total_1>total_2 then -1*@direction else if total_1<total_2 then 1*@direction else 0
			else
				return 1*@direction
		_sort=(a, b)=>
			[a, b]=[$(a), $(b)]
			value_1=a.children(".#{column}").text()
			value_2=b.children(".#{column}").text()
			if spec_order? and spec_order=='swin'
				[value_1,value_2]=[Number(value_1.match(pregex)[1]), Number(value_2.match(pregex)[1])]
				minimum=Math.round(window.num_games*0.04)
				lower_min=Math.round(window.num_games*0.01)
				total_1=Number(a.children(".total").text())
				total_2=Number(b.children(".total").text())
				if total_1>=minimum
					if total_2>=minimum
						return _base(value_1, value_2, total_1, total_2)
					else
						return -1*@direction
				else
					if total_2>=minimum
						return 1*@direction
					else
						if total_1>=lower_min
							if total_2>=lower_min
								return _base(value_1, value_2, total_1, total_2)
							else
								return -1*@direction
						else
							return _base(value_1, value_2, total_1, total_2)
			else if not isNaN(Number(value_1)) and not isNaN(Number(value_2))
				[value_1,value_2]=[Number(value_1), Number(value_2)]
				if value_1>value_2 then -1*@direction else if value_1==value_2 then 0 else 1*@direction
			else if pregex.test(value_1) and pregex.test(value_2)
				[value_1,value_2]=[Number(value_1.match(pregex)[1]), Number(value_2.match(pregex)[1])]
				if value_1>value_2 then -1*@direction else if value_1==value_2 then 0 else 1*@direction
			else
				if value_1>value_2 then 1*@direction else if value_1==value_2 then 0 else -1*@direction
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
			success: (msg)->
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
		success: (msg)->
			$('#last-updated').text("LAST UPDATED:#{msg.msg}")
			if msg.status=='QUEUE'
				setTimeout(_update_status, msg.delay)
	)

$(document).ready(->
	if $('.page_link').length>0 then window.page_handler=new PlayerGamePageHandler()
	if $('.table-sort.active:first').length>0 then window.champion_sort=new ChampionSort()
	if $('#stat-filter').length>0 then window.stat_filter=new StatFilter()
	$('#force-update').bind('click', force_update)
	$('a[data-toggle="tab"]').click((e)->
		e.preventDefault()
		$(@).tab('show')
	)
)
