from rest_framework import serializers

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model=User

        fields=["id","username","password","email"]

        read_only_fields=["id"]

        
    def  create(self, validated_data):
        
        return User.objects.create_user(**validated_data)
     