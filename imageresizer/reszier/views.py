from django.shortcuts import render
from django.http import HttpResponse
from .forms import ResizeForm
from PIL import Image
from io import BytesIO

def index(request):
    if request.method == 'POST':
        form = ResizeForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image']
            width = form.cleaned_data['width']
            height = form.cleaned_data['height']

            img = Image.open(image_file)
            img = img.resize((width, height), Image.Resampling.LANCZOS)

            buffer = BytesIO()
            img_format = 'JPEG' if img.mode in ('RGB', 'L') else 'PNG'
            img.save(buffer, format=img_format)
            buffer.seek(0)

            response = HttpResponse(buffer.read(), content_type=f'image/{img_format.lower()}')
            response['Content-Disposition'] = f'attachment; filename="resized_{width}x{height}.{img_format.lower()}"'
            return response
    else:
        form = ResizeForm()

    return render(request, 'index.html', {'form': form})

