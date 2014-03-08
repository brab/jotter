from django.contrib.auth.models import User

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


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', )
        write_only_fields = ('password', )

    def restore_object(self, attrs, instance=None):
        """
        Instantiate a new User instance
        """
        if instance is None:
            user = User(
                    email=attrs['email'],
                    username=attrs['username'],
                    )
            user.set_password(attrs['password'])
            return user
        return instance
