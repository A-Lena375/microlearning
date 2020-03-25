from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from microlearning.models import Article


class TestViews(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

        self.article = Article.objects.create(title="Some title",
                                              status="new",
                                              type="some_str",
                                              id_med=9)

    def test_login_required_page(self):
        article_index_url = reverse('microlearning:article_index')

        response = self.client.get(article_index_url)
        self.assertRedirects(response, '/accounts/login/?next=' + article_index_url)

    def test_article_index_GET(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('microlearning:article_index'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'article/index.html')

    def test_article_list_GET(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('microlearning:article_list'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'article/list.html')

    def test_article_details_GET(self):
        self.client.force_login(self.user)

        response = self.client.get(self.article.get_absolute_url())

        self.assertEquals(
            reverse('microlearning:article_details', args=['some_str', 9, 'some-title']),
            self.article.get_absolute_url()
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'article/detail.html')

    def test_settings_POST(self):
        self.client.force_login(self.user)

        self.assertEquals(self.user.profile.subscribed_category, '')

        response = self.client.post(reverse('microlearning:settings'), {'category': 'familymedicine'})
        self.assertEquals(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertEquals(self.user.profile.subscribed_category, 'familymedicine')

    def test_settings_GET(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('microlearning:settings'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'article/settings.html')

    def test_register_POST(self):
        response = self.client.post(reverse('microlearning:register'), {
            'username': 'test_user',
            'first_name': 'test_user',
            'email': 'user@test.com',
            'password': 'test_password',
            'password2': 'test_password'
        })

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration_done.html')

    def test_register_POST_no_data(self):
        response = self.client.post(reverse('microlearning:register'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertFormError(response, 'form', 'username', ["This field is required."])
        self.assertFormError(response, 'form', 'password', ["This field is required."])

    def test_register_GET(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('microlearning:register'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_edit_POST(self):
        self.client.force_login(self.user)

        self.assertEquals(self.user.first_name, '')
        self.assertEquals(self.user.last_name, '')
        self.assertEquals(self.user.email, 'temporary@gmail.com')

        response = self.client.post(reverse('microlearning:edit'), {
            'first_name': 'test_user',
            'last_name': 'test_user',
            'email': 'user@test.com'
        })

        self.assertEquals(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertEquals(self.user.first_name, 'test_user')
        self.assertEquals(self.user.last_name, 'test_user')
        self.assertEquals(self.user.email, 'user@test.com')

    def test_edit_GET(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('microlearning:edit'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit.html')

    def test_view_profile_GET(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('microlearning:profile'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
