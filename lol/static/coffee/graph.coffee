draw_chart=(data, kwargs={})->
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
		for day in data
			date=new Date(day[0])
			now=new Date()
			if day[1]['champions'][data_options.y]['count']<10# or (date.getUTCMonth()!=now.getUTCMonth()|date.getUTCFullYear()!=now.getUTCFullYear())
				continue
			parsed.push({'x':day[0], 'y':Math.round((day[1]['champions'][data_options.y]['won']/day[1]['champions'][data_options.y]['count'])*100)})
	else if data_options.data_parse=='chistorypop'
		for day in data
			if day[1]['champions'][data_options.y]['count']<10
				continue
			parsed.push({'x':day[0], 'y':(day[1]['champions'][data_options.y]['won']/day[1]['count'])*100})

	chart_options['data']=parsed

	Morris.Line(chart_options)

$(document).ready(->
	window.draw_chart=draw_chart
	if window.chart? then draw_chart(window.chart_data, window.chart)
)
