draw_chart=(data, y='rating', aoptions={}, data_parse='default', container='elo-graph')->
	# console.log data
	defaults={
		element:container
		xkey:'x'
		ykeys:'y'
		labels:['ELO']
		ymax:'auto'
		ymin:'auto'
		# smooth:false
		hideHover:true
		lineColors: ['#3269b4', '#C0D800', '#CB4B4B', '#4DA74D', '#9440ED']
		# subtitle:'ELO GRAPH'
		# # fontColor:'#fff'
		# shadowSize:0
		# xaxis: {
		# 	mode:'time'
		# 	noTicks:10
		# 	# showLabels:false
		# }
		# yaxis: {
		# 	autoscale: true
		# 	autoscaleMargin:1
		# 	# showLabels:false
		# 	# tickFormatter:(num)->"#{num}%"
		# }
		# mouse: {
		# 	track:true
		# 	trackFormatter:(obj)->"#{Flotr.Date.format(obj.x, '%y-%m-%d')}: #{Math.round(obj.y)}"
		# 	sensiblility:3
		# 	lineColor:'#fff'
		# 	relative:true
		# }
		# lines: {
		# 	fill:true
		# 	show:true
		# }
		# points: {
		# 	show:true
		# 	lineWidth:1
		# 	radius:2
		# 	fillColor:'#9D261D'
		# }
		# grid: {
		# 	color:'#000'
		# 	verticalLines:false
		# 	# horizontalLines:false
		# 	outline:''
		# }
	}

	options=$.extend({}, defaults)
	$.extend(true, options, aoptions)
	parsed=[]
	# console.log options

	if data_parse=='default'
		for day in data
			if day[1][y]<10
				continue
			parsed.push({'x':day[0], 'y':day[1][y]})
	else if data_parse=='chistorywr'
		for day in data
			date=new Date(day[0])
			now=new Date()
			if day[1]['champions'][y]['count']<10# or (date.getUTCMonth()!=now.getUTCMonth()|date.getUTCFullYear()!=now.getUTCFullYear())
				continue
			parsed.push({'x':day[0], 'y':Math.round((day[1]['champions'][y]['won']/day[1]['champions'][y]['count'])*100)})
	else if data_parse=='chistorypop'
		for day in data
			if day[1]['champions'][y]['count']<10
				continue
			parsed.push({'x':day[0], 'y':(day[1]['champions'][y]['won']/day[1]['count'])*100})

	options['data']=parsed

	Morris.Line(options)

$(document).ready(->
	window.draw_chart=draw_chart
	if window.chart? then draw_chart(window.chart_data, window.chart)
)
