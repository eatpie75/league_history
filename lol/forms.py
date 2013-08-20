from django import forms
from models import MAPS, MODES

class MapModeForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(MapModeForm, self).__init__(*args, **kwargs)
		self.elo_filter=kwargs.get('elo_filter', 0)
	maps=[(-1, 'All maps'),]
	maps.extend(MAPS)
	modes=[(-1, 'All modes'),]
	modes.extend(MODES)
	game_map=forms.ChoiceField(required=False, choices=maps[:-1], widget=forms.Select(attrs={'class':'form-control input-sm'}))
	game_mode=forms.ChoiceField(required=False, choices=modes[:-1], widget=forms.Select(attrs={'class':'form-control input-sm'}))
	elo_filter=forms.ChoiceField(required=False, choices=((-1, 'All'), (0, 'Bronze league'), (1, 'Silver league'), (2, 'Gold league'), (3, 'Platinum league')), widget=forms.Select(attrs={'class':'col-md-2'}))
