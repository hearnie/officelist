from django import forms

class GaterangeForm(forms.Form):
	target = forms.CharField(max_length=20, label='target')
	maxjumps = forms.IntegerField(label='maxjumps', max_value=16, min_value=2)

class CaprangeForm(forms.Form):
	target = forms.CharField(max_length=20, label='target')
	resultcount = forms.IntegerField(label='maxjumps', max_value=100, min_value=1)
	

		
