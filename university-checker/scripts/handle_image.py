#обработчик изображений, который принимеат файл и сохраняет куда надшо

import os



def handle_uploaded_file(f, slug):
    print(os.getcwd())
    print(os.pardir)
    os.chdir(".")
    with open(rf'{os.getcwd()}/media/services_images/{slug}.png', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)