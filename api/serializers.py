from .models import Group, Device
from rest_framework import serializers

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields ="__all__"
        
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields ="__all__"