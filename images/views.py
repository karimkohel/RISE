from django.shortcuts import render
from .models import Image
from django.views.generic.list import ListView

# Create your views here.
def homeView(request):
    return render(request, 'images/index.html')


class ImageListView(ListView):
    model = Image
    context_object_name = 'images'
    paginate_by = 20
    template_name = 'images/index.html'

    # TODO: after implementing the search algorithm use it here
    # def get_queryset(self):
    #     return object_list