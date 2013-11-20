from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from api.models import CheckList, CheckListItem


class CheckListItemSerializer(ModelSerializer):
    check_list = PrimaryKeyRelatedField()
    class Meta:
        model = CheckListItem
        fields = ('checked', 'check_list', 'description', 'id', 'title', )


class CheckListSerializer(ModelSerializer):
    check_list_items = CheckListItemSerializer(
            many=True,
            read_only=True,
            )

    class Meta:
        model = CheckList
        fields = ('check_list_items', 'id', 'title', )
