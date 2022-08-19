from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as lgn, logout as lgout
from .forms import SignUpForm
from .models import Film, Comment


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


@csrf_exempt
def upload_film(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user.is_superuser:
                film = Film()
                film.name = request.POST.get('name')
                film.summary = request.POST.get('summary')
                film.genre = request.POST.get('genre')
                film.director = request.POST.get('director')
                film.actors = request.POST.get('actors')
                film.country = request.POST.get('country')
                film.yearOfPublication = request.POST.get('yearOfPublication')
                film.photo = request.POST.get('photo')
                film.save()
                return HttpResponse('Film uploaded successfully !')
            return HttpResponse('You should be admin !')
        return HttpResponse('You should login first !')
    return HttpResponse('Request method not allowed !')


@csrf_exempt
def show_all_film(request):
    if request.method == 'GET':
        films = Film.objects.all().values_list('name', 'photo')
        return HttpResponse(films)
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
