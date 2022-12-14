from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from .forms import UploadFileForm
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from pdf2docx import Converter




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
            uploaded_file_url = fs.url(filename)
            print(f"myfile: {myfile}")
            print(f"fs: {fs}")
            print(f"filename: {filename}")
            print(f"uploaded_file_url: {uploaded_file_url}")
            docx = '/media/conv.docx'
            cv = Converter(uploaded_file_url)
            cv.convert(docx_file)      
            cv.close()
        else:
            form = UploadFileForm()
        return render(request, 'home.html')
    
    def handle_uploaded_file(self,f):
        with open(f'pdf_ting/pdf_app/media/{f}', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
