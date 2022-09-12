from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from .forms import UploadFileForm
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class Home(TemplateView):

    template_name = "home.html"
    @method_decorator(csrf_exempt)
    def post(self,request):
        if request.method == 'POST':
#             form = UploadFileForm(request.POST, request.FILES)
#             print(request.FILES['myfile'])
#             self.handle_uploaded_file(request.FILES.get('myfile', False))
#             print("made it here")
            myfile = request.FILES.get('myfile', False)
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
        else:
            form = UploadFileForm()
        return render(request, 'home.html')
    
    def handle_uploaded_file(self,f):
        with open(f'pdf_ting/pdf_app/media/{f}', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
