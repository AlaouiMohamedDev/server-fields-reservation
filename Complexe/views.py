from datetime import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .serializers import ComplexeSportifSerializer,TerrainSerializer,CategoryTerrainSerializer,PhotoSerializer,ReservationSerializer,PostSerializer
from .models import ComplexeSportif,Terrain,CategoryTerrain,Photo,Reservation,Post,Joined,Ville
import jwt
from rest_framework.decorators import api_view
from users.models import User
from .serializers import ReservationSerializer,JoinedSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import Group
import requests
from bs4 import BeautifulSoup


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
        '__________________________':'__________________________',
        'List Reservation':'/reservation-list/',
        'Get Specific Reservation':'/reservation-Id/<str:pk>/',
        'create Reservation':'/reservation-create/',
        'update Reservation':'/reservation-update/<str:pk>/',
        'delete Reservation':'/reservation-delete/<str:pk>/',
        '__________________________':'__________________________',
        'List Post':'/post-list/',
        'Get Specific Post':'/post-Id/<str:pk>/',
        'create Post':'/post-create/',
        'update Post':'/post-update/<str:pk>/',
        'delete Post':'/post-delete/<str:pk>/',
        'Decrement number of players needed': 'decrementPlayersNeeded/<str:pk>/'
    }
    return Response(api_urls,  status=status.HTTP_200_OK)
#Crud for Reservations
@api_view(['GET'])
def reservationList(request):
    reservations = Reservation.objects.all()
    data = []
    for reservation in reservations:
        day_name = reservation.date.strftime('%A')
        terrain_photo_url = reservation.terrain.photo_set.first().url
        reservation = {
            'id':reservation.id,
            'idField':reservation.terrain.id,
            'date': reservation.date,
            'day': day_name,
            'from': reservation.startTime,
            'to': reservation.endTime,
            'name': reservation.user.first_name,
            'userId': reservation.user.id,
            'terrain': terrain_photo_url,
            'complexe': reservation.terrain.category.complexeSportif.url,
            'complexeName' :reservation.terrain.category.complexeSportif.name,
            'address': reservation.terrain.category.complexeSportif.adresse,
            'price': reservation.terrain.category.price,
            'nameField': reservation.terrain.name,
            'owner':reservation.terrain.category.complexeSportif.user.id,
            'approved':reservation.approved_rejected
        }
        data.append(reservation)
    return JsonResponse(data[::-1], safe=False)
@api_view(['GET'])
def reservationId(request,pk):
    reservation = Reservation.objects.get(id=pk)
    serializer = ReservationSerializer(reservation, many=False)
    data = {
        'data': serializer.data,
        'message': 'reservation listed successfully',
        'status': 200
    }
    return JsonResponse(data)

@api_view(['POST'])
def reservationCreate(request):
    token = request.data['jwt']
    payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    user = User.objects.get(id=payload['id'])
    request.data['user'] = user.id
    serializer = ReservationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        reservation = serializer.save(user=user)
        data = {
            'reservation_id': reservation.id,
            'message': 'Reservation added successfully',
            'status': 200
        }
        return JsonResponse(data)
    else:
        return JsonResponse(({'message' : 'You cant book a field right now','status':400}))
@api_view(['POST'])
def reservationUpdate(request,pk):
    reservation = Reservation.objects.get(id=pk)
    serializer = ReservationSerializer(instance=reservation, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
    else:
        return JsonResponse(({'message' : 'Invalid Data','status':400}))
    return JsonResponse(({'message' : 'reservation updated successfully','status':200}))
@api_view(['DELETE'])
def reservationDelete(request,pk):
    reservation = Reservation.objects.get(id=pk)
    reservation.delete()
    return JsonResponse(({'message' : 'reservation deleted successfully','status':200}))
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
    print(request.data)
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


@api_view(['GET'])
def complexe_sportif_utilisateur(request, utilisateur_id):
    complexes = ComplexeSportif.objects.filter(user=utilisateur_id)
    data = []
    for complexe in complexes:
        complexe_data = {
            'id': complexe.id,
            'name': complexe.name,
            'adresse': complexe.adresse,
            'lattitude': complexe.lattitude,
            'longtitude': complexe.longtitude,
            'description': complexe.description,
            'zone': complexe.zone.id,
            'user': complexe.user.id,
            'url': complexe.url
        }
        data.append(complexe_data)
    return Response(data)

#CRUD for fields 

@api_view(['GET'])
def complex_terrains(request, complex_id):

    complexe = ComplexeSportif.objects.get(id=complex_id)
    terrains = Terrain.objects.filter(category__complexeSportif=complexe)

    data = []
    for terrain in terrains:
        terrain_data = {}
        terrain_data['id'] = terrain.id
        terrain_data['Fieldname'] = terrain.name
        terrain_data['Complexename'] = terrain.category.complexeSportif.name
        terrain_data['address'] = terrain.category.complexeSportif.adresse
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

# retourner fields #########################
@api_view(['GET'])
def list_fields(request):
    terrains = Terrain.objects.all()
    data = []
    for terrain in terrains:
        terrain_data = {}
        terrain_data['id'] = terrain.id
        terrain_data['Fieldname'] = terrain.name
        terrain_data['Complexename'] = terrain.category.complexeSportif.name
        terrain_data['address'] = terrain.category.complexeSportif.adresse
        terrain_data['lat'] = terrain.category.complexeSportif.lattitude
        terrain_data['long'] = terrain.category.complexeSportif.longtitude
        terrain_data['price'] = terrain.category.price
        terrain_data['number_of_players'] = terrain.number_of_players
        terrain_data['reserved'] = terrain.is_reserved
        terrain_data['area'] = terrain.category.area
        terrain_data['complex_photo']= terrain.category.complexeSportif.url
        terrain_data['user_is_active'] = terrain.category.complexeSportif.user.is_active
        terrain_data['city'] = terrain.category.complexeSportif.zone.ville.name
        #category only first letter
        terrain_data['category'] = int(terrain.category.typeTerrain[0])
        # Photo du terrain
        terrain_photo = terrain.photo_set.first()
        if terrain_photo:
            terrain_data['terrain_photo'] = terrain_photo.url
     

        data.append(terrain_data)

    return Response(data)


#api to get first letter of category
@api_view(['GET'])
def list_categories_FL(request):
    categories = CategoryTerrain.objects.all()
    data = []
    for category in categories:
        category_data = {}
        category_data['id'] = category.id
        category_data['typeTerrain'] = category.typeTerrain[0]
        data.append(category_data)

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
        category = CategoryTerrain.objects.filter(typeTerrain=typeTerrain).last()
        field['category']= category.id
        serializer = TerrainSerializer(data=field)
        if serializer.is_valid():
            terrain = serializer.save()
            photo_data = {'url': field['url'], 'terrain': terrain.id}
            photo_serializer = PhotoSerializer(data=photo_data)
            if photo_serializer.is_valid():
                photo_serializer.save()
            else:
                terrain.delete()
                return JsonResponse(({'message': 'Invalid photo data', 'status': 400}))
        else:
            return JsonResponse(({'message' : 'Invalid Terrain Data','status':400}))
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

#CRUD for Post
# user name / terrain name/image  image complexe  reservation object
@api_view(['GET'])
def postList(request):
    posts = Post.objects.all()
    data = []
    for post in posts:
        reservation = Reservation.objects.filter(post=post).first()
        terrain = post.terrain
        complexe = terrain.category.complexeSportif
        user = post.user
        # Photo du terrain
        terrain_photo = terrain.photo_set.first()
        if terrain_photo:
            terrain_photo = terrain_photo.url
        complexe_image = complexe.url if complexe else None
        reservation_data = ReservationSerializer(reservation, many=False).data if reservation else None
        joinList = Joined.objects.filter(post=post)
        userJoined=[]
        for j in joinList:
            userJoined.append(j.user.id)
        post_data = {
            'id': post.id,
            'description': post.description,
            'maxPlayers' : terrain.number_of_players,
            'neededPlayers' : post.number_of_players_needed,
            'date': post.date,
            'userId': user.id,
            'user_name': user.first_name + ' ' + user.last_name,
            'userImage':user.profile_pic,
            'terrain_photo': terrain_photo,
            'terrain_name': terrain.name,
            'complexe_image': complexe_image,
            'reservation': reservation_data,
            'joined':userJoined
        }
        data.append(post_data)
    return JsonResponse({'data': data[::-1]})
@api_view(['GET'])
def postId(request,pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    data = {
        'data': serializer.data,
        'message': 'field post listed successfully',
        'status': 200
    }
    return JsonResponse(data)


@api_view(['POST'])
def postCreate(request):
    token = request.data['jwt']
    print(token)
    if not token:
        return JsonResponse(({'message' : 'Invalid Credentials', 'status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])

    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Invalid Credentials', 'status':401}))
    print(payload['id'])
    user = User.objects.filter(id=payload['id']).first()

    request.data['user'] = user.id
    request.data['date'] = datetime.now()
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(({'message' : 'post created successfully', 'status':200}))
    else:
        return JsonResponse(({'message' : 'Invalid Data', 'status':400}))
@api_view(['POST'])
def postUpdate(request,pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(instance = post,data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return JsonResponse(({'message' : 'Invalid Data','status':400}))
    return JsonResponse(({'message' : 'field post updated succesfully','status':200}))
@api_view(['DELETE'])
def postDelete(request,pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return JsonResponse(({'message' : 'field post deleted succesfully','status':200}))






############################# Reservation Apis ########################################

@api_view(['GET'])
def reservations(request):
    reservations = Reservation.objects.order_by('-id')
    data = []
    for res in reservations:
        data.append({
            'id': res.id,
            'date': res.date,
            'startTime': res.startTime,
            'endTime': res.endTime,
            'user_last_name': res.user.last_name,
            'user_first_name': res.user.first_name,
            'terrain': res.terrain.name,
            'approved_rejected': res.approved_rejected,
        })
    return Response(data)

@api_view(['GET'])
def completedReservations(request):
    reservations = Reservation.objects.filter(post__number_of_players_needed=0)
    reservations1 = Reservation.objects.filter(post=None)
    data = []
    for reservation in reservations:
        if reservation.approved_rejected == 'waiting':
            day_name = reservation.date.strftime('%A')
            terrain_photo_url = reservation.terrain.photo_set.first().url
            reservation = {
                'id':reservation.id,
                'idField':reservation.terrain.id,
                'date': reservation.date,
                'day': day_name,
                'from': reservation.startTime,
                'to': reservation.endTime,
                'name': reservation.user.first_name,
                'userId': reservation.user.id,
                'terrain': terrain_photo_url,
                'complexe': reservation.terrain.category.complexeSportif.url,
                'address': reservation.terrain.category.complexeSportif.adresse,
                'price': reservation.terrain.category.price,
                'nameField': reservation.terrain.name,
                'owner':reservation.terrain.category.complexeSportif.user.id,
            }
            data.append(reservation)
    for reservation in reservations1:
        if reservation.approved_rejected == 'waiting':
            day_name = reservation.date.strftime('%A')
            terrain_photo_url = reservation.terrain.photo_set.first().url
            reservation = {
                'id':reservation.id,
                'idField':reservation.terrain.id,
                'date': reservation.date,
                'day': day_name,
                'from': reservation.startTime,
                'to': reservation.endTime,
                'name': reservation.user.first_name,
                'userId': reservation.user.id,
                'terrain': terrain_photo_url,
                'complexe': reservation.terrain.category.complexeSportif.url,
                'address': reservation.terrain.category.complexeSportif.adresse,
                'price': reservation.terrain.category.price,
                'nameField': reservation.terrain.name,
                'owner':reservation.terrain.category.complexeSportif.user.id,
            }
            data.append(reservation)
     # Order the data in decreasing order with respect to the 'id' field
    data = sorted(data, key=lambda k: k['id'], reverse=True)

    return JsonResponse({'data':data})

@api_view(['GET'])
def fullReservations(request):
    reservations = Reservation.objects.filter(post=None)
    serializer = ReservationSerializer(reservations, many=True)
    data = {
        'data': serializer.data,
        'message': 'Unassigned reservations listed successfully',
        'status': 200
    }
    return JsonResponse(data)



def check_reservation_status(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return JsonResponse({'message': 'Reservation not found', 'status': 404})

    if reservation.approved_rejected == 'approved':
        return JsonResponse({'message': 'approved', 'status': 400})
    elif reservation.approved_rejected == 'rejected':
        return JsonResponse({'message': 'rejected', 'status': 400})
    else:
        return JsonResponse({'message': 'Status unknown', 'status': 400})

@api_view(['POST'])
def approveReservation(request):
    reservation_id = request.data.get('reservation_id')
    status = request.data.get('status')
    if not reservation_id:
        return JsonResponse({'message': 'Reservation id not provided', 'status': 400})
    if not status:
        return JsonResponse({'message': 'Status not provided', 'status': 400})
    if status not in ['approved', 'rejected', 'waiting']:
        return JsonResponse({'message': 'Invalid status provided', 'status': 400})
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return JsonResponse({'message': 'Reservation not found', 'status': 404})
    reservation.approved_rejected = status
    reservation.save()
    return JsonResponse({'message': 'Reservation status updated successfully', 'status': 200})


#List all reservations with their status
@api_view(['GET'])
def reservationsStatus(request):
    reservations = Reservation.objects.filter(post__number_of_players_needed=0)
    reservations1 = Reservation.objects.filter(post=None)
    data = []
    for reservation in reservations:
        day_name = reservation.date.strftime('%A')
        terrain_photo_url = reservation.terrain.photo_set.first()
        if terrain_photo_url:
            terrain_photo_url = terrain_photo_url.url
        reservation = {
            'id':reservation.id,
            'idField':reservation.terrain.id,
            'date': reservation.date,
            'day': day_name,
            'from': reservation.startTime,
            'to': reservation.endTime,
            'name': reservation.user.first_name,
            'userId': reservation.user.id,
            'terrain': terrain_photo_url,
            'complexe': reservation.terrain.category.complexeSportif.url,
            'complexeName' :reservation.terrain.category.complexeSportif.name,
            'address': reservation.terrain.category.complexeSportif.adresse,
            'price': reservation.terrain.category.price,
            'nameField': reservation.terrain.name,
            'owner':reservation.terrain.category.complexeSportif.user.id,
            'status': reservation.approved_rejected
        }
        data.append(reservation)
    for reservation in reservations1:
        day_name = reservation.date.strftime('%A')
        terrain_photo_url = reservation.terrain.photo_set.first()
        if terrain_photo_url:
            terrain_photo_url = terrain_photo_url.url
        reservation = {
            'id':reservation.id,
            'idField':reservation.terrain.id,
            'date': reservation.date,
            'day': day_name,
            'from': reservation.startTime,
            'to': reservation.endTime,
            'name': reservation.user.first_name,
            'userId': reservation.user.id,
            'terrain': terrain_photo_url,
            'complexe': reservation.terrain.category.complexeSportif.url,
            'address': reservation.terrain.category.complexeSportif.adresse,
            'price': reservation.terrain.category.price,
            'nameField': reservation.terrain.name,
            'owner':reservation.terrain.category.complexeSportif.user.id,
            'status': reservation.approved_rejected
        }
        data.append(reservation)
        data = sorted(data, key=lambda k: k['id'], reverse=True)

    return JsonResponse({'data':data})

@api_view(['GET'])
def listJoined(request):
    listjoined = Joined.objects.order_by('-id')
    data = []
    for joined in listjoined:
        reservation = Reservation.objects.filter(post=joined.post.id)
        serializer = ReservationSerializer(reservation, many=True)
        data.append({
        'id': joined.id,
        'owner': joined.post.user.id,
        'user': joined.user.id,
        'ownerImage' : joined.post.user.profile_pic,
        'ownerFirstName':joined.post.user.first_name,
        'ownerLastName':joined.post.user.last_name,
        'reservation': serializer.data[0]['date'],
        'userFirstName':joined.user.first_name,
        'userLastName':joined.user.last_name,
        'userImage':joined.user.profile_pic,
        'postid':joined.post.id,
        'field':joined.post.terrain.name,
        'request':joined.accepted
        })
    return JsonResponse({"data":data})


@api_view(['POST'])
def joinMatch(request):
    token = request.data['jwt']
    if not token:
        return JsonResponse(({'message' : 'Invalid Credentials', 'status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Invalid Credentials', 'status':401}))

    serializer = JoinedSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(({'message' : 'Request to joined created successfully', 'status':200}))
    else:
        return JsonResponse(({'message' : 'Invalid Data', 'status':400}))
    


@api_view(['POST'])
def decrementPlayersNeeded(request,pk):
    token = request.data['jwt']
    if not token:
        return JsonResponse(({'message' : 'Invalid Credentials', 'status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Invalid Credentials', 'status':401}))
    post = Post.objects.get(id=pk)
    if not post:
        return JsonResponse(({'message' : 'Post not found', 'status':404}))
    if post.number_of_players_needed <= 0:
        return JsonResponse(({'message' : 'No more players needed', 'status':400}))
    
    post.number_of_players_needed -= 1
    post.save()

    joinId = request.data['joinId']
    join = Joined.objects.get(id=joinId)

    join.accepted = "Accepted"
    join.save()

    if post.number_of_players_needed == 0:
        joindList = Joined.objects.filter(post=post.id)
        for ele in joindList:
            if ele.accepted != "Accepted":
                ele.accepted = "Rejected"
                ele.save()
                
    

    return JsonResponse(({'message' : 'Request accepted successfully', 'status':200}))





@api_view(['POST'])
def rejectPlayer(request,pk):
    token = request.data['jwt']
    if not token:
        return JsonResponse(({'message' : 'Invalid Credentials', 'status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Invalid Credentials', 'status':401}))
   
    joinId = request.data['joinId']
    join = Joined.objects.get(id=joinId)

    join.accepted = "Rejected"
    join.save()
    
    return JsonResponse(({'message' : 'Request rejected successfully', 'status':200}))


## approve user "host"
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_host(request, user_id):
    if not request.user.groups.filter(name='admin').exists():
        return Response({'message': 'Only admins can approve user accounts','status':404})
    try:
        user = User.objects.get(id=user_id, is_active=False, groups__name='host')
    except User.DoesNotExist:
        return Response({'message': 'User not found or account is already approved','status':404})
    
    approved_hosts_group, created = Group.objects.get_or_create(name='approved_hosts')
    user.groups.add(approved_hosts_group)
    
    user.is_active = True
    user.save()
    
    return Response({'message': 'User account has been approved','status':200})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_host(request, user_id):
    if not request.user.groups.filter(name='admin').exists():
        return Response({'message': 'Only admins can approve user accounts','status':404})
    try:
        user = User.objects.get(id=user_id, is_active=False, groups__name='host')
    except User.DoesNotExist:
        return Response({'message': 'User not found or account is already approved','status':404})
    
    approved_hosts_group, created = Group.objects.get_or_create(name='approved_hosts')
    user.groups.add(approved_hosts_group)
    
    user.is_active = False
    user.save()
    
    return Response({'message': 'User account has been approved','status':200})

@api_view(['POST'])
def approveHosts(request,user_id):
    token = request.data['jwt']
    if not token:
        print('hi token')
        return JsonResponse(({'message' : 'Only hosts can add photos','status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Only hosts can add photos','status':401}))
    if not payload['role']== 'admin':
        print('hi role')
        return JsonResponse(({'message' : 'Only hosts can add photos','status':401}))
    user = User.objects.get(id=user_id)
    if not user:
        print('hi user')
        return JsonResponse(({'message' : 'User not found','status':404}))
    user.is_active = True
    user.save()
    return JsonResponse(({'message' : 'User approved successfully','status':200}))

@api_view(['POST'])
def rejectHosts(request,user_id):
    token = request.data['jwt']
    if not token:
        return JsonResponse(({'message' : 'Only hosts can add photos','status':401}))
    try:
        payload = jwt.decode(token,'PLEASE WORK',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return JsonResponse(({'message' : 'Only hosts can add photos','status':401}))
    if not payload['role']== 'admin':
        return JsonResponse(({'message' : 'Only hosts can add photos','status':401}))
    user = User.objects.get(id=user_id)
    if not user:
        return JsonResponse(({'message' : 'User not found','status':404}))
    user.is_active = False
    user.save()
    return JsonResponse(({'message' : 'User approved successfully','status':200}))

##api to count number of reservations and cities and complexes
@api_view(['GET'])
def getStats(request):
    reservations = Reservation.objects.all()
    reservationsCount = len(reservations)
    cities = Ville.objects.all()
    citiesCount = len(cities)
    complexes = ComplexeSportif.objects.all()
    complexesCount = len(complexes)
    return JsonResponse(({'reservationsCount' : reservationsCount,'citiesCount':citiesCount,'complexesCount':complexesCount,'status':200}))




@api_view(['GET'])
def getCititesScraping(request):
    url = "https://profilbaru.com/article/List_of_cities_in_Morocco"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find('table', {'class': 'wikitable sortable'})
    rows = table.find_all("tr")
    cityList = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 2:
            first_cell = cells[1].text.strip()
            first_cell = first_cell.split("[")[0].strip()
            cityList.append(first_cell)
    return JsonResponse(({'cities' : cityList,'status':200}))