from django.shortcuts import render
def index(request):
    return render(request, 'collection/index.html')
# Create your views here.
