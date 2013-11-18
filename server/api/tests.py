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
from lib import increment_slug


def login(client, username, password):
    return client.post(
            '/api/v1/sessions/',
            {
                'password': password,
                'username': username,
            },
        )

def logout(client):
    return client.delete('/api/v1/sessions/', )


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

        assign_perm('api.add_checklist', self.user)
        assign_perm('api.view_checklist', self.user)
        assign_perm('api.view_checklist', self.user, self.check_list)

    def test_GET_authentication_required(self):
        response = self.client.get('/api/v1/check-lists/', )
        self.assertEqual(response.status_code, 403)

        response = self.client.get('/api/v1/check-lists/%d/' % (
            self.check_list.id, ), )
        self.assertEqual(response.status_code, 403)

    def test_GET_returns_allowed_instances(self):
        """
        GET to the endpoint returns instances

        - that the user has permission to view
        """
        login(self.client, username='test', password='password', )
        response = self.client.get('/api/v1/check-lists/', )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('id'), self.check_list.id)
        self.assertEqual(response.data[0].get('title'), self.check_list.title)

    def test_GET_instance_requires_permission(self):
        """
        GET with an id requires permission to view
        """
        login(self.client, username='test', password='password', )
        response = self.client.get('/api/v1/check-lists/%d/' % (
            self.check_list_1.id,
            ), )
        self.assertEqual(response.status_code, 404)

    def test_GET_instance(self):
        """
        GET with an id returns specified instance
        """
        login(self.client, username='test', password='password', )
        response = self.client.get('/api/v1/check-lists/%d/' % (
            self.check_list.id,
            ), )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('id'), self.check_list.id)
        self.assertEqual(response.data.get('title'), self.check_list.title)

    def test_POST_authentication_required(self):
        response = self.client.post('/api/v1/check-lists/', )
        self.assertEqual(response.status_code, 403)

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
        response = self.client.get('/api/v1/sessions/', )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('isAuthenticated'), False)

    def test_GET_returns_authenticated(self):
        """
        Return authenticated user's session info
        """
        self.client.login(username='test', password='password', )
        response = self.client.get('/api/v1/sessions/', )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('isAuthenticated'), True)

    def test_DELETE_requires_authentication(self):
        """
        DELETE requires an existing session
        """
        response = self.client.delete('/api/v1/sessions/', )
        self.assertEqual(response.status_code, 400)
        self.assertTrue('session' in response.data.get('detail', ''))

    def test_DELETE_deletes_session(self):
        """
        DELETE deletes the current session

        logs out the current user
        """
        self.client.post(
                '/api/v1/sessions/',
                {
                    'username': 'test',
                    'password': 'password',
                },
            )
        response = self.client.delete('/api/v1/sessions/', )
        self.assertEqual(response.status_code, 204)

    def test_POST_requires_parameters(self):
        """
        POST requires parameters

        - password
        - username
        """
        response = self.client.post(
                '/api/v1/sessions/',
                {
                    'password': 'password',
                },
            )
        self.assertEqual(response.status_code, 400)
        self.assertTrue('username' in response.data.get('detail', ''))

        response = self.client.post(
                '/api/v1/sessions/',
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
                '/api/v1/sessions/',
                {
                    'username': 'test',
                    'password': 'notMyPassword',
                },
            )
        self.assertEqual(response.status_code, 400)
        self.assertTrue('Invalid' in response.data.get('detail'))

        response = self.client.post(
                '/api/v1/sessions/',
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
                '/api/v1/sessions/',
                {
                    'username': 'test',
                    'password': 'password',
                },
            )
        self.assertEqual(response.status_code, 201)
        self.assertTrue('Authentication' in response.data.get('detail', ''))
        cookie = response.cookies.popitem()
        self.assertEqual('sessionid', cookie[0])
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
