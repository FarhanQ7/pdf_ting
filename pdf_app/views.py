from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt, csrf_protect

class Home(TemplateView):

    template_name = "home.html"
    @csrf_exempt
    def upload_file(self,request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES['file'])
                return HttpResponseRedirect('/success/url/')
        else:
            form = UploadFileForm()
        return render(request, 'upload.html', {'form': form})
