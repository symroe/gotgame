from django.views.generic import TemplateView


class ApiExplorerView(TemplateView):
    """
        Shows the Api Explorer.
    """
    template_name = 'admin/api/api_explorer.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ApiExplorerView, self).get_context_data(*args, **kwargs)

        # getting base url
        context['base_url'] = self.request.build_absolute_uri('/api/v1/')
        return context
