from django.shortcuts import render, redirect
from .models import auth
from django.http import HttpResponse
# Create your views here.

def home_view(request, *args, **kwargs):
    context = {
        'messages': [], 
        'login': False
    }
    if "email" in request.session:
        context['login'] = True
        context['email'] = request.session['email']
    return render(request, "home.html", context)

def login_view(request, *args, **kwargs):
    context = {
        'messages': []
    }
    if request.method == "POST":
        email = request.POST['email'].lower()
        password = request.POST['password']
        objs = auth.objects.all()
        for i in objs:
            if i.email.lower() == email:
                if i.password == password:
                    request.session["email"] = email
                    return redirect("/")
                else:
                    context['messages'].append("Invalid Password for this id")
            else:
                context['messages'].append("Invalid Username and password")

    return render(request, "login.html", context)

def signin_view(request, *args, **kwargs):
    context = {
        'messages': []
    }
    if request.method == "POST":
        obj = request.POST
        auth_ = auth()
        if obj["full_name"].replace(" ", "").isalpha():
            auth_.full_name = obj["full_name"].lower()
        else:
            context["messages"].append("Invalid or Empty Name Field")
        if obj["phone_number"]:
            auth_.phone_number = obj["phone_number"].lower()
        else:
            context["messages"].append("Invalid Phone Number")
        if obj["email"]:
            auth_.email = obj["email"].lower()
            objs = auth.objects.all()
            for i in objs:
                if i.email.lower() == obj["email"].lower():
                    context['messages'].append("Used Email")
                    return render(request, "signup.html", context)
        else:
            context["messages"].append("Invalid email")
        if obj["password"]:
            auth_.password = obj["password"]
        else:
            context["messages"].append("Invalid Password")
        if context['messages']:
            redirect("/login/")
        else:
            auth_.save()        
    return render(request, "signup.html", context)

def logout(request, *args, **kwargs):
    if "email" in request.session:
        del request.session['email']
    return redirect("/")

def bad_request(request, *args, **kwargs):
    return HttpResponse("<h1>Error 400</h1><h3>Bad Request</h3>")

def permission_denied(request, *args, **kwargs):
    return HttpResponse("<h1>Error 403<h3>Permission Denied")

def page_not_found(request, *args, **kwargs):
    return HttpResponse("<h1>Error 404</h1><h3>Page Not Found</h3")

def server_error(request, *args, **kwargs):
    return HttpResponse("<h1>Error 500</h1><h3>Server Error</h3>")