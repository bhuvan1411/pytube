from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from videos.models import Video

@login_required
def home_view(request):
    return render(request, 'home/home.html')

def home_view(request):
    return render(request, 'home/home.html')

def search_view(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Video.objects.filter(title__icontains=query)
    return render(request, 'home/search_results.html', {'query': query, 'results': results})
