from rest_framework.serializers import ModelSerializer
from base_app.models import GatheringFake

class TestDataSerializer(ModelSerializer):
    class Meta:
        model = GatheringFake
        fields = '__all__'