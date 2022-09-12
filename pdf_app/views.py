from django.views.generic import TemplateView

class Home(TemplateView):
    permission_classes = (permissions.AllowAny,)
    template_name = "home.html"
