from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.files.storage import default_storage
import img2pdf
from PIL import Image
import io
import os
from docx2pdf import convert
import pdfkit

def convert_to_pdf(request):
    if request.method == 'POST':
        file = request.FILES.get('document')

        if file is None:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        if file.content_type.startswith('image/'):
            # Handle image file conversion to PDF
            pdf_buffer = convert_image_to_pdf(file)
        elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            # Handle document file conversion to PDF
            pdf_buffer = convert_document_to_pdf(file)
        else:
            return JsonResponse({'error': 'Unsupported file format'}, status=400)

        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="converted.pdf"'
        return response
    else:
        return JsonResponse({'error': 'Invalid request'}, status=405)


def convert_image_to_pdf(image_file):
    image = Image.open(image_file)
    pdf_buffer = img2pdf.convert(image.filename)
    return pdf_buffer


def convert_document_to_pdf(document_file):
    file_name = default_storage.save(document_file.name, document_file)
    file_path = default_storage.path(file_name)

    output_path = '/path/to/temp/output.pdf'

    # Convert the document to PDF
    convert(file_path, output_path)

    with open(output_path, 'rb') as f:
        pdf_buffer = f.read()

    os.remove(file_path)
    os.remove(output_path)

    return pdf_buffer


def index(request):
    return render(request, 'converter/pdfconverter.html')
