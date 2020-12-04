import codecs
import os
import tempfile
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from progect.bulletinboard.models import Post


class TestIndexView(TestCase):

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        dir_ = os.path.dirname(os.path.abspath(__file__))
        image = os.path.join(dir_, 'static', 'test.jpg')
        f = codecs.open(image, encoding='base64')
        self.image = SimpleUploadedFile(f.name, f.read())
        f.close()

    def test_index_page_without_posts(self):
        response = self.client.get(reverse('bulletinboard:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Объявлений нет')

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_index_page_with_post(self):
        user = User.objects.create_user(username='username', password='pass1234')
        post = Post.objects.create(author=user, announcement_title='test_prod', description='',
                                   announcement_image=self.image, category='test ct')
        response = self.client.get(reverse('bulletinboard:home'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_announcements'], [post], transform=lambda x: x)
