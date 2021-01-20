from django import forms

class TruckDetailForm(forms.Form):
	truck_key = forms.IntegerField()