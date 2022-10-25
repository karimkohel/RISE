from django.urls import reverse_lazy
from .models import Image
from django.views.generic.edit import CreateView
from .forms import ImageForm

class ImageListView(CreateView):
    model = Image
    form_class = ImageForm
    template_name = 'images/index.html'
    success_url = reverse_lazy("images:index")

    def get_context_data(self, **kwargs):
        context = super(ImageListView, self).get_context_data(**kwargs)
        context['images'] = self.model.objects.all()[:20]
        return context
