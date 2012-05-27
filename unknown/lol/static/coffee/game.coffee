class TellMeMore
	constructor:()->
		@game=window.game_pk
		@cache={}
		@bind()
	bind:->
		_this_=@
		$('.player_expand').click((e)->
			_this_.expand($(@))
		)
	bind_toggle:(el, extra, expand=1)->
		_this_=@
		el.unbind()
		$(el).click((e)->
			if expand
				_this_.expand($(@))
			else
				_this_.collapse($(@), extra)
		)
	info_template:_.template(
		"<td colspan=11>
			<div class='span4'>
				<b>Physical/Magical Damage</b><br>
				<div class='hori-bar purple' title='Magical Damage'><div class='red' title='Physical Damage' style='width:<% print((physical_damage_dealt/damage_dealt)*100) %>%;'></div></div>
			</div>
		</td>")
	get_info:(player)->
		if "#{player}" not in _.keys(@cache)
			$.ajax(
				type: 'GET'
				async: false
				url: "/ajax/player_info/#{player}/"
				dataType: "json"
				success:(msg)=>
					@cache[player]=msg
			)
		return @cache[player]
	expand:(el)->
		player=el.data('player')
		info=@get_info(player)
		extra=$("<tr class='drop-stats'></tr>").insertAfter(el.closest('tr'))
		extra.css('height')
		extra.css('height', '100px')
		setTimeout(=>
			extra.html(@info_template(info))
		, 210)
		# extra=$(@info_template(info)).insertAfter(el.closest('tr'))
		@bind_toggle(el, extra, 0)
	collapse:(el, extra)->
		extra.html('')
		extra.css('height', '0px')
		setTimeout(=>
			extra.remove()
		, 500)
		@bind_toggle(el)

$(document).ready(->
	window.tell_me_more=new TellMeMore()
)
