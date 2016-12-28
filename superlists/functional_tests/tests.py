from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = None
        self.new_browser_session()

    def tearDown(self):
        self.browser.quit()

    def new_browser_session(self):
        if self.browser:
            self.browser.quit()
        self.browser = webdriver.Firefox(
            firefox_binary=FirefoxBinary(
                firefox_path=r"C:\Program Files (x86)\Mozilla Firefox ESR\firefox.exe"
            )
        )
        self.browser.implicitly_wait(3)

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_for_one_user(self):
        # Evan has heard about a cool new online to-do app. He goes to check out
        # its homepage.
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "Buy peacock feathers" into a text box (Evan's hobby is tying
        # fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')

        # When he hits enter, the page updates, and now the page lists "1: Buy
        # peacock feathers" as an item in a to-do list.
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting him to add another item. He enters
        # "Use peacock feathers to make a fly" (Evan is very methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on his list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Satisfied, he goes back to sleep.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Evan starts a new todo list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # He notices that his list has a unique URL
        evan_list_url = self.browser.current_url
        self.assertRegex(evan_list_url, '/lists/.+')

        # Now a new user, Calvin, comes along to the site

        ## We use a new browser session to make sure that no
        ## information of Evan's is coming through from cookies etc
        self.new_browser_session()

        # Calvin visits the home page. There is no sign of Evan's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Calvin starts a new list by entering a new item. He is
        # less interesting than Evan...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: Buy milk')

        # Calvin gets his own unique URL
        calvin_list_url = self.browser.current_url
        self.assertRegex(calvin_list_url, '/lists/.+')
        self.assertNotEqual(calvin_list_url, evan_list_url)

        # Again, there is no trace of Evan's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep

    def test_layout_and_styling(self):
        # Evan goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # He notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=10
        )

        # He starts a new list and sees the input is nicely centered
        # there too
        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width']/2,
            512,
            delta=10
        )
