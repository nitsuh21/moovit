from django.shortcuts import render

# Create your views here.
def create(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'create.html')