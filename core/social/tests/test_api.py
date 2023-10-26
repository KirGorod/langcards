from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from user.factories import UserFactory
from social.factories import SiteCommentFactory
from social.models import SiteComment


class TestSiteMessages(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory.create()
        self.user2 = UserFactory.create()
        self.comment = SiteCommentFactory.create(user=self.user)
        SiteCommentFactory.create_batch(20)

    def test_get_single_comment(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('social:comments-detail', args=[self.comment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_comment_no_auth(self):
        url = reverse('social:comments-detail', args=[self.comment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_single_comment_not_owned(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('social:comments-detail', args=[self.comment.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_comment_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('social:comments-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_get_comment_list_no_auth(self):
        url = reverse('social:comments-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)

    def test_post_comment(self):
        self.client.force_authenticate(user=self.user)
        data = {'message': 'This site is awesome'}
        url = reverse('social:comments-list')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_comment_no_auth(self):
        data = {'message': 'This site is awesome'}
        url = reverse('social:comments-list')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_comment(self):
        self.client.force_authenticate(user=self.user)
        message = 'This site is awesome'
        data = {'message': message}
        url = reverse('social:comments-detail', args=[self.comment.pk])
        response = self.client.patch(url, data=data, format='json')
        comment = SiteComment.objects.get(id=self.comment.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(comment.message, message)

    def test_patch_comment_no_auth(self):
        message = 'This site is awesome'
        data = {'message': message}
        url = reverse('social:comments-detail', args=[self.comment.pk])
        response = self.client.patch(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_comment_not_owned(self):
        self.client.force_authenticate(user=self.user2)
        message = 'This site is awesome'
        data = {'message': message}
        url = reverse('social:comments-detail', args=[self.comment.pk])
        response = self.client.patch(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_comment(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('social:comments-detail', args=[self.comment.pk])
        response = self.client.delete(url)
        comment_exists = SiteComment.objects.filter(
            id=self.comment.pk
        ).exists()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(comment_exists)

    def test_delete_comment_no_auth(self):
        url = reverse('social:comments-detail', args=[self.comment.pk])
        response = self.client.delete(url)
        comment_exists = SiteComment.objects.filter(
            id=self.comment.pk
        ).exists()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(comment_exists)

    def test_delete_comment_not_owned(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('social:comments-detail', args=[self.comment.pk])
        response = self.client.delete(url)
        comment_exists = SiteComment.objects.filter(
            id=self.comment.pk
        ).exists()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(comment_exists)
