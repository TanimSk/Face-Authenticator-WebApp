from django.shortcuts import render, HttpResponse


def form(req):
    return render(req, 'form.html')


def register(req):
    if req.method == 'POST':
        name = req.POST.get('user')
        email = req.POST.get('email')
        
        print(req.FILES.get('images'), name, email)
        HttpResponse(False)

    return render(req, 'register.html')
