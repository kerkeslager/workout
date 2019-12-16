from django.views.generic.base import TemplateView
from django.shortcuts import render

from base import view_utils

@view_utils.require_auth
def home(request):
    return render(request, 'home.html')
