from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render

from forms import *
import eveoffice
from django import forms



def search_gaterange(request):
	try:
		current_system = request.META['HTTP_EVE_SOLARSYSTEMNAME']
	except:
		current_system = ""
	template = get_template('search_gaterange.html')
	html = template.render(Context({'current_system':current_system}))
	return HttpResponse(html)


def gaterange_result(request):

	form = GaterangeForm(request.GET)
	if form.is_valid():			
		jumps = form.cleaned_data['maxjumps']
		jumpsObj = eveoffice.SystemLinks()
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
   

def search_caprange(request):
	try:
		current_system = request.META['HTTP_EVE_SOLARSYSTEMNAME']
	except:
		current_system = ""
	template = get_template('search_caprange.html')
	html = template.render(Context({'current_system':current_system}))
	return HttpResponse(html)



#caprange search results
def caprange_result(request):
	form = CaprangeForm(request.GET)
	if form.is_valid():
		target = form.cleaned_data['target']
		resultcount = form.cleaned_data['resultcount']
		capObj = eveoffice.RangeLinks()
		caprangelist = capObj.lydist(target,resultcount)
		template = get_template('caprange_result.html')
		caphtml = template.render(Context({'resultcount':resultcount, 'target':target, 'caprangelist':caprangelist}))
	else:
		message = 'empty form'
		template = get_template('caprange_result.html')
		caphtml = template.render(Context({'target':form}))
	return HttpResponse(caphtml) 


def igb(request):
	current_system = ""
	try:
		current_system = request.META['HTTP_EVE_SOLARSYSTEMNAME']
		trusted = request.META['HTTP_EVE_TRUSTED']

	except KeyError:
		trusted = "No"
	template = get_template('igb.html')
	html = template.render(Context({'trusted':trusted, 'current_system':current_system}))
	return HttpResponse(html)



