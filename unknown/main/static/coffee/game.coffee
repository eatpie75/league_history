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
		"<tr><td colspan=6 style='position:relative;'>
			<div class='span4'>
				<div style='border-bottom:1px solid #ddd;' class='span2'>
					Minion Kills:
				</div>
				<div style='border-bottom:1px solid #ddd;' class='span2 pull-right'>
					<%= minion_kills %>
				</div>
			</div>
		</td></tr>")
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
		extra=$(@info_template(info)).insertAfter(el.closest('tr'))
		@bind_toggle(el, extra, 0)
	collapse:(el, extra)->
		extra.remove()
		@bind_toggle(el)

$(document).ready(->
	window.tell_me_more=new TellMeMore
)
