from .models import Apply, Job, User
from rest_framework.serializers import ModelSerializer

class ApplySerializer(ModelSerializer):
    class Meta:
        model = Apply
        fields = '__all__'
        
class JobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields= '__all__'
        
class UserSerializer(ModelSerializer):
    class Meta:
        model= User
        fields ='__all__'
        
