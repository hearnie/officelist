from django import forms

class GaterangeForm(forms.Form):
	target = forms.CharField(max_length=20, label='target')
	maxjumps = forms.IntegerField(label='maxjumps', max_value=16, min_value=2)
	

		
#	def system_lookup(self):
#		targetsystemclean = self.cleaned_data['targetsystem']
#		SystemObject = eveoffice.SYSlinks()
#		targetoutput = SystemObject.sysID(targetsystem)
#		return (targetoutput,maxjumps)
		
