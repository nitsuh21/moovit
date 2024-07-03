from django.shortcuts import render

# Create your views here.
def overview(request):
    if request.method == 'POST':
        print(request.POST)
    else:
        return render(request, 'dashboard/overview.html')