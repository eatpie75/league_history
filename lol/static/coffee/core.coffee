$(document).ready(->
	measure_popover=(tip, el)->
		el=$(el)
		tip=$(tip)
		scroll=window.scrollY
		offset=el.offset().top-scroll
		tip.css('display', 'none').appendTo(document.body)
		[height, width]=[tip.height(), tip.width()]
		tip.remove()
		if offset-height>=0
			return 'top'
		else
			return 'bottom'
	window.connect_items=->
		$('div.item.sprite,img.item.sprite').each(->
			el=$(@)
			item=window.items[el.data('item').slice(1)]
			el.popover({
				'html':true
				'content':item.description
				'title':item.name
				'placement':measure_popover
				'trigger':'hover'
				'animation':false
			})
		)
	window.connect_items()
)
