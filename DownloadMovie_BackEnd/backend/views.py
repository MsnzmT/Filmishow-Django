from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as lgn, logout as lgout
from .forms import SignUpForm


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponse('User created successfully!')

        return HttpResponse(f"{form.errors}")

    return HttpResponse('Only post method allowed!')


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            lgn(request, user)
            return HttpResponse('Login Successfully')
        else:
            return HttpResponse('Login Failed - Your password or username is wrong')
    else:
        return HttpResponse('request method not allowed !')


@csrf_exempt
def logout(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            lgout(request)
            return HttpResponse('You were loged out seccessfully !')
        return HttpResponse('You should login first !')
    return HttpResponse('Request method not allowed !')


