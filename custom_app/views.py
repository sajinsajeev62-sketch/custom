from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required


@login_required
def welcome(request):
    return render(request, 'first.html')
