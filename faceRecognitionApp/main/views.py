from django.shortcuts import render, HttpResponse
from .models import RegisteredUser, UserImage
from PIL import Image
from . import face_recognize
import json


def form(req):
    if req.method == 'POST':
        # Target image
        img = req.FILES.get('img')
        target_img = Image.open(img)

        # Reference image
        ref_imgs = UserImage.objects.all()
        for ref_img in ref_imgs:
            new_ref_img = Image.open(ref_img.image)

            # Comparing images
            if face_recognize.compare(target_img, new_ref_img):
                # print(ref_img.user)
                return HttpResponse(json.dumps(
                    {
                        'stat': True,
                        'name': ref_img.user.name,
                        'email': ref_img.user.email
                    }
                ))

            else:
                return HttpResponse(json.dumps(
                    {
                        'stat': False
                    }
                ))

        return HttpResponse(False)

    return render(req, 'form.html')


def register(req):
    if req.method == 'POST':
        name = req.POST.get('user')
        email = req.POST.get('email')
        imgs = req.FILES.getlist('images')

        user_instance = RegisteredUser(name=name, email=email)
        user_instance.save()

        for img in imgs:
            UserImage(image=img, user=user_instance).save()

        return HttpResponse(False)

    return render(req, 'register.html')
