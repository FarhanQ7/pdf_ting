# pdfconverter/converter/urls.py
from django.urls import path
from .views import convert_to_pdf, index

app_name = 'converter'

urlpatterns = [
    path('convert-to-pdf/', convert_to_pdf, name='convert_to_pdf'),
    path('', index, name='index'),
]

