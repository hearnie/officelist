from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render

from forms import GaterangeForm
import eveoffice
from django import forms
from django.http import HttpResponseRedirect

#current root, first search form
def search_form(request):
	return render(request, 'search_form.html')

# first search form result, systems by gate jumps
def result(request):
	if 'target' in request.GET:
		tgt = request.GET['target']
		jumpsObj = eveoffice.SYSlinks()
		jumps = 9
		systemlist = jumpsObj.gatedist(tgt,jumps)
		template = get_template('result.html')
		html = template.render(Context({'jumps':jumps,'tgt':tgt, 'systemlist':systemlist}))
	else:
		message = 'empty form'
	return HttpResponse(html)


# new gaterange result with validation
def search_gaterange(request):
	return render(request, 'search_gaterange.html')
	
	
	

#	maxjumps = 8
#	maxjumps = forms.IntegerField(label='maxjumps', max_value=16, min_value=2, required=False, initial=8)
#	def clean_targetsystem(self):
#		targetsystem = self.cleaned_data['targetsystem']
#		return targetsystem


def gaterange_result(request):
	if 1 == 1:
#	if 'target' in request.GET:
		form = GaterangeForm(request.POST)
		if form.is_valid():			
			jumps = form.cleaned_data['maxjumps']
			jumpsObj = eveoffice.SYSlinks()
			systemlist = jumpsObj.gatedist(form.cleaned_data['target'], jumps)
			template = get_template('gaterange_result.html')
			tgt = form.cleaned_data['target']
			html = template.render(Context({'jumps':jumps,'tgt':tgt, 'systemlist':systemlist}))
			return HttpResponse(html) 
		else:
			jumps = 10
			errors = "Invalid form"
			template = get_template('gaterange_result.html')
			html = template.render(Context({'errors':errors}))
	return HttpResponse(html)
   

#form for searching by cap range
def search_caprange(request):
	
	return render(request, 'search_caprange.html')

#caprange search results
def caprange_result(request):
	if 'target' in request.GET:
		target = request.GET['target']
		jumps = 10
		capObj = eveoffice.RANGElinks()
		caprangelist = capObj.lydist(target)
		template = get_template('caprange_result.html')
		caphtml = template.render(Context({'jumps':jumps, 'target':target, 'caprangelist':caprangelist}))
	else:
		message = 'empty form'
	return HttpResponse(caphtml)





