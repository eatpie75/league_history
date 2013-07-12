from django_jinja.base import Library
from lol.core.runes import RUNES, RUNE_STATS

register = Library()


@register.filter
def rune_summary(runepage):
	def _format(page):
		for stat, amount in page['stats'].iteritems():
			if amount<1.0:
				page['stats'][stat]=round(amount, 2)
			elif 1.0<=amount<=10.0:
				page['stats'][stat]=round(amount, 1)
			else:
				page['stats'][stat]=int(round(amount))
			if page['stats'][stat]%1==0:
				page['stats'][stat]=int(page['stats'][stat])
		return page
	presum=[]
	for page in runepage:
		tmp={'stats':{}, 'runes':{}}
		# print page
		if len(page['slots'])==0:
			continue
		name=page['name']
		tmp['name']=name
		tmp['id']=page['id']
		tmp['active']=page.get('active') if page.get('active')!=None else False
		for slot in page['slots']:
			rune=RUNES[slot['id']]
			if slot['id'] not in tmp['runes']:
				tmp['runes'][slot['id']]={
					'name':rune['name'],
					'count':0
				}
			tmp['runes'][slot['id']]['count']+=1
			for effect in rune['effect']:
				stat=effect['stat']
				if stat not in tmp['stats']:
					tmp['stats'][stat]=0.0
				tmp['stats'][stat]+=effect['amount']
		presum.append(tmp)
	map(_format, presum)
	return presum


@register.filter
def rune_stat_str(id):
	return RUNE_STATS[id]
