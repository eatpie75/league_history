tier_goals={
	1:[100, 200, 300, 400]
	2:[500, 600, 700, 800, 900]
	3:[1000, 1100, 1200, 1300, 1400]
	4:[1500, 1600, 1700, 1800, 1900]
	5:[2000, 2100, 2200, 2300, 2400]
	6:[2500, 2600]
}
tier_colors={
	1:['#866500','#866500','#866500','#866500','#866500']
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
		if tier==6 then division=4
		return {'tier':tier, 'division':5-division, 'rank':rank}
	_lcs_hover=(index, options)->
		data=options.data[index]
		return JSON.stringify(_lcs_num_reverser(data['y']))
	# console.log data
	chart_defaults={
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

	if data_options.data_parse=='default'
		for day in data
			if day[1][data_options.y]<10
				continue
			parsed.push({'x':day[0], 'y':day[1][data_options.y]})
	else if data_options.data_parse=='elo'
		for day in data
			if day[1][data_options.y]<10 or new Date(day[0])<data_options.graph_begin_date
				continue
			parsed.push({'x':day[0], 'y':day[1][data_options.y]})
	else if data_options.data_parse=='chistorywr'
		chart_options.hoverCallback=_chistorywr_hover
		for day in data
			date=new Date(day[0])
			now=new Date()
			if day[1]['champions'][data_options.y]['count']<20# or (date.getUTCMonth()!=now.getUTCMonth()|date.getUTCFullYear()!=now.getUTCFullYear())
				continue
			parsed.push({'x':day[0], 'y':Math.round((day[1]['champions'][data_options.y]['won']/day[1]['champions'][data_options.y]['count'])*100), 'count':day[1]['champions'][data_options.y]['count']})
	else if data_options.data_parse=='chistorypop'
		for day in data
			if day[1]['champions'][data_options.y]['count']<10
				continue
			parsed.push({'x':day[0], 'y':(day[1]['champions'][data_options.y]['won']/day[1]['count'])*100})
	else if data_options.data_parse=='lcs'
		chart_options.hoverCallback=_lcs_hover
		chart_options.yLabelFormat=(x)->return ''
		chart_options.grid=false
		# chart_options.axes=false
		low=2600
		high=0
		for day in data
			if day[1]['avg']>high then high=day[1]['avg']
			if day[1]['avg']<low then low=day[1]['avg']
			parsed.push('x':day[0], 'y':day[1]['avg'])
		low_tier=_lcs_num_reverser(low)['tier']
		high_tier=_lcs_num_reverser(high)['tier']
		goals=[]
		colors=[]
		prefix_goals=[]
		append_goals=[]
		prefix_colors=[]
		append_colors=[]
		for x in [low_tier..high_tier]
			goals=goals.concat(tier_goals[x])
			colors=colors.concat(tier_colors[x])
		if low_tier==high_tier
			prefix_goals=prefix_goals.concat(tier_goals[low_tier-1].slice(-1))
			append_goals=append_goals.concat(tier_goals[low_tier+1][0])
			prefix_colors=prefix_colors.concat(tier_colors[low_tier-1].slice(-1))
			append_colors=append_colors.concat(tier_colors[low_tier+1][0])
		chart_options.goals=prefix_goals.concat(goals, append_goals)
		chart_options.goalLineColors=prefix_colors.concat(colors, append_colors)
		chart_options.goalStrokeWidth=2

	chart_options['data']=parsed

	window.drawn_chart=Morris.Line(chart_options)
	return [data_options, chart_options]

$(document).ready(->
	window.draw_chart=draw_chart
	if window.chart? then draw_chart(window.chart_data, window.chart)
)
