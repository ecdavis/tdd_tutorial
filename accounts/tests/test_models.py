from django.contrib import auth
from django.test import TestCase
from accounts.models import Token

User = auth.get_user_model()


class UserModelTest(TestCase):
	def test_user_is_valid_with_email_only(self):
		user = User(email="foo@example.com")
		user.full_clean()

	def test_no_problem_with_auth_login(self):
		user = User.objects.create(email="evan@example.com")
		user.backend = ''
		request = self.client.request().wsgi_request
		auth.login(request, user)  # should not raise

	def test_email_is_primary_key(self):
		user = User()
		self.assertFalse(hasattr(user, 'id'))


class TokenModelTest(TestCase):
	def test_links_user_with_auto_generated_uid(self):
		token1 = Token.objects.create(email='foo@example.com')
		token2 = Token.objects.create(email='foo@example.com')
		self.assertNotEqual(token1.uid, token2.uid)
