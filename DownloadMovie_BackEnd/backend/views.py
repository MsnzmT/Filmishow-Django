from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as lgn, logout as lgout
from .models import *
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from .forms import *


@csrf_exempt
def signup(request):
    if request.method == 'GET':
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})
    elif request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pass1 = form.cleaned_data['password1']
            pass2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            country = form.cleaned_data['country']
            phone_number = form.cleaned_data['phone_number']
            if pass2 != pass1:
                return HttpResponse('Entered passwords are not identical')
            else:
                CustomUser.objects.create_user(username=username, password=pass1, email=email,
                                               first_name=first_name, last_name=last_name,
                                               country=country, phone_number=phone_number)
                return HttpResponse('User created successfully!')
    else:
        return HttpResponse('Only post method allowed!')


@csrf_exempt
def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

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
    if request.method == 'GET':
        if request.user.is_authenticated:
            lgout(request)
            return HttpResponse('You were loged out seccessfully !')
        return HttpResponse('You should login first !')
    return HttpResponse('Request method not allowed !')


@permission_required('backend.add_film', raise_exception=True)
@csrf_exempt
def upload_film(request):
    if request.method == 'GET':
        form = UploadFilmForm()
        return render(request, 'upload_film.html', {'form': form})
    elif request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                form = UploadFilmForm(request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponse('Film uploaded successfully !')
            return HttpResponse('You should be admin !')
        return HttpResponse('You should login first !')
    return HttpResponse('Request method not allowed !')


@csrf_exempt
def show_all_film(request):
    if request.method == 'GET':
        films = Film.objects.all()
        return render(request, 'film_detail.html', {'films': films})
    return HttpResponse('Request method not allowed !')


@csrf_exempt
def add_comment(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            comment = Comment()
            # choose film
            film_name = request.POST.get('film')
            film = Film.objects.get(name=film_name)
            comment.film = film
            # find commenter
            comment.commenter = request.user
            comment.text = request.POST.get('text')
            comment.save()
            return HttpResponse('Your comment added successfully !')
        return HttpResponse('You should login first !')
    return HttpResponse('Request method not allowed !')


@csrf_exempt
def filter_films(request):
    if request.path == '/category/horror/':
        films = Film.objects.filter(genre='H').values_list('name', 'photo')
        return HttpResponse(films)
    elif request.path == '/category/action/':
        films = Film.objects.filter(genre='A').values_list('name', 'photo')
        return HttpResponse(films)
    elif request.path == '/category/comedy/':
        films = Film.objects.filter(genre='C').values_list('name', 'photo')
        return HttpResponse(films)
    elif request.path == '/category/fantasy/':
        films = Film.objects.filter(genre='F').values_list('name', 'photo')
        return HttpResponse(films)
    elif request.path == '/category/drum/':
        films = Film.objects.filter(genre='D').values_list('name', 'photo')
        return HttpResponse(films)


@csrf_exempt
def search_film(request):
    if request.method == "GET":
        film_name = request.GET.get('film_name')
        try:
            film = Film.objects.get(name=film_name)
        except Film.DoesNotExist:
            return HttpResponse('404 Not Found', status=404)
        return HttpResponse(film)
    return HttpResponse('Request method not allowed !')
