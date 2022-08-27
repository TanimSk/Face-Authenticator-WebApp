from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect
from django.template.loader import render_to_string
from .models import *
from PIL import Image
from . import face_recognize
from datetime import datetime, date
from pytz import timezone
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

        # Target image
        target_img = Image.open(
            req.FILES.get('img')
        )

        # Reference image
        ref_imgs = user.user_images.all()
        for ref_img in ref_imgs:
            new_ref_img = Image.open(ref_img.image)

            # Comparing images and Logging
            if face_recognize.compare(target_img, new_ref_img):
                
                now_time = datetime.now(timezone('Asia/Dhaka'))
                join_in = Timing.objects.get(name='main').time_in
                delta_time = (datetime.combine(now_time.today(), join_in).replace(tzinfo=timezone('Asia/Dhaka')) - now_time).total_seconds()
                user_log = Log(name=user.name, user=user)
                user_log.late_join = True if delta_time < 0 else False
                user_log.save()

                # Save into Session
                req.session['is_signed_in'] = 'Y'
                req.session['user_id'] = user_log.id
                req.session['user_name'] = ref_img.user.name
                req.session['user_email'] = ref_img.user.email

                return HttpResponse(json.dumps(
                    {
                        'stat': 'is_user',
                        'content': render_to_string('signout.html', {
                            'name': ref_img.user.name,
                            'email': ref_img.user.email
                        }, request=req)
                    }
                ))

        # Couldn't match image
        return HttpResponse(json.dumps(
            {
                'stat': 'face_unmatched'
            }
        ))

    if req.session.get('is_signed_in', None) == 'Y':
        return render(req, 'signout.html', {
            'name': req.session.get('user_name', 'Somethings Wrong'),
            'email': req.session.get('user_email', 'Somethings Wrong')
        })
    
    else:
        return render(req, 'form.html')


def sign_out(req):
    if req.method == 'POST':

        req.session['is_signed_in'] = 'N'
        user_id = req.session.get('user_id', '')

        # Getting signout time and duration
        signout_time = datetime.now(timezone('Asia/Dhaka'))
        user_log = Log.objects.get(id=user_id)
        delta_time = signout_time - user_log.time_in
        delta_time = round((delta_time.total_seconds() / 3600), 3)
        
        # Checking late or not
        leave_time = Timing.objects.get(name='main').time_out
        
        if ((datetime.combine(signout_time.today(), leave_time).replace(tzinfo=timezone('Asia/Dhaka')) - signout_time).total_seconds() < 0):
            user_log.late_leave = True
        else:
             user_log.late_leave = False

        # Storing user log to DB
        user_log.time_out = signout_time
        user_log.total_hours = delta_time
        user_log.save()

        return redirect('/')

    return HttpResponse('Invalid Request')


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


@login_required(login_url='/admin/')
def dashboard(req):
    user_logs = Log.objects.all()
    return render(req, 'dashboard.html', {'logs': user_logs})
