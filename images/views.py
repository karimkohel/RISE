from django.urls import reverse_lazy
from .models import Image
from django.views.generic.edit import CreateView
from .forms import ImageForm
from .searcher import search
from django.conf import settings

class ImageListView(CreateView):
    model = Image
    form_class = ImageForm
    template_name = 'images/index.html'
    success_url = reverse_lazy("images:index")

    def get_context_data(self, **kwargs):
        context = super(ImageListView, self).get_context_data(**kwargs)
        context['images'] = Image.objects.all()[:20]
        print(Image.objects.last().image_file)
        # context['images'] = search(ImageForm.cleaned_data[], "indexing.csv", 20)
        return context
