from django.shortcuts import render

from api.serializers import UserSerializer

from rest_framework.views import APIView

from rest_framework.response import Response

# Create your views here.
class UserCreationView(APIView):

    def post(self,request,*args,**kwargs):

        serializer_instance=UserSerializer(data=request.data)

        if serializer_instance.is_valid():

            serializer_instance.save()

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)