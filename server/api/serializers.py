"""
Serializers Module
"""
from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from api.models import Budget, BudgetCategory, BudgetExpense, CheckList, \
        CheckListItem


class BudgetExpenseSerializer(ModelSerializer):
    """
    Serializer for the BudgetExpense model
    """
    budget_category = PrimaryKeyRelatedField()

    class Meta(type):
        """
        Meta
        """
        model = BudgetExpense
        fields = ('id', 'budget_category', 'title', 'amount', 'created', )


class BudgetCategorySerializer(ModelSerializer):
    """
    Serializer for the BudgetCategory model
    """
    budget = PrimaryKeyRelatedField()
    budget_expenses = BudgetExpenseSerializer(
            many=True,
            read_only=True,
            )

    class Meta(type):
        """
        Meta
        """
        model = BudgetCategory
        fields = ('id', 'amount', 'budget', 'title', 'budget_expenses', )


class BudgetSerializer(ModelSerializer):
    """
    Serializer for the Budget model
    """
    budget_categories = BudgetCategorySerializer(
            many=True,
            read_only=True,
            )

    class Meta(type):
        """
        Meta
        """
        model = Budget
        fields = ('budget_categories', 'id', 'owner', 'title', )
        read_only_fields = ('owner', )


class CheckListItemSerializer(ModelSerializer):
    """
    Serializer for the CheckListItem model
    """
    check_list = PrimaryKeyRelatedField()

    class Meta(type):
        """
        Meta
        """
        model = CheckListItem
        fields = ('checked', 'check_list', 'description', 'id', 'title', )


class CheckListSerializer(ModelSerializer):
    """
    Serializer for the CheckList model
    """
    check_list_items = CheckListItemSerializer(
            many=True,
            read_only=True,
            )

    class Meta(type):
        """
        Meta
        """
        model = CheckList
        fields = ('check_list_items', 'id', 'title', 'owner', )
        read_only_fields = ('owner', )


class UserSerializer(ModelSerializer):
    """
    Serializer for the User model
    """
    class Meta(type):
        """
        Meta
        """
        model = User
        fields = ('id', 'email', 'username', 'password', )
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
