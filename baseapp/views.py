from django.shortcuts import render, render_to_response
from django.template.context import RequestContext

def index(request):
    return render_to_response('baseapp/index.html')
