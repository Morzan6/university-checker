#обработчик изображений, который принимеат файл и сохраняет куда надшо

def handle_uploaded_file(f, slug):
    with open(f'media/services_images/{slug}.png', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)