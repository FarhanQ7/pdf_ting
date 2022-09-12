from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from .forms import UploadFileForm

class Home(TemplateView):

    template_name = "home.html"
    @method_decorator(csrf_exempt)
    def post(self,request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            self.handle_uploaded_file(request.FILES['file'])
            print("made it here")
        else:
            form = UploadFileForm()
        return render(request, 'home.html', {'form': form})
    
    def handle_uploaded_file(self,f):
        with open('thing.pdf', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
