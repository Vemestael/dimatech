from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json


class BaseApiTestCases:
    class BaseApiTest(APITestCase):
        @classmethod
        def setUpClass(cls):
            super().setUpClass()
            user_obj = User.objects.create_user(username='test_user', password='password')
            user_obj.save()
            cls.headers = {}
            cls.equal_data = []
            cls.model_data = {}
            cls.model_abridged_data = {}
            cls.path = ''
            cls.model_id = 0

        def test_get(self):
            response = self.client.get(path=self.path, format='json', headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(json.loads(response.content), self.equal_data)

        def test_post_success(self):
            response = self.client.post(path=self.path, data=self.model_data, headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        def test_post_incorrect_data(self):
            response = self.client.post(path=self.path, data=self.model_abridged_data, headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        def test_post_forbidden(self):
            response = self.client.post(path=self.path, data=self.model_data, headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_put_success(self):
            response = self.client.put(path=f'{self.path}{self.model_id}/', data=self.model_data, headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_put_incorrect_data(self):
            response = self.client.put(path=f'{self.path}{self.model_id}/', data=self.model_abridged_data,
                                       headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        def test_put_forbidden(self):
            response = self.client.put(path=f'{self.path}{self.model_id}/', data=self.model_data, headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_put_not_found(self):
            response = self.client.put(path=f'{self.path}{self.model_id + 1}/', data=self.model_data,
                                       headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        def test_patch_success(self):
            response = self.client.patch(path=f'{self.path}{self.model_id}/', data=self.model_abridged_data,
                                         headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_patch_forbidden(self):
            response = self.client.patch(path=f'{self.path}{self.model_id}/', data=self.model_abridged_data,
                                         headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_patch_not_found(self):
            response = self.client.patch(path=f'{self.path}{self.model_id + 1}/', data=self.model_abridged_data,
                                         headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        def test_delete_success(self):
            response = self.client.delete(path=f'{self.path}{self.model_id}/', headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        def test_delete_forbidden(self):
            response = self.client.delete(path=f'{self.path}{self.model_id}/', headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        def test_delete_not_found(self):
            response = self.client.delete(path=f'{self.path}{self.model_id + 1}/', headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        def test_head(self):
            response = self.client.head(path=self.path, headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_options(self):
            response = self.client.options(path=self.path, headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
