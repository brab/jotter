"""
API package tests
"""
from pdb import set_trace

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase

from rest_framework.test import APIClient

from api.models import CheckList


class CheckListAPITest(TestCase):
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
        self.check_list = CheckList.objects.create(
                owner=self.user,
                title='Test List',
                )
        content_type = ContentType.objects.get_for_model(CheckList)
        perm = Permission.objects.get(
                content_type=content_type,
                codename='add_checklist',
                )
        self.user.user_permissions.add(perm)

    def test_GET_returns_all_instances(self):
        """
        GET to the endpoint returns instances

        - that the user has permission to access
        """
        self.client.login(username='test', password='password', )
        response = self.client.get('/api/v1/check-lists/', )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('title'), 'Test List')

    def test_POST_creates_instance(self):
        """
        POST to the endpoint creates a CheckList instance
        """
        self.client.login(username='test', password='password', )
        response = self.client.post(
                '/api/v1/check-lists/',
                {
                    'title': 'My List',
                    'owner': '%d' % self.user.id,
                },
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('title'), 'My List')
        self.assertEqual(response.data.get('owner'), self.user.id)

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
