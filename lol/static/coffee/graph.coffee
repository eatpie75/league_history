tier_goals={
	1:[100, 200, 300, 400]
	2:[500, 600, 700, 800, 900]
	3:[1000, 1100, 1200, 1300, 1400]
	4:[1500, 1600, 1700, 1800, 1900]
	5:[2000, 2100, 2200, 2300, 2400]
	6:[2500, 2551]
}
tier_colors={
	1:['#866500','#866500','#866500','#866500']
	2:['#9a9a9a','#9a9a9a','#9a9a9a','#9a9a9a','#9a9a9a']
	3:['#ffca2a','#ffca2a','#ffca2a','#ffca2a','#ffca2a']
	4:['#52a2ab','#52a2ab','#52a2ab','#52a2ab','#52a2ab']
	5:['#00c068','#00c068','#00c068','#00c068','#00c068']
	6:['#c30b0b','#c30b0b']
}
draw_chart=(data, kwargs={})->
	_chistorywr_hover=(index, options)->
		return "<b>#{options.data[index]['x']}</b><br>#{options.data[index]['y']}% Winrate<br>Played #{options.data[index]['count']} times"
	_lcs_num_reverser=(lcs)->
		tier=Math.floor(lcs/500)+1
		division=Math.floor((lcs-(tier-1)*500)/100)
		rank=100-Math.floor((lcs-(tier-1)*500-division*100))
		if tier==6
			division=4
			rank-=50
		return {'tier':tier, 'division':5-division, 'rank':rank}
	_lcs_hover=(index, options)->
		data=options.data[index]
		return JSON.stringify(_lcs_num_reverser(data['y']))
	# console.log data
	chart_defaults={
		type:'Line'
		element:'elo-graph'
		xkey:'x'
		ykeys:'y'
		labels:['ELO']
		ymax:'auto'
		ymin:'auto'
		# smooth:false
		hideHover:true
		lineColors: ['#3269b4', '#C0D800', '#CB4B4B', '#4DA74D', '#9440ED']
	}
	data_defaults={
		y:'rating'
		data_parse:'default'
		graph_begin_date:new Date('2010-01-01')
	}

	chart_options=$.extend(true, {}, chart_defaults, kwargs.chart_options)
	data_options=$.extend(true, {}, data_defaults, kwargs.data_options)
	parsed=[]
	# console.log chart_options

	if chart_options.type=='Line' and data_options.data_parse=='default'
		for day in data
			if day[1][data_options.y]<10
				continue
			parsed.push({'x':day[0], 'y':day[1][data_options.y]})
	else if chart_options.type=='Line' and data_options.data_parse=='chistorywr'
		chart_options.hoverCallback=_chistorywr_hover
		for day in data
			# date=new Date(day[0])
			# now=new Date()
			if day[1]['champions'][data_options.y]['count']<20# or (date.getUTCMonth()!=now.getUTCMonth()|date.getUTCFullYear()!=now.getUTCFullYear())
				continue
			parsed.push({'x':day[0], 'y':Math.round((day[1]['champions'][data_options.y]['won']/day[1]['champions'][data_options.y]['count'])*100), 'count':day[1]['champions'][data_options.y]['count']})
	else if chart_options.type=='Line' and data_options.data_parse=='chistorypop'
		for day in data
			if day[1]['champions'][data_options.y]['count']<10
				continue
			parsed.push({'x':day[0], 'y':(day[1]['champions'][data_options.y]['won']/day[1]['count'])*100})
	else if chart_options.type=='Line' and data_options.data_parse=='lcs' and data.length>2
		chart_options.hoverCallback=_lcs_hover
		chart_options.yLabelFormat=(x)->return ''
		chart_options.grid=false
		# chart_options.axes=false
		low=2600
		high=0
		for day in data
			if day[1]['avg']>high then high=day[1]['avg']
			if day[1]['avg']<low then low=day[1]['avg']
			parsed.push({'x':day[0], 'y':day[1]['avg']})
		low_rank=_lcs_num_reverser(low)
		high_rank=_lcs_num_reverser(high)
		low_tier=low_rank['tier']
		high_tier=high_rank['tier']
		goals=[]
		colors=[]
		prefix_goals=[]
		append_goals=[]
		prefix_colors=[]
		append_colors=[]
		for x in [low_tier..high_tier]
			# if x==low_tier and low_rank['division']!=5
			# 	s=low_rank['division']-1
			# 	e=50
			# else if x==high_tier and high_rank['division']!=1
			# 	s=0
			# 	e=high_rank['division']+1
			# else
			# 	s=0
			# 	e=50
			# goals=goals.concat(tier_goals[x].slice(s, e))
			# colors=colors.concat(tier_colors[x].slice(s, e))
			goals=goals.concat(tier_goals[x])
			colors=colors.concat(tier_colors[x])
		if low_tier==high_tier
			if low_tier!=1
				prefix_goals=prefix_goals.concat(tier_goals[low_tier-1].slice(-1))
				prefix_colors=prefix_colors.concat(tier_colors[low_tier-1].slice(-1))
			if low_tier!=6
				append_goals=append_goals.concat(tier_goals[low_tier+1][0])
				append_colors=append_colors.concat(tier_colors[low_tier+1][0])
		else
			if high_tier!=6
				append_goals=append_goals.concat(tier_goals[high_tier+1][0])
				append_colors=append_colors.concat(tier_colors[high_tier+1][0])
		chart_options.goals=[].concat(prefix_goals, goals, append_goals)
		chart_options.goalLineColors=[].concat(prefix_colors, colors, append_colors)
		chart_options.goalStrokeWidth=2
	else if chart_options.type=='Donut' and data_options.data_parse=='default'
		chart_options.colors=[
			'#D676E5'
			'#B15CBF'
			'#8D4299'
			'#692873'
			'#450F4E'

			'#88ACDE'
			'#6B8CBA'
			'#4F6D97'
			'#324E73'
			'#162F50'
		]
		for champion in data
			parsed.push({'label':"#{window.STATIC_URL}img/champions/#{champion['champion_id']}.png", 'value':champion[data_options.y], 'blue_team':champion.blue_team})
		parsed.sort((a,b)->
			if a.blue_team and !b.blue_team
				return 1
			else if !a.blue_team and b.blue_team
				return -1
			else if a.value>b.value
				return 1
			else if a.value<b.value
				return -1
			else
				return 0
		)

	chart_options['data']=parsed

	window.drawn_chart=Morris[chart_options['type']](chart_options)
	return [data_options, chart_options]

$(document).ready(->
	window.draw_chart=draw_chart
	if window.chart?
		if Array.isArray(window.chart)
			for i_chart in window.chart
				draw_chart(window.chart_data, i_chart)
		else
			draw_chart(window.chart_data, window.chart)
)
