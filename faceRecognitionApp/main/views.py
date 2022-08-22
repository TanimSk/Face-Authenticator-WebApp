from django.shortcuts import render, HttpResponse
from .models import Registered_user, User_image

def form(req):
    return render(req, 'form.html')


def register(req):
    if req.method == 'POST':
        name = req.POST.get('user')
        email = req.POST.get('email')
        
        user_instance = Registered_user(name=name, email=email)
        User_image(image=None, user=user_instance).save()
        user_instance.save()

        print(req.FILES.get('images'), name, email)
        HttpResponse(False)

    return render(req, 'register.html')
