from django.shortcuts import render

# Create your views here.
def create_order(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'create.html')