from django.shortcuts import render

def index(request):
    return render(
        request,
        "index.html",
        {
            "title": "Пример",
        },
    )

def test(request):
    return render(request, "test.html")
