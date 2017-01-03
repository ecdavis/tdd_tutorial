import re
from django.core import mail
from .base import FunctionalTest
import time

TEST_EMAIL = 'evan@example.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):
	def test_can_get_email_link_to_log_in(self):
		# Evan goes to the awesome superlists site
		# and notices a "log in" section in the navbar for the first time
		# It's telling him to enter his email address, so he does.
		self.browser.get(self.server_url)
		self.browser.find_element_by_name('email').send_keys(
			TEST_EMAIL + '\n'
		)
		time.sleep(1)

		# A message appears telling him an email has been sent
		email = mail.outbox[0]
		self.assertIn(TEST_EMAIL, email.to)
		self.assertEqual(email.subject, SUBJECT)

		# It has a URL link in it
		self.assertIn('Use this link to log in', email.body)
		url_search = re.search(r'http://.+/.+$', email.body)
		if not url_search:
			self.fail(
				'Could not find URL in email body:\n{}'.format(email.body)
			)
		url = url_search.group(0)
		self.assertIn(self.server_url, url)

		# He clicks it
		self.browser.get(url)

		# He is logged in!
		self.browser.find_element_by_link_text('Log out')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertIn(TEST_EMAIL, navbar.text)
