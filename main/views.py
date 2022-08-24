from django.shortcuts import render, HttpResponse
from .models import RegisteredUser, UserImage, Log
from PIL import Image
from . import face_recognize
import json


def form(req):
    if req.method == 'POST':

        email = req.POST.get('email')
        user = RegisteredUser.objects.filter(email=email).first()

        if user is None:
            return HttpResponse(json.dumps(
            {
                'stat': 'not_user'
            }
        ))

        Log(name=user.name).save()

        # Target image
        target_img = Image.open(
            req.FILES.get('img')
        )

        # Reference image
        ref_imgs = user.user_images.all()
        for ref_img in ref_imgs:
            new_ref_img = Image.open(ref_img.image)

            # Comparing images
            if face_recognize.compare(target_img, new_ref_img):
                # print(ref_img.user)
                return HttpResponse(json.dumps(
                    {
                        'stat': 'is_user',
                        'name': ref_img.user.name,
                        'email': ref_img.user.email
                    }
                ))

        return HttpResponse(json.dumps(
            {
                'stat': 'face_unmatched'
            }
        ))

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

        return HttpResponse(json.dumps(
            {
                'stat': True
            }
        ))

    return render(req, 'register.html')
