from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from api.models import Post, User, Comment, Reply
from api.serializers import PostSerializer, UserSerializer, CommentSerializer, ReplySerializer

from django.core.files.storage import default_storage

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from rest_framework import generics


# Create your views here.
# post views .
@csrf_exempt
def postApi(request,id=0):
    if request.method=='GET':
        posts = Post.objects.filter(is_draft = True)
        posts_serializer = PostSerializer(posts, many=True)
        return JsonResponse(posts_serializer.data, safe=False)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.filter(is_draft = True)
    serializer_class = PostSerializer

#comments CRUD
@csrf_exempt
def commentApi(request,id=0):
    if request.method=='GET':
        comments = Comment.objects.all()
        comments_serializer = CommentSerializer(comments, many=True)
        return JsonResponse(comments_serializer.data, safe=False)

    elif request.method=='POST':
        comment_data=JSONParser().parse(request)
        comment_serializer = CommentSerializer(data=comment_data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)

#     elif request.method=='PUT':
#         comment_data = JSONParser().parse(request)
#         comment=comments.objects.get(commentId=comment_data['commentId'])
#         comment_serializer=CommentSerializer(comment,data=comment_data)
#         if comment_serializer.is_valid():
#             comment_serializer.save()
#             return JsonResponse("Updated Successfully!!", safe=False)
#         return JsonResponse("Failed to Update.", safe=False)

#     elif request.method=='DELETE':
#         comment=comments.objects.get(commentId=id)
#         comment.delete()
#         return JsonResponse("Deleted Succeffully!!", safe=False)

@csrf_exempt
def replyApi(request,id=0):
    if request.method=='GET':
        replys = Reply.objects.all()
        replys_serializer = ReplySerializer(replys, many=True)
        return JsonResponse(replys_serializer.data, safe=False)

    elif request.method=='POST':
        reply_data=JSONParser().parse(request)
        reply_serializer = ReplySerializer(data=reply_data)
        if reply_serializer.is_valid():
            reply_serializer.save()
            return JsonResponse("Added Successfully!!" , safe=False)
        return JsonResponse("Failed to Add.",safe=False)


#reagister API
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
#Login API (post)
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found!')
        # if not user.check_password(password):
        #     raise AuthenticationFailed('Incorrect password!')
        if not User.objects.filter(password=password).first():
            raise AuthenticationFailed('Incorrect password!')
        payload = {
            'id': user.id, #store the user id
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60), #set how this token will existe (1h)
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response
#User get last login
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
#Logout
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response