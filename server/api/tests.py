"""
API package tests
"""
from ipdb import set_trace

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import override_settings

from guardian.shortcuts import assign_perm
from rest_framework.test import APIClient

from api.models import Budget, BudgetCategory, CheckList, CheckListItem
from lib import increment_slug


def login(client, username, password):
    return client.post(
            '/api/v1/sessions',
            {
                'password': password,
                'username': username,
            },
        )

def logout(client):
    return client.delete('/api/v1/sessions', )


class BudgetTest(TestCase):
    """
    Unit tests for the Buget API
    """
    def setUp(self):
        """
        Test suite set up method
        """
        self.client = APIClient()
        self.user = User.objects.create(
                username='test',
                password='password',
                )
        self.user.set_password('password')
        self.user.save()
        self.user1 = User.objects.create(
                username='test1',
                password='password',
                )
        self.user1.set_password('password')
        self.user1.save()
        self.budget = Budget.objects.create(
                owner=self.user,
                title='Test Budget',
                )
        self.budget_1 = Budget.objects.create(
                owner=self.user1,
                title='Test Budget 1',
                )

        BudgetCategory.objects.create(
                budget=self.budget,
                title='Category 1',
                )
        BudgetCategory.objects.create(
                budget=self.budget,
                title='Category 2',
                )

        assign_perm('api.add_budget', self.user)
        assign_perm('api.view_budget', self.user)
        assign_perm('api.view_budget', self.user, self.budget)

    def test_GET_authentication_required(self):
        """
        Authentication is required
        """
        response = self.client.get('/api/v1/budgets', )
        self.assertEqual(response.status_code, 403)

        response = self.client.get('/api/v1/budgets/%d' % (
            self.budget.id, ), )
        self.assertEqual(response.status_code, 403)

    def test_GET_returns_allowed_instances(self):
        """
        GET to the endpoint returns instances

        - that the user has permission to view
        """
        login(self.client, username='test', password='password', )
        response = self.client.get('/api/v1/budgets', )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('id'), self.budget.id)
        self.assertEqual(response.data[0].get('title'), self.budget.title)
        self.assertEqual(len(response.data[0].get('budget_categories')), 2)

    def test_GET_instance_requires_permission(self):
        """
        GET with an id requires permission to view
        """
        login(self.client, username='test', password='password', )
        response = self.client.get('/api/v1/budgets/%d' % (
            self.budget_1.id,
            ), )
        self.assertEqual(response.status_code, 404)

    def test_GET_instance(self):
        """
        GET with an id returns specified instance
        """
        login(self.client, username='test', password='password', )
        response = self.client.get('/api/v1/budgets/%d' % (
            self.budget.id,
            ), )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('id'), self.budget.id)
        self.assertEqual(response.data.get('title'), self.budget.title)
        self.assertEqual(len(response.data.get('budget_categories')), 2)

    def test_POST_authentication_required(self):
        """
        POST requires authentication
        """
        response = self.client.post('/api/v1/budgets', )
        self.assertEqual(response.status_code, 403)

    def test_POST_creates_instance(self):
        """
        POST to the endpoint creates a Budget instance
        """
        self.client.login(username='test', password='password', )
        response = self.client.post(
                '/api/v1/budgets',
                {
                    'title': 'My Budget',
                },
            )
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data.get('title'), 'My Budget')

        budgets = Budget.objects.filter(
                title='My Budget',
                owner__id=self.user.id,
                )
        self.assertEqual(budgets.count(), 1)
        budget = budgets[0]

        self.assertTrue(self.user.has_perm(
            'api.change_budget',
            budget))
        self.assertTrue(self.user.has_perm(
            'api.delete_budget',
            budget))
        self.assertTrue(self.user.has_perm(
            'api.view_budget',
            budget))


class BudgetCategoryTest(TestCase):
    """
    Unit tests for the BudgetCategory API
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
                username='test',
                password='password',
                )
        self.user.set_password('password')
        self.user.save()
        self.user1 = User.objects.create(
                username='test1',
                password='password',
                )
        self.user1.set_password('password')
        self.user1.save()
        self.budget = Budget.objects.create(
                owner=self.user,
                title='Test Budget',
                )
        self.budget_1 = Budget.objects.create(
                owner=self.user1,
                title='Test Budget 1',
                )

        self.budget_category = BudgetCategory.objects.create(
                budget=self.budget,
                title='Category 1',
                )
        self.budget_category_1 = BudgetCategory.objects.create(
                budget=self.budget_1,
                title='Category 2',
                )

        assign_perm('api.add_budget', self.user)
        assign_perm('api.change_budget', self.user)
        assign_perm('api.view_budget', self.user)
        assign_perm('api.change_budget', self.user, self.budget)
        assign_perm('api.view_budget', self.user, self.budget)
        assign_perm('api.add_budgetcategory', self.user)
        assign_perm('api.change_budgetcategory', self.user)

        assign_perm('api.add_budget', self.user1)
        assign_perm('api.change_budget', self.user1)
        assign_perm('api.view_budget', self.user1)
        assign_perm('api.add_budgetcategory', self.user1)
        assign_perm('api.change_budgetcategory', self.user1)

    def test_GET_list_not_allowed(self):
        """
        Listing all BudgetCategories is not allowed
        """
        response = self.client.get('/api/v1/budget-categories', )
        self.assertEqual(response.status_code, 403)

        login(self.client, username='test', password='password', )
        response = self.client.get('/api/v1/budget-categories', )
        self.assertEqual(response.status_code, 403)

    def test_GET_authentication_required(self):
        """
        User must be authenticated to retrieve a BudgetCategory
        """
        response = self.client.get('/api/v1/budget-categories/%d' % (
            self.budget_category.id, ), )
        self.assertEqual(response.status_code, 403)

    def test_GET_returns_allowed_instance(self):
        """
        Return permitted budget_category

        Only instances that the user has view permission for the related
        budget_category are returned
        """
        login(self.client, username='test', password='password', )
        response = self.client.get('/api/v1/budget-categories/%d' % (
            self.budget_category.id, ), )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.get('title') == self.budget_category.title)

    def test_GET_return_403_if_not_permitted(self):
        """
        Return 403 on not permitted instances

        Only instances that the user has view permission for the related
        check_list are returned
        """
        login(self.client, username='test', password='password', )
        response = self.client.get('/api/v1/budget-categories/%d' % (
            self.budget_category_1.id, ), )
        self.assertEqual(response.status_code, 403)

    def test_POST_authentication_required(self):
        """
        User must be authenticated to create a BudgetCategory
        """
        response = self.client.post(
                '/api/v1/budget-categories',
                { },
                )
        self.assertEqual(response.status_code, 403)

    def test_POST_authorization_required(self):
        """
        User must have permission to create a BudgetCategory

        - 'add-budget' permission
        """
        login(self.client, username='test1', password='password', )
        response = self.client.post(
                '/api/v1/budget-categories',
                {
                    'budget': self.budget.id,
                    'title': 'Category 1',
                },
                )
        self.assertEqual(response.status_code, 403)

    def test_POST_creates_check_list_item(self):
        """
        Create a new BudgetCategory
        """
        login(self.client, username='test', password='password', )
        response = self.client.post(
                '/api/v1/budget-categories',
                {
                    'budget': self.budget.id,
                    'title': 'Category 1',
                },
                )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('budget'), self.budget.id)
        self.assertEqual(response.data.get('title'), 'Category 1')


class CheckListPermissionsTest(TestCase):
    """
    Unit tests for the CheckListPermissions API
    """
    def setUp(self):
        """
        Test suite set up method
        """
        self.client = APIClient()
        self.user = User.objects.create(
                username='test',
                password='password',
                )
        self.user.set_password('password')
        self.user.save()
        self.user1 = User.objects.create(
                username='test1',
                password='password',
                )
        self.user1.set_password('password')
        self.user1.save()
        self.check_list = CheckList.objects.create(
                owner=self.user,
                title='Test List',
                )

        assign_perm('api.view_checklist', self.user)
        assign_perm('api.view_checklist', self.user, self.check_list)
        assign_perm('api.change_checklist', self.user, self.check_list)

    def test_GET_authentication_required(self):
        """
        Authentication is required
        """
        response = self.client.get('/api/v1/check-list-permissions/' \
                '{check_list_id}'.format(check_list_id=self.check_list.id, ),
                )
        self.assertEqual(response.status_code, 403)

    def test_GET_authorization_required(self):
        """
        Authorization is required
        """
        login(self.client, username='test1', password='password', )
        response = self.client.get('/api/v1/check-list-permissions/' \
                '{check_list_id}'.format(check_list_id=self.check_list.id, ),
                )
        self.assertEqual(response.status_code, 403)

    def test_GET_returns_list_of_users(self):
        """
        Endpoint returns like of users with any permission(s)
        """
        login(self.client, username='test', password='password', )
        response = self.client.get(
                '/api/v1/check-list-permissions/{check_list_id}'.format(
                    check_list_id=self.check_list.id,
                    ),
                )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.data), list)
        self.assertEqual(len(response.data), 1)

        # add permissions for a second user
        assign_perm('api.view_checklist', self.user1, self.check_list)
        assign_perm('api.change_checklist', self.user1, self.check_list)

        response = self.client.get(
                '/api/v1/check-list-permissions/{check_list_id}'.format(
                    check_list_id=self.check_list.id,
                    ),
                )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.data), list)
        self.assertEqual(len(response.data), 2)

    def test_PUT_authentication_required(self):
        """
        Authentication is required
        """
        response = self.client.put('/api/v1/check-list-permissions/' \
                '{check_list_id}'.format(check_list_id=self.check_list.id, ),
                {
                    'user': self.user1.id,
                    },
                )
        self.assertEqual(response.status_code, 403)

    def test_PUT_authorization_required(self):
        """
        Authorization is required
        """
        login(self.client, username='test1', password='password', )
        response = self.client.put('/api/v1/check-list-permissions/' \
                '{check_list_id}'.format(check_list_id=self.check_list.id, ),
                {
                    'user': self.user1.id,
                    },
                )
        self.assertEqual(response.status_code, 403)

    def test_PUT_toggle_owner_permissions(self):
        """
        Cannot change owner permissions
        """
        login(self.client, username='test', password='password', )
        response = self.client.put(
                '/api/v1/check-list-permissions/{check_list_id}'.format(
                    check_list_id=self.check_list.id,
                    ),
                {
                    'user': self.user.id,
                    },
                )
        self.assertEqual(response.status_code, 400)

    def test_PUT_toggles_user_permissions(self):
        """
        Toggle the permissions set for a given user
        """
        login(self.client, username='test', password='password', )
        # add permissions
        response = self.client.put(
                '/api/v1/check-list-permissions/{check_list_id}'.format(
                    check_list_id=self.check_list.id,
                    ),
                {
                    'user': self.user1.id,
                    },
                )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.get('change_checklist'))
        self.assertTrue(self.user1.has_perm(
            'api.change_checklist',
            self.check_list,
            ))
        self.assertTrue(response.data.get('view_checklist'))
        self.assertTrue(self.user1.has_perm(
            'api.view_checklist',
            self.check_list,
            ))

        # remove permissions
        response = self.client.put(
                '/api/v1/check-list-permissions/{check_list_id}'.format(
                    check_list_id=self.check_list.id,
                    ),
                {
                    'user': self.user1.id,
                    },
                )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data.get('change_checklist'))
        self.assertFalse(self.user1.has_perm(
            'api.change_checklist',
            self.check_list,
            ))
        self.assertFalse(response.data.get('view_checklist'))
        self.assertFalse(self.user1.has_perm(
            'api.view_checklist',
            self.check_list,
            ))


class CheckListTest(TestCase):
    """
    Unit tests for the CheckList API
    """
    def setUp(self):
        """
        Test suite set up method
        """
        self.client = APIClient()
        self.user = User.objects.create(
                username='test',
                password='password',
                )
        self.user.set_password('password')
        self.user.save()
        self.user1 = User.objects.create(
                username='test1',
                password='password',
                )
        self.user1.set_password('password')
        self.user1.save()
        self.check_list = CheckList.objects.create(
                owner=self.user,
                title='Test List',
                )
        self.check_list_1 = CheckList.objects.create(
                owner=self.user1,
                title='Test List 1',
                )

        CheckListItem.objects.create(
                check_list=self.check_list,
                title='Item 1',
                )
        CheckListItem.objects.create(
                check_list=self.check_list,
                title='Item 2',
                description='things',
                checked=True,
                )

        assign_perm('api.add_checklist', self.user)
        assign_perm('api.view_checklist', self.user)
        assign_perm('api.view_checklist', self.user, self.check_list)

    def test_GET_authentication_required(self):
        """
        Authentication is required
        """
        response = self.client.get('/api/v1/check-lists', )
        self.assertEqual(response.status_code, 403)

        response = self.client.get('/api/v1/check-lists/%d' % (
            self.check_list.id, ), )
        self.assertEqual(response.status_code, 403)

    def test_GET_returns_allowed_instances(self):
        """
        GET to the endpoint returns instances

        - that the user has permission to view
        """
        login(self.client, username='test', password='password', )
        response = self.client.get('/api/v1/check-lists', )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('id'), self.check_list.id)
        self.assertEqual(response.data[0].get('title'), self.check_list.title)
        self.assertEqual(len(response.data[0].get('check_list_items')), 2)

    def test_GET_instance_requires_permission(self):
        """
        GET with an id requires permission to view
        """
        login(self.client, username='test', password='password', )
        response = self.client.get('/api/v1/check-lists/%d' % (
            self.check_list_1.id,
            ), )
        self.assertEqual(response.status_code, 404)

    def test_GET_instance(self):
        """
        GET with an id returns specified instance
        """
        login(self.client, username='test', password='password', )
        response = self.client.get('/api/v1/check-lists/%d' % (
            self.check_list.id,
            ), )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('id'), self.check_list.id)
        self.assertEqual(response.data.get('title'), self.check_list.title)
        self.assertEqual(len(response.data.get('check_list_items')), 2)

    def test_POST_authentication_required(self):
        """
        POST requires authentication
        """
        response = self.client.post('/api/v1/check-lists', )
        self.assertEqual(response.status_code, 403)

    def test_POST_creates_instance(self):
        """
        POST to the endpoint creates a CheckList instance
        """
        self.client.login(username='test', password='password', )
        response = self.client.post(
                '/api/v1/check-lists',
                {
                    'title': 'My List',
                },
            )
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data.get('title'), 'My List')

        check_lists = CheckList.objects.filter(
                title='My List',
                owner__id=self.user.id,
                )
        self.assertEqual(check_lists.count(), 1)
        check_list = check_lists[0]

        self.assertTrue(self.user.has_perm(
            'api.change_checklist',
            check_list))
        self.assertTrue(self.user.has_perm(
            'api.delete_checklist',
            check_list))
        self.assertTrue(self.user.has_perm(
            'api.view_checklist',
            check_list))


class CheckListItemTest(TestCase):
    """
    Unit tests for the CheckListItem API
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
                username='test',
                password='password',
                )
        self.user.set_password('password')
        self.user.save()
        self.user1 = User.objects.create(
                username='test1',
                password='password',
                )
        self.user1.set_password('password')
        self.user1.save()
        self.check_list = CheckList.objects.create(
                owner=self.user,
                title='Test List',
                )
        self.check_list_1 = CheckList.objects.create(
                owner=self.user1,
                title='Test List 1',
                )

        self.check_list_item = CheckListItem.objects.create(
                check_list=self.check_list,
                title='Item 1',
                )
        self.check_list_item_1 = CheckListItem.objects.create(
                check_list=self.check_list_1,
                title='Item 2',
                description='things',
                checked=True,
                )

        assign_perm('api.add_checklist', self.user)
        assign_perm('api.change_checklist', self.user)
        assign_perm('api.view_checklist', self.user)
        assign_perm('api.change_checklist', self.user, self.check_list)
        assign_perm('api.view_checklist', self.user, self.check_list)
        assign_perm('api.add_checklistitem', self.user)
        assign_perm('api.change_checklistitem', self.user)
        assign_perm('api.delete_checklistitem', self.user)

        assign_perm('api.add_checklist', self.user1)
        assign_perm('api.change_checklist', self.user1)
        assign_perm('api.view_checklist', self.user1)
        assign_perm('api.add_checklistitem', self.user1)
        assign_perm('api.change_checklistitem', self.user1)

    def test_GET_list_not_allowed(self):
        """
        Listing all CheckListItems is not allowed
        """
        response = self.client.get('/api/v1/check-list-items', )
        self.assertEqual(response.status_code, 403)

        login(self.client, username='test', password='password', )
        response = self.client.get('/api/v1/check-list-items', )
        self.assertEqual(response.status_code, 403)

    def test_GET_authentication_required(self):
        """
        User must be authenticated to retrieve a CheckListItem
        """
        response = self.client.get('/api/v1/check-list-items/%d' % (
            self.check_list_item.id, ), )
        self.assertEqual(response.status_code, 403)

    def test_GET_returns_allowed_instance(self):
        """
        Return permitted check_list_item

        Only instances that the user has view permission for the related
        check_list are returned
        """
        login(self.client, username='test', password='password', )
        response = self.client.get('/api/v1/check-list-items/%d' % (
            self.check_list_item.id, ), )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.get('title') == self.check_list_item.title)
        self.assertTrue(response.data.get('description') \
                == self.check_list_item.description)
        self.assertTrue(response.data.get('checked') \
                == self.check_list_item.checked)

    def test_GET_return_403_if_not_permitted(self):
        """
        Return 403 on not permitted instances

        Only instances that the user has view permission for the related
        check_list are returned
        """
        login(self.client, username='test', password='password', )
        response = self.client.get('/api/v1/check-list-items/%d' % (
            self.check_list_item_1.id, ), )
        self.assertEqual(response.status_code, 403)

    def test_POST_authentication_required(self):
        """
        User must be authenticated to create a CheckListItem
        """
        response = self.client.post(
                '/api/v1/check-list-items',
                { },
                )
        self.assertEqual(response.status_code, 403)

    def test_POST_authorization_required(self):
        """
        User must have permission to create a CheckListItem

        - 'add-checklist' permission
        """
        login(self.client, username='test1', password='password', )
        response = self.client.post(
                '/api/v1/check-list-items',
                {
                    'check_list': self.check_list.id,
                    'title': 'Item 1',
                },
                )
        self.assertEqual(response.status_code, 403)

    def test_POST_creates_check_list_item(self):
        """
        Create a new CheckListItem
        """
        login(self.client, username='test', password='password', )
        response = self.client.post(
                '/api/v1/check-list-items',
                {
                    'check_list': self.check_list.id,
                    'checked': False,
                    'description': 'more info',
                    'title': 'Item 1',
                },
                )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('check_list'), self.check_list.id)
        self.assertEqual(response.data.get('checked'), False)
        self.assertEqual(response.data.get('description'), 'more info')
        self.assertEqual(response.data.get('title'), 'Item 1')

    def test_DELETE_authentication_required(self):
        """
        User must be authenticated to delete a CheckListItem
        """
        response = self.client.delete(
                '/api/v1/check-list-items/%s' % self.check_list_item.id,
                { },
                )
        self.assertEqual(response.status_code, 403)

    def test_DELETE_authorization_required(self):
        """
        User must have permission to delete a CheckListItem

        - 'change-checklist' permission
        """
        login(self.client, username='test1', password='password', )
        response = self.client.delete(
                '/api/v1/check-list-items/%s' % self.check_list_item.id,
                { },
                )
        self.assertEqual(response.status_code, 403)

    def test_DELETE_deletes_check_list_item(self):
        """
        Delete a CheckListItem
        """
        login(self.client, username='test', password='password', )
        response = self.client.delete(
                '/api/v1/check-list-items/%s' % self.check_list_item.id,
                { },
                )
        self.assertEqual(response.status_code, 204)

        with self.assertRaises(CheckListItem.DoesNotExist):
            CheckListItem.objects.get(id=self.check_list_item.id, )


class SessionTest(TestCase):
    """
    Test the authentication API
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
                username='test',
                password='password',
                )
        self.user.set_password('password')
        self.user.save()

    def test_GET_returns_non_authenticated(self):
        """
        Return non authenticated user's session info
        """
        response = self.client.get('/api/v1/sessions', )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('isAuthenticated'), False)

    def test_GET_returns_authenticated(self):
        """
        Return authenticated user's session info
        """
        self.client.login(username='test', password='password', )
        response = self.client.get('/api/v1/sessions', )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('isAuthenticated'), True)

    def test_DELETE_requires_authentication(self):
        """
        DELETE requires an existing session
        """
        response = self.client.delete('/api/v1/sessions', )
        self.assertEqual(response.status_code, 400)
        self.assertTrue('session' in response.data.get('detail', ''))

    def test_DELETE_deletes_session(self):
        """
        DELETE deletes the current session

        logs out the current user
        """
        self.client.post(
                '/api/v1/sessions',
                {
                    'username': 'test',
                    'password': 'password',
                },
            )
        response = self.client.delete('/api/v1/sessions', )
        self.assertEqual(response.status_code, 204)

    def test_POST_requires_parameters(self):
        """
        POST requires parameters

        - password
        - username
        """
        response = self.client.post(
                '/api/v1/sessions',
                {
                    'password': 'password',
                },
            )
        self.assertEqual(response.status_code, 400)
        self.assertTrue('username' in response.data.get('detail', ''))

        response = self.client.post(
                '/api/v1/sessions',
                {
                    'username': 'test',
                },
            )
        self.assertEqual(response.status_code, 400)
        self.assertTrue('password' in response.data.get('detail', ''))

    def test_POST_checks_credentials(self):
        """
        POST requires correct credentials
        """
        response = self.client.post(
                '/api/v1/sessions',
                {
                    'username': 'test',
                    'password': 'notMyPassword',
                },
            )
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Invalid' in response.data.get('detail'))

        response = self.client.post(
                '/api/v1/sessions',
                {
                    'username': 'notMyUsername',
                    'password': 'password',
                },
            )
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Invalid' in response.data.get('detail'))

    def test_POST_creates_session(self):
        """
        POST to the endpoint authenticates a user and creates a session
        """
        response = self.client.post(
                '/api/v1/sessions',
                {
                    'username': 'test',
                    'password': 'password',
                },
            )
        self.assertEqual(response.status_code, 201)
        self.assertTrue('Authentication' in response.data.get('detail', ''))
        self.assertTrue('csrftoken' in response.cookies)
        self.assertTrue('sessionid' in response.cookies)
        self.assertEqual(response.data.get('isAuthenticated'), True)

    def test_POST_username_is_case_insensitive(self):
        """
        Usernames are lowercase'd before authenticating
        """
        response = self.client.post(
                '/api/v1/sessions',
                {
                    'username': 'Test',
                    'password': 'password',
                    },
                )
        self.assertEqual(response.status_code, 201)
        self.assertTrue('Authentication' in response.data.get('detail', ''))
        self.assertTrue('csrftoken' in response.cookies)
        self.assertTrue('sessionid' in response.cookies)
        self.assertEqual(response.data.get('isAuthenticated'), True)


class SlugTest(TestCase):
    """
    Test slug lib function
    """
    def test_first_increment_slug(self):
        """
        First increment on a slug should append '-1' to the end
        """
        slug = 'hello-world'
        new_slug = increment_slug(slug)
        self.assertEqual(new_slug, '%s-1' % slug)

    def test_increment_slug(self):
        """
        Incrementing a slug should increment the number at the end
        """
        slug = 'hello-world-1'
        new_slug = increment_slug(slug)
        self.assertEqual(new_slug, 'hello-world-2')

        slug = 'hello-world-10'
        new_slug = increment_slug(slug)
        self.assertEqual(new_slug, 'hello-world-11')


@override_settings(TESTING=True)
class UpdateCodebaseTest(TestCase):
    """
    Test codebase update API
    """
    def setUp(self):
        self.client = APIClient()

    def test_POST_updates_codebase(self):
        """
        POST to endpoint runs external update script
        """
        response = self.client.post(
                '/api/v1/update',
                )
        self.assertEqual(response.status_code, 200)


class UserTest(TestCase):
    """
    Unit tests for the User API
    """
    def setUp(self):
        """
        Test suite set up method
        """
        self.client = APIClient()
        self.user = User.objects.create(
                email="test@jotter.ca",
                username='test',
                password='password',
                )
        self.user.set_password('password')
        self.user.save()
        self.user1 = User.objects.create(
                email="test1@jotter.ca",
                username='test1',
                password='password',
                )
        self.user1.set_password('password')
        self.user1.save()

        assign_perm('auth.add_user', self.user)
        assign_perm('auth.change_user', self.user)

    def test_GET_returns_list_of_users(self):
        """
        All users listed

        list values should be well-formed
        """
        response = self.client.get('/api/v1/users', )
        self.assertEqual(response.status_code, 200)
        # there should be 1 more than created in the setup method
        # -> an unusable user is always added to the system
        self.assertEqual(len(response.data), 3)
        user_dict = response.data[0]
        self.assertTrue('email' in user_dict)
        self.assertTrue('username' in user_dict)
        self.assertTrue('password' in user_dict)

    def test_POST_authentication_required(self):
        """
        User must be authenticated to create a User
        """
        response = self.client.post(
                '/api/v1/users',
                { },
                )
        self.assertEqual(response.status_code, 403)

    def test_POST_authorization_required(self):
        """
        User must have permission to create a User

        - 'add-user' permission
        """
        login(self.client, username='test1', password='password', )
        response = self.client.post(
                '/api/v1/users',
                {
                    'username': 'peterpan',
                    'email': 'ppan@jotter.ca',
                    'password': 'peterpass',
                    },
                )
        self.assertEqual(response.status_code, 403)

    def test_POST_creates_user(self):
        """
        Creates a new User
        """
        login(self.client, username='test', password='password', )
        response = self.client.post(
                '/api/v1/users',
                {
                    'username': 'peterpan',
                    'email': 'ppan@jotter.ca',
                    'password': 'peterpass',
                    },
                )
        self.assertEqual(response.status_code, 201)
        self.assertTrue('email' in response.data)
        self.assertEqual(response.data.get('email'), 'ppan@jotter.ca')
        self.assertTrue('username' in response.data)
        self.assertEqual(response.data.get('username'), 'peterpan')
        self.assertTrue('password' in response.data)
        self.assertNotEqual(response.data.get('password'), 'peterpass')

        try:
            user = User.objects.get(
                    username='peterpan',
                    email='ppan@jotter.ca',
                    )
        except User.DoesNotExist:
            self.fail('User object not found')
        else:
            self.assertTrue(user.check_password('peterpass'))
