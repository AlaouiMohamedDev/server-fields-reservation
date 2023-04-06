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
        'List Photo':'/photo-list/',
        'Get Specific photo':'/photo-Id/<str:pk>/',
        'create Photo':'/photo-create/',
        'update Photo':'/photo-update/<str:pk>/',
        'delete Photo':'/photo-delete/<str:pk>/',
    }
    return Response(api_urls,  status=status.HTTP_200_OK)

#CRUD for COMPLEXE

@api_view(['GET'])
def complexeList(request):
    complexeSportif = ComplexeSportif.objects.all()
    serializer = ComplexeSportifSerializer(complexeSportif, many=True)
    data = {
        'data': serializer.data,
        'message': 'complexe listed successfully',
        'status': 200
    }
    return JsonResponse(data)

@api_view(['GET'])
def complexeId(request,pk):
    complexeSportif = ComplexeSportif.objects.get(id=pk)
    serializer = ComplexeSportifSerializer(complexeSportif, many=False)
    data = {
        'data': serializer.data,
        'message': 'complexe listed successfully',
        'status': 200
    }
    return JsonResponse(data)

@api_view(['POST'])
def complexeCreate(request):
    token = request.data['jwt']
    if not token:
        return JsonResponse(({'message' : 'Only hosts can add complexes','status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Only hosts can add complexes','status':401}))
    if not payload['role']== 'host':
        return JsonResponse(({'message' : 'Only hosts can add complexes','status':401}))
    user = User.objects.get(id=payload['id'])
    request.data['user'] = user.id
    serializer = ComplexeSportifSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        complexe = serializer.save(user=user)
    else:
        return JsonResponse(({'message' : 'Invalid Data','status':400}))
    return JsonResponse(({'message' : 'complexe added successfully','status':200, 'complexe_id': complexe.id}))


@api_view(['POST'])
def complexeUpdate(request,pk):
    user = request.user
    token = request.data['jwt']
    if not token:
        return JsonResponse(({'message' : 'Only hosts can update complexes','status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Only hosts can update complexes','status':401}))
    if not payload['role']== 'host':
        return JsonResponse(({'message' : 'Only hosts can update complexes','status':401}))
    complexeSportif = ComplexeSportif.objects.get(id=pk)
    user = User.objects.get(id=payload['id'])
    request.data['user'] = user.id
    serializer = ComplexeSportifSerializer(instance = complexeSportif,data=request.data,context={'request': request})
    if serializer.is_valid():
        serializer.save(user=user)
    else:
        return JsonResponse(({'message' : 'Invalid Data','status':400}))
    return JsonResponse(({'message' : 'complexe updated succesfully','status':200}))

@api_view(['DELETE'])
def complexeDelete(request,pk):
    token = request.data['jwt']
    if not token:
        return JsonResponse(({'message' : 'Only hosts can delete complexes','status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Only hosts can delete complexes','status':401}))
    if not payload['role']== 'host':
        return JsonResponse(({'message' : 'Only hosts can delete complexes','status':401}))
    complexeSportif = ComplexeSportif.objects.get(id=pk)
    complexeSportif.delete()
    return JsonResponse(({'message' : 'complexe deleted succesfully','status':200}))


#CRUD for fields 

# retourner fields #########################
@api_view(['GET'])
def list_fields(request):
    terrains = Terrain.objects.all()
    data = []
    for terrain in terrains:
        terrain_data = {}
        terrain_data['Field name'] = terrain.name
        terrain_data['Complexe name'] = terrain.category.complexeSportif.name
        terrain_data['price'] = terrain.category.price
        terrain_data['number_of_players'] = terrain.number_of_players
        terrain_data['reserved'] = terrain.is_reserved
        terrain_data['area'] = terrain.category.area
        terrain_data['complex_photo']= terrain.category.complexeSportif.url

        # Photo du terrain
        terrain_photo = terrain.photo_set.first()
        if terrain_photo:
            terrain_data['terrain_photo'] = terrain_photo.url
     

        data.append(terrain_data)

    return Response(data)


#############################################


@api_view(['POST'])

def fieldCreate(request):
    token = request.data['jwt']
    if not token:
        return JsonResponse(({'message' : 'Only hosts can add fields','status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Only hosts can add fields','status':401}))
    if not payload['role']== 'host':
        return JsonResponse(({'message' : 'Only hosts can add fields','status':401}))
    data = request.data['fields']
    for field in data:
        typeTerrain = field['category']
        category = CategoryTerrain.objects.filter(typeTerrain=typeTerrain).first()
        field['category']= category.id
        serializer = TerrainSerializer(data=field)
        if serializer.is_valid():
            serializer.save()
        else:
            return JsonResponse(({'message' : 'Invalid Data','status':400}))
    return JsonResponse(({'message' : 'field created succesfully','status':200}))

@api_view(['POST'])
def fieldUpdate(request,pk):
    token = request.data['jwt']
    if not token:
        return JsonResponse(({'message' : 'Only hosts can update fields','status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Only hosts can update fields','status':401}))
    if not payload['role']== 'host':
        return JsonResponse(({'message' : 'Only hosts can update fields','status':401}))
    terrain = Terrain.objects.get(id=pk)
    serializer = TerrainSerializer(instance = terrain,data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return JsonResponse(({'message' : 'Invalid Data','status':400}))
    return JsonResponse(({'message' : 'field updated succesfully','status':200}))

@api_view(['DELETE'])
def fieldDelete(request,pk):
    token = request.data['jwt']
    if not token:
        return JsonResponse(({'message' : 'Only hosts can delete fields','status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Only hosts can delete fields','status':401}))
    if not payload['role'] == 'host':
        return JsonResponse(({'message' : 'Only hosts can delete fields','status':401}))
    terrain = Terrain.objects.get(id=pk)
    terrain.delete()
    return JsonResponse(({'message' : 'field deleted succesfully','status':200}))

@api_view(['GET'])
def fieldList(request):
    terrain = Terrain.objects.all()
    data = []
    for t in terrain:
        serializer = TerrainSerializer(t)
        photos = Photo.objects.filter(terrain=t)
        photo_serializer = PhotoSerializer(photos, many=True)
        serialized_data = serializer.data
        serialized_data['terrain_photos'] = photo_serializer.data
        data.append({'terrain': serialized_data})
    return JsonResponse({'data': data, 'message': 'field listed successfully', 'status': 200})



@api_view(['GET'])
def fieldId(request, pk):
    terrain = Terrain.objects.get(id=pk)
    serializer = TerrainSerializer(terrain, many=False)
    photos = Photo.objects.filter(terrain=terrain)
    photo_serializer = PhotoSerializer(photos, many=True)
    serialized_data = serializer.data
    serialized_data['terrain_photos'] = photo_serializer.data
    data = {
        'data': serialized_data,
        'message': 'field listed successfully',
        'status': 200
    }
    return JsonResponse(data)






#CRUD for fieldCategory




@api_view(['GET'])
def fieldCategoryList(request):
    categoryTerrain = CategoryTerrain.objects.all()
    serializer = CategoryTerrainSerializer(categoryTerrain, many=True)
    data = {
        'data': serializer.data,
        'message': 'field categories listed successfully',
        'status': 200
    }
    return JsonResponse(data)

@api_view(['GET'])
def fieldCategoryId(request,pk):
    categoryterrain = CategoryTerrain.objects.get(id=pk)
    serializer = CategoryTerrainSerializer(categoryterrain, many=False)
    data = {
        'data': serializer.data,
        'message': 'field categories listed successfully',
        'status': 200
    }
    return JsonResponse(data)


@api_view(['POST'])

def fieldCategoryCreate(request):
    token = request.data['jwt']
    if not token:
        return JsonResponse(({'message' : 'Only hosts can add categories','status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Only hosts can add categories','status':401}))
    if not payload['role']== 'host':
        return JsonResponse(({'message' : 'Only hosts can add categories','status':401}))
    data = request.data['categories']
    for category in data:
        serializer = CategoryTerrainSerializer(data=category)
        if serializer.is_valid():
            serializer.save()
        else:
            return JsonResponse(({'message' : 'Invalid Data','status':400}))
    return JsonResponse(({'message' : 'field category created succesfully','status':200}))
# BetterCode
# data = request.data['categories']
# complexe_id = request.data['complexe_id']
# for category in data:
#     category['complexe_id'] = complexe_id  # Assign the complexe_id field to the category data
#     serializer = CategoryTerrainSerializer(data=category)
#     if serializer.is_valid():
#         serializer.save()
#     else:
#         print(serializer.errors)

# return JsonResponse(({'message' : 'field categories created successfully',
#                 'status':200})) 


@api_view(['POST'])
def fieldCategoryUpdate(request,pk):
    token = request.data['jwt']
    if not token:
        return JsonResponse(({'message' : 'Only hosts can update categories','status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Only hosts can update categories','status':401}))
    if not payload['role']== 'host':
        return JsonResponse(({'message' : 'Only hosts can update categories','status':401}))
    categoryTerrain = CategoryTerrain.objects.get(id=pk)
    serializer = CategoryTerrainSerializer(instance = categoryTerrain,data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return JsonResponse(({'message' : 'Invalid Data','status':400}))
    return JsonResponse(({'message' : 'field category updated succesfully','status':200}))

@api_view(['DELETE'])
def fieldCategoryDelete(request,pk):
    token = request.data['jwt']
    if not token:
        return JsonResponse(({'message' : 'Only hosts can delete categories','status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Only hosts can delete categories','status':401}))
    if not payload['role'] == 'host':
        return JsonResponse(({'message' : 'Only hosts can delete categories','status':401}))
    categoryterrain = CategoryTerrain.objects.get(id=pk)
    categoryterrain.delete()
    return JsonResponse(({'message' : 'field category deleted succesfully','status':200}))



#CRUD for Photo



@api_view(['GET'])
def photoList(request):
    photo = Photo.objects.all()
    serializer =PhotoSerializer(photo, many=True)
    data = {
        'data': serializer.data,
        'message': 'field categories listed successfully',
        'status': 200
    }
    return JsonResponse(data)

@api_view(['GET'])
def photoId(request,pk):
    data = {
        'data': serializer.data,
        'message': 'field categories listed successfully',
        'status': 200
    }
    photo = Photo.objects.get(id=pk)
    serializer = PhotoSerializer(photo, many=False)
    return JsonResponse(data)


@api_view(['POST'])

def photoCreate(request):
    token = request.data['jwt']
    if not token:
        return JsonResponse(({'message' : 'Only hosts can add photos','status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Only hosts can add photos','status':401}))
    if not payload['role']== 'host':
        return JsonResponse(({'message' : 'Only hosts can add photos','status':401}))
    serializer = PhotoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return JsonResponse(({'message' : 'Invalid Data','status':400}))
    return JsonResponse(({'message' : 'field picture created succesfully','status':200}))

@api_view(['POST'])
def photoUpdate(request,pk):
    token = request.data['jwt']
    if not token:
        return JsonResponse(({'message' : 'Only hosts can update photos','status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Only hosts can update photos','status':401}))
    if not payload['role']== 'host':
        return JsonResponse(({'message' : 'Only hosts can update photos','status':401}))
    photo = Photo.objects.get(id=pk)
    serializer = PhotoSerializer(instance = photo,data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return JsonResponse(({'message' : 'Invalid Data','status':400}))
    return JsonResponse(({'message' : 'field picture updated succesfully','status':200}))

@api_view(['DELETE'])
def photoDelete(request,pk):
    token = request.data['jwt']
    if not token:
        return JsonResponse(({'message' : 'Only hosts can delete Photos','status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Only hosts can delete photos','status':401}))
    if not payload['role'] == 'host':
        return JsonResponse(({'message' : 'Only hosts can delete photos','status':401}))
    photo = Photo.objects.get(id=pk)
    photo.delete()
    return JsonResponse(({'message' : 'field picture deleted succesfully','status':200}))

