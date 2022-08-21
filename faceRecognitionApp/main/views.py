from django.shortcuts import render

def form(req):
    return render(req, 'form.html')

def register(req):
    return render(req, 'register.html')
