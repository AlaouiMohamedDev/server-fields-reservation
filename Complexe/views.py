from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.exceptions import AuthenticationFailed
from .serializers import ComplexeSportifSerializer,TerrainSerializer,CategoryTerrainSerializer,PhotoSerializer
from .models import ComplexeSportif,Terrain,CategoryTerrain,Photo
import jwt
from rest_framework.decorators import api_view
from users.models import User
# Create your views here.
@api_view(['GET'])
def apiOverview(request):
    api_urls={
        'List Complexe':'/complexe-list/',
        'Get Specific Complexe':'/complexe-Id/<str:pk>/',
        'create Complexe':'/complexe-create/',
        'update Complexe':'/complexe-update/<str:pk>/',
        'delete Complexe':'/complexe-delete/<str:pk>/',
        '__________________________':'__________________________',
        'List Field':'/field-list/',
        'Get Specific Field':'/field-Id/<str:pk>/',
        'create Field':'/field-create/',
        'update Field':'/field-update/<str:pk>/',
        'delete Field':'/field-delete/<str:pk>/',
        '__________________________':'__________________________',
        'List Field Category':'/fieldCategory-list/',
        'Get Specific Field Category':'/fieldCategory-Id/<str:pk>/',
        'create Field Category':'/fieldCategory-create/',
        'update Field Category':'/fieldCategory-update/<str:pk>/',
        'delete Field Category':'/fieldCategory-delete/<str:pk>/',
        '__________________________':'__________________________',
        'List Photo':'/field-list/',
        'Get Specific photo':'/field-Id/<str:pk>/',
        'create Photo':'/photo-create/',
        'update Photo':'/photo-update/<str:pk>/',
        'delete Photo':'/photo-delete/<str:pk>/',
    }
    return Response(api_urls,  status=status.HTTP_200_OK)

#CRUD for COMPLEXE

@api_view(['GET'])
def complexeList(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can add list sportifs.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role']== 'host':
        return Response({'error': 'Only hosts can add list sportifs.'},status.HTTP_401_UNAUTHORIZED)
    complexeSportif = ComplexeSportif.objects.all()
    serializer = ComplexeSportifSerializer(complexeSportif, many=True)
    return JsonResponse(({'message' : 'complexe retrieved',
                    'status':200}))

@api_view(['GET'])
def complexeId(request,pk):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can get complexe sportifs.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role']== 'host':
        return Response({'error': 'Only hosts can get complexe sportifs.'},status.HTTP_401_UNAUTHORIZED)
    complexeSportif = ComplexeSportif.objects.get(id=pk)
    serializer = ComplexeSportifSerializer(complexeSportif, many=False)
    return JsonResponse(({'message' : 'complexe retrieved',
                    'status':200}))

@api_view(['POST'])
def complexeCreate(request):
    token = request.data['jwt']
    if not token:
        return Response({'error': 'Only hosts can add complexe sportifs.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role']== 'host':
        return Response({'error': 'Only hosts can add complexe sportifs.'},status.HTTP_401_UNAUTHORIZED )
    user = User.objects.get(id=payload['id'])
    request.data['user'] = user.id
    serializer = ComplexeSportifSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(user=user)
    else:
        print(serializer.errors)
    return JsonResponse(({'message' : 'complexe added successfully',
                    'status':200}))


@api_view(['POST'])
def complexeUpdate(request,pk):
    user = request.user
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can add complexe sportifs.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role']== 'host':
        return Response({'error': 'Only hosts can add complexe sportifs.'},status.HTTP_401_UNAUTHORIZED)
    complexeSportif = ComplexeSportif.objects.get(id=pk)
    user = User.objects.get(id=payload['id'])
    request.data['user'] = user.id
    serializer = ComplexeSportifSerializer(instance = complexeSportif,data=request.data,context={'request': request})
    if serializer.is_valid():
        serializer.save(user=user)
    return JsonResponse(({'message' : 'complexe updated succesfully',
                    'status':200}))

@api_view(['DELETE'])
def complexeDelete(request,pk):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can add complexe sportifs.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role']== 'host':
        return Response({'error': 'Only hosts can add complexe sportifs.'},status.HTTP_401_UNAUTHORIZED)
    complexeSportif = ComplexeSportif.objects.get(id=pk)
    complexeSportif.delete()
    return JsonResponse(({'message' : 'complexe deleted succesfully',
                    'status':200}))


#CRUD for fields 



@api_view(['POST'])

def fieldCreate(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can add fields.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role']== 'host':
        return Response({'error': 'Only hosts can add fields.'},status.HTTP_401_UNAUTHORIZED)
    serializer = TerrainSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return JsonResponse(({'message' : 'field created succesfully',
                    'status':200}))

@api_view(['POST'])
def fieldUpdate(request,pk):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can update fields.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role']== 'host':
        return Response({'error': 'Only hosts can update fields.'},status.HTTP_401_UNAUTHORIZED)
    terrain = Terrain.objects.get(id=pk)
    serializer = TerrainSerializer(instance = terrain,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return JsonResponse(({'message' : 'field updated succesfully',
                    'status':200}))

@api_view(['DELETE'])
def fieldDelete(request,pk):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can delete fields.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role'] == 'host':
        return Response({'error': 'Only hosts can delete fields.'},status.HTTP_401_UNAUTHORIZED)
    terrain = Terrain.objects.get(id=pk)
    terrain.delete()
    return JsonResponse(({'message' : 'field deleted succesfully',
                    'status':200}))

@api_view(['GET'])
def fieldList(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can list fields.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role'] == 'host':
        return Response({'error': 'Only hosts can list fields.'},status.HTTP_401_UNAUTHORIZED)
    terrain = Terrain.objects.all()
    serializer = TerrainSerializer(terrain, many=True)
    return JsonResponse(({'message' : 'field retrieved succesfully',
                    'status':200}))

@api_view(['GET'])
def fieldId(request,pk):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can get a field.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role']== 'host':
        return Response({'error': 'Only hosts can get a field.'},status.HTTP_401_UNAUTHORIZED)
    terrain = Terrain.objects.get(id=pk)
    serializer = TerrainSerializer(terrain, many=False)
    return JsonResponse(({'message' : 'field retrieved succesfully',
                    'status':200}))





#CRUD for fieldCategory




@api_view(['GET'])
def fieldCategoryList(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can list field categories.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role'] == 'host':
        return Response({'error': 'Only hosts can list fields.'},status.HTTP_401_UNAUTHORIZED)
    categoryTerrain = CategoryTerrain.objects.all()
    serializer = CategoryTerrainSerializer(categoryTerrain, many=True)
    return JsonResponse(({'message' : 'field categories retrieved succesfully',
                    'status':200}))

@api_view(['GET'])
def fieldCategoryId(request,pk):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can get a field categories.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role']== 'host':
        return Response({'error': 'Only hosts can get a field.'},status.HTTP_401_UNAUTHORIZED)
    categoryterrain = CategoryTerrain.objects.get(id=pk)
    serializer = CategoryTerrainSerializer(categoryterrain, many=False)
    return JsonResponse(({'message' : 'field category retrieved succesfully',
                    'status':200}))


@api_view(['POST'])

def fieldCategoryCreate(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can add field categories.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role']== 'host':
        return Response({'error': 'Only hosts can add fields.'},status.HTTP_401_UNAUTHORIZED)
    serializer = CategoryTerrainSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
    return JsonResponse(({'message' : 'field category created succesfully',
                    'status':200}))

@api_view(['POST'])
def fieldCategoryUpdate(request,pk):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can update field Categories.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role']== 'host':
        return Response({'error': 'Only hosts can update field Categories.'},status.HTTP_401_UNAUTHORIZED)
    categoryTerrain = CategoryTerrain.objects.get(id=pk)
    serializer = CategoryTerrainSerializer(instance = categoryTerrain,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return JsonResponse(({'message' : 'field category updated succesfully',
                    'status':200}))

@api_view(['DELETE'])
def fieldCategoryDelete(request,pk):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can delete field Categories.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role'] == 'host':
        return Response({'error': 'Only hosts can delete field Categories.'},status.HTTP_401_UNAUTHORIZED)
    categoryterrain = CategoryTerrain.objects.get(id=pk)
    categoryterrain.delete()
    return JsonResponse(({'message' : 'field category deleted succesfully',
                    'status':200}))





#CRUD for Photo




@api_view(['GET'])
def photoList(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can list picutres.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role'] == 'host':
        return Response({'error': 'Only hosts can list pictures.'},status.HTTP_401_UNAUTHORIZED)
    photo = Photo.objects.all()
    serializer =PhotoSerializer(photo, many=True)
    return JsonResponse(({'message' : 'field pictures retrieved succesfully',
                    'status':200}))

@api_view(['GET'])
def photoId(request,pk):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can get a picture.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role']== 'host':
        return Response({'error': 'Only hosts can get a picutre.'},status.HTTP_401_UNAUTHORIZED)
    photo = Photo.objects.get(id=pk)
    serializer = PhotoSerializer(photo, many=False)
    return JsonResponse(({'message' : 'field picture retrieved succesfully',
                    'status':200}))


@api_view(['POST'])

def photoCreate(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can add picutes.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role']== 'host':
        return Response({'error': 'Only hosts can add picutes.'},status.HTTP_401_UNAUTHORIZED)
    serializer = PhotoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return JsonResponse(({'message' : 'field picture created succesfully',
                    'status':200}))

@api_view(['POST'])
def photoUpdate(request,pk):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can update picutes.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role']== 'host':
        return Response({'error': 'Only hosts can update pictures.'},status.HTTP_401_UNAUTHORIZED)
    photo = Photo.objects.get(id=pk)
    serializer = PhotoSerializer(instance = photo,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return JsonResponse(({'message' : 'field picture updated succesfully',
                    'status':200}))

@api_view(['DELETE'])
def photoDelete(request,pk):
    token = request.COOKIES.get('jwt')
    if not token:
        return Response({'error': 'Only hosts can delete pictures.'},status.HTTP_401_UNAUTHORIZED)
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated')
    if not payload['role'] == 'host':
        return Response({'error': 'Only hosts can delete pictures.'},status.HTTP_401_UNAUTHORIZED)
    photo = Photo.objects.get(id=pk)
    photo.delete()
    return JsonResponse(({'message' : 'field picture deleted succesfully',
                    'status':200}))
