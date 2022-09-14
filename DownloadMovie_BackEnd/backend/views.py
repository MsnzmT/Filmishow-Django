from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class SignUp(APIView):
    def post(self, request):
        username = request.data['username']
        pass1 = request.data['password1']
        pass2 = request.data['password2']
        email = request.data['email']
        # first_name = request.data['first_name']
        # last_name = request.data['last_name']
        full_name = request.data['full_name']
        # country = request.data['country']
        # phone_number = request.data['phone_number']
        if pass2 != pass1:
            return Response({'message': 'Entered passwords are not identical'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            CustomUser.objects.create_user(username=username, password=pass1, email=email,
                                           full_name=full_name)
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)


class LogOut(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, requset):
        requset.user.auth_token.delete()
        return Response({'message': 'Logged out successfully!'}, status=status.HTTP_200_OK)


class AllFilms(APIView):
    def get(self, request):
        films = Film.objects.all()
        serializer = FilmSerializer(films, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UploadFilm(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        serializer = FilmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Film uploaded successfully !'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class AddComment(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, film_id):
        text = request.query_params.get('text')
        film = get_object_or_404(Film, id=film_id)
        comment = Comment()
        comment.film = film
        comment.text = text
        user_name = request.user
        user = get_object_or_404(CustomUser, username=user_name)
        comment.commenter = user
        comment.save()
        serializer = FilmSerializer(film)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FilterFilms(APIView):
    def get(self, request):
        try:
            if request.path == '/category/horror/':
                films = Film.objects.filter(genres__name='ترسناک')
            elif request.path == '/category/action/':
                films = Film.objects.filter(genres__name='اکشن')
            elif request.path == '/category/comedy/':
                films = Film.objects.filter(genres__name='کمدی')
            elif request.path == '/category/fantasy/':
                films = Film.objects.filter(genres__name='فانتزی')
            elif request.path == '/category/drum/':
                films = Film.objects.filter(genres__name='درام')
        except Film.DoesNotExist:
            return Response({'message': '404 not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FilmSerializer(films, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchFilmName(APIView):
    def get(self, request):
        film_name = request.query_params.get('name')
        film = get_object_or_404(Film, eName=film_name)
        serializer = IdSerializer(film)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchFilmId(APIView):
    def get(self, request, film_id):
        film = get_object_or_404(Film, id=film_id)
        serializer = FilmSerializer(film)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutJWT(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)