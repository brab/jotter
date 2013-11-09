from rest_framework.serializers import ModelSerializer

from api.models import CheckList


class CheckListSerializer(ModelSerializer):
    class Meta:
        model = CheckList
        fields = ('id', 'title', )
