"""
API package tests
"""
from pdb import set_trace

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase

from guardian.shortcuts import assign_perm
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
        CheckList.objects.create(
                owner=self.user1,
                title='Test List 1',
                )

        assign_perm('api.add_checklist', self.user)
        assign_perm('api.view_checklist', self.user, self.check_list)

    def test_GET_authentication_required(self):
        response = self.client.get('/api/v1/check-lists/', )
        self.assertEqual(response.status_code, 401)

    def test_GET_returns_allowed_instances(self):
        """
        GET to the endpoint returns instances

        - that the user has permission to view
        """
        self.client.login(username='test', password='password', )
        response = self.client.get('/api/v1/check-lists/', )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('title'), 'Test List')

    def test_POST_authentication_required(self):
        response = self.client.post('/api/v1/check-lists/', )
        self.assertEqual(response.status_code, 401)

    def test_POST_creates_instance(self):
        """
        POST to the endpoint creates a CheckList instance
        """
        self.client.login(username='test', password='password', )
        response = self.client.post(
                '/api/v1/check-lists/',
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
