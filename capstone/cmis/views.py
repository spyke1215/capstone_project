from django.shortcuts import render

# Create your views here.
def index (request):
    return render(request,'cmis/index.html')

def menu (request):
    return render(request,'cmis/menu.html')

