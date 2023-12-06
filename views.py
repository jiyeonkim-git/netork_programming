import logging
from django.views.generic.base import TemplateView

logger = logging.getLogger('mylogger')


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['apps'] = ['polls', 'books']
        return context
