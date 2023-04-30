from django.shortcuts import render
from django.http import JsonResponse
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
import jwt
import datetime
from rest_framework.decorators import api_view
# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return JsonResponse(({'message' : 'registered successfully',
                        'status':200}))
        else:
            print(serializer.errors)
            return JsonResponse(({'message' : 'Invalid Credentials',
                    'status':401}))


class GoogleRegister(APIView):
    def post(self, request):
        request.data['password'] = 'dKPH4$0&X3Oy'
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return JsonResponse(({'message' : 'registered successfully',
                        'status':200}))
        else:
            print(serializer.errors)
            return JsonResponse(({'message' : 'Invalid Credentials',
                    'status':401}))
        
class GoogleLogin(APIView):
    def post(self, request):
        email = request.data['email']
        user = User.objects.filter(email=email).first()
        if user is None:
            return JsonResponse(({'message' : 'Invalid Credentials',
                    'status':401}))
        payload = {
            'id': user.id,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=6000),
            'iat':  datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'PLEASE WORK', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
             'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'profile_pic': user.profile_pic,
                'role': user.role
            },
            'message' : 'login successfully',
            'status':200
        }
        return JsonResponse(response.data)
class GoogleAuth(APIView):
    def post(self, request):
        email = request.data['email']
        user = User.objects.filter(email=email).first()

        if user is None:
            # User doesn't exist, register them
            request.data['password'] = 'dKPH4$0&X3Oy'
            serializer = UserSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                user = serializer.instance
            else:
                return JsonResponse({'message': 'Invalid Credentials', 'status': 401})

        # User exists, log them in
        payload = {
            'id': user.id,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=6000),
            'iat':  datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'PLEASE WORK', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
             'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'profile_pic': user.profile_pic,
                'role': user.role
            },
            'message': 'login successfully',
            'status': 200
        }
        return JsonResponse(response.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is None:
            return JsonResponse(({'message' : 'Invalid Credentials',
                    'status':401}))
        if not user.check_password(password):
            return JsonResponse(({'message' : 'Invalid Credentials',
                    'status':401}))
        payload = {
            'id': user.id,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':  datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'PLEASE WORK', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
             'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'profile_pic': user.profile_pic,
                'role': user.role
            },
            'message' : 'login successfully',
            'status':200
        }
        return JsonResponse(response.data)


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            return JsonResponse(({'message' : 'Invalid Credentials',
                    'status':401}))
        try:
            payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse(({'message' : 'Invalid Credentials',
                    'status':401}))
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
class LogoutView(APIView):
    def post(self,request):
        response =Response()
        response.delete_cookie('jwt')
        response.data={
            'message':'Logged out Succesfully','status':200}
        return response


################################ User update
@api_view(['PUT'])
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=404) 
    data = request.data
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'password' in data:
        if user.check_password(data['password']):
            user.save()
            return Response({'message': 'Profile Information updated successfully', 'status':200})
        else:
            return Response({'message': 'Incorrect password', 'status': 400})


@api_view(['POST'])
def update_profile_picture(request):
    token = request.data['jwt']
    if not token:
        return JsonResponse(({'message' : 'Invalid Credentials', 'status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])

    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Invalid Credentials', 'status':401}))
    user = User.objects.filter(id=payload['id']).first()
    profile_picture = request.data['profile_pic']
    print(profile_picture)
    if profile_picture:
        user.profile_pic = profile_picture
        user.save()
        return Response({ 'message': 'Profile picture updated successfully', 'status':200})
    else:
        return Response({'error': 'No profile picture provided.','status':200} )
    