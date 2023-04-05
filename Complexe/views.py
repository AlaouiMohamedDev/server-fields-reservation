from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from requests import Response
from .models import ComplexeSportif
from .serializers import complexSerializer
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['POST'])
def complexCreate(request):
   serializer = complexSerializer(data=request.data)
   if serializer.is_valid():
       serializer.save()
   return JsonResponse(serializer.data, safe=False)

@api_view(['DELETE'])
def complexDelete(request,pk):
   complexes = ComplexeSportif.objects.get(id=pk)
   complexes.delete()
   return JsonResponse('Item is deleted', safe=False)

@api_view(['POST'])
def complexUpdate(request,pk):
   complexes = ComplexeSportif.objects.get(id=pk)
   serializer = complexSerializer(instance=complexes,data=request.data)
   if serializer.is_valid():
       serializer.save()
   return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def complexDetails(request, pk):
    complexes = ComplexeSportif.objects.get(id=pk)
    serializer = complexSerializer(complexes,many=False)
    return JsonResponse(serializer.data, safe=False)
   







       








