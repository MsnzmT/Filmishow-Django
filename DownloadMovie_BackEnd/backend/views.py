from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView


class SignUp(APIView):
    def post(self, request):
        username = request.data['username']
        pass1 = request.data['password1']
        pass2 = request.data['password2']
        email = request.data['email']
        full_name = request.data['full_name']
        users = CustomUser.objects.filter(username=username)
        if users.exists():
            return Response(status=status.HTTP_409_CONFLICT)
        if pass2 != pass1:
            return Response({'message': 'Entered passwords are not identical'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            CustomUser.objects.create_user(username=username, password=pass1, email=email,
                                           full_name=full_name)
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)


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
                films = Film.objects.filter(genres__name='horror')
            elif request.path == '/category/action/':
                films = Film.objects.filter(genres__name='action')
            elif request.path == '/category/comedy/':
                films = Film.objects.filter(genres__name='comedy')
            elif request.path == '/category/fantasy/':
                films = Film.objects.filter(genres__name='fantasy')
            elif request.path == '/category/drum/':
                films = Film.objects.filter(genres__name='drum')
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


class Arrival(APIView):
    def get(self, request):
        films = ArrivalFilm.objects.all()
        serializer = ArrivalSerializer(films, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikeComment(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, comment_id):
        liked_comment = CommentLike.objects.filter(comment_id=comment_id).filter(user_id=request.user.id)
        disliked_comment = CommentDislike.objects.filter(comment_id=comment_id).filter(user_id=request.user.id)
        if (not liked_comment.exists()) and (not disliked_comment.exists()):
            comment1 = get_object_or_404(Comment, id=comment_id)
            comment1.like += 1
            comment1.save()
            like = CommentLike()
            like.user_id = request.user.id
            like.comment_id = comment_id
            like.save()
            return Response(status=status.HTTP_200_OK)
        elif (not liked_comment.exists()) and (disliked_comment.exists()):
            comment2 = get_object_or_404(Comment, id=comment_id)
            comment2.dislike -= 1
            comment2.like += 1
            comment2.save()
            like = CommentLike()
            disliked_comment.delete()
            like.user_id = request.user.id
            like.comment_id = comment_id
            like.save()
            return Response(status=status.HTTP_200_OK)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


class EmailVerification(CreateAPIView):
    serializer_class = EmailSerializer


class CodeValidate(CreateAPIView):
    serializer_class = EmailCodeSerializer


class DislikeComment(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, comment_id):
        liked_comment = CommentLike.objects.filter(comment_id=comment_id).filter(user_id=request.user.id)
        disliked_comment = CommentDislike.objects.filter(comment_id=comment_id).filter(user_id=request.user.id)

        if (not liked_comment.exists()) and (not disliked_comment.exists()):
            comment1 = get_object_or_404(Comment, id=comment_id)
            comment1.dislike += 1
            comment1.save()
            like = CommentDislike()
            like.user_id = request.user.id
            like.comment_id = comment_id
            like.save()
            return Response(status=status.HTTP_200_OK)
        elif (liked_comment.exists()) and (not disliked_comment.exists()):
            comment2 = get_object_or_404(Comment, id=comment_id)
            comment2.dislike += 1
            comment2.like -= 1
            comment2.save()
            like = CommentDislike()
            liked_comment.delete()
            like.user_id = request.user.id
            like.comment_id = comment_id
            like.save()
            return Response(status=status.HTTP_200_OK)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class AddFavorite(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, film_id):
        film = get_object_or_404(Film, id=film_id)
        favorited_film = Favorite.objects.filter(user_id=request.user.id).filter(film_id=film_id)
        if favorited_film.exists():
            favorited_film.delete()
            return Response(status.HTTP_205_RESET_CONTENT)
        favorite = Favorite()
        favorite.user_id = request.user.id
        favorite.film_id = film_id
        favorite.film_eName = film.eName
        favorite.film_pName = film.pName
        favorite.film_photo = film.photo
        favorite.film_group = film.group
        favorite.save()
        return Response(status=status.HTTP_200_OK)


class GetFavorites(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        film_ids = Favorite.objects.filter(user_id=request.user.id)
        serializer = FavoriteSerializer(film_ids, many=True)
        return Response(serializer.data)


class LikeFilm(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, film_id):
        liked_film = FilmLike.objects.filter(film_id=film_id).filter(user_id=request.user.id)
        disliked_film = FilmDislike.objects.filter(film_id=film_id).filter(user_id=request.user.id)
        if (not liked_film.exists()) and (not disliked_film.exists()):
            film1 = get_object_or_404(Film, id=film_id)
            film1.like += 1
            film1.save()
            like = FilmLike()
            like.user_id = request.user.id
            like.film_id = film_id
            like.save()
            return Response(status=status.HTTP_200_OK)
        elif (not liked_film.exists()) and (disliked_film.exists()):
            film2 = get_object_or_404(Film, id=film_id)
            film2.dislike -= 1
            film2.like += 1
            film2.save()
            like = FilmLike()
            disliked_film.delete()
            like.user_id = request.user.id
            like.film_id = film_id
            like.save()
            return Response(status=status.HTTP_200_OK)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


class DislikeFilm(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, film_id):
        liked_film = FilmLike.objects.filter(film_id=film_id).filter(user_id=request.user.id)
        disliked_film = FilmDislike.objects.filter(film_id=film_id).filter(user_id=request.user.id)
        if (not liked_film.exists()) and (not disliked_film.exists()):
            film1 = get_object_or_404(Film, id=film_id)
            film1.dislike += 1
            film1.save()
            dislike = FilmDislike()
            dislike.user_id = request.user.id
            dislike.film_id = film_id
            dislike.save()
            return Response(status=status.HTTP_200_OK)
        elif (liked_film.exists()) and (not disliked_film.exists()):
            film2 = get_object_or_404(Film, id=film_id)
            film2.dislike += 1
            film2.like -= 1
            film2.save()
            like = FilmDislike()
            liked_film.delete()
            like.user_id = request.user.id
            like.film_id = film_id
            like.save()
            return Response(status=status.HTTP_200_OK)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
