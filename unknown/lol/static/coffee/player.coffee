class PlayerGamePageHandler
	constructor:()->
		@page=1
		@summoner=window.account_id
		@_bind()
	_bind:->
		_this_=@
		$('.page_link').bind('click', (e)->
			_this_.change_page($(@))
		)
	change_page:(el=1)->
		if typeof(el)=='object' then page=el.data('page') else page=el
		$.ajax(
			type: 'GET',
			url: "/ajax/summoner_games/#{@summoner}/?page=#{page}",
			dataType: "html",
			success: (msg)=>
				$('#games').html(msg)
				@_bind()
		)

class ChampionSort
	constructor:()->
		@direction=1
		@column=$('.table-sort.active:first')
		@column_str=@column.data('column')
		@icon=@column.children('span').children('i')
		@_icons={'-1':'icon-arrow-up', '1':'icon-arrow-down'}
		@_bind()
	_bind:->
		_this_=@
		$('.table-sort').bind('click', (e)->
			el=$(@)
			if _this_.column_str==el.data('column')
				_this_.icon.removeClass(_this_._icons["#{_this_.direction}"]).addClass(_this_._icons["#{_this_.direction*-1}"])
				_this_.direction*=-1
			else
				_this_.column.removeClass('active')
				_this_.icon.removeClass(_this_._icons["#{_this_.direction}"])
				_this_.direction=1
				_this_.column=el
				_this_.column_str=_this_.column.data('column')
				_this_.icon=_this_.column.children('span').children('i')
				_this_.column.addClass('active')
				_this_.icon.addClass(_this_._icons["#{_this_.direction}"])
			_this_.sort(el.data('column'))
		)
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
			$('#stat-filter').submit()
		)

$(document).ready(->
	window.page_handler=new PlayerGamePageHandler()
	window.champion_sort=new ChampionSort()
	window.stat_filter=new StatFilter()
)
