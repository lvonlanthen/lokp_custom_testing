import random
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from unittest import TestCase

from ..base import (
    BUTTON_APPROVE,
    LINK_VIEW_DEAL,
    LINK_VIEW_STAKEHOLDER,
    PASSWORD,
    TEXT_INACTIVE_VERSION,
    TEXT_PENDING_VERSION,
    TITLE_LOGIN_VIEW,
    USERNAME,
)


class LmkpFunctionalTestCase(TestCase):

    BASE_URL = 'http://localhost:6544'

    def login(
            self, redirect=None, form_present=False, username=None,
            password=None):
        """
        Login and do a redirect if necessary.
        """
        if not form_present:
            self.driver.get(self.url('/login'))
        if self.el('name', 'login') is False:
            # Already logged in
            if redirect:
                self.driver.get(redirect)
            return
        pwd = PASSWORD if not password else password
        user = USERNAME if not username else username
        self.el('name', 'login').send_keys(user)
        self.el('name', 'password').send_keys(pwd)
        if redirect is not None:
            self.driver.execute_script(
                "document.getElementsByName('came_from')[0].value='%s'"
                % redirect)
        self.el('name', 'form.submitted').click()
        self.driver.implicitly_wait(5)

    def logout(self):
        self.driver.get(self.url('/logout'))
        self.driver.implicitly_wait(5)

    def el(self, by, selector, inverse=False):
        """
        Find and return an elements by a given selector.
        """
        if not inverse:
            self.driver.implicitly_wait(5)
        try:
            if by == 'link_text':
                el = self.driver.find_element_by_link_text(selector)
            elif by == 'tag_name':
                el = self.driver.find_element_by_tag_name(selector)
            elif by == 'class_name':
                el = self.driver.find_element_by_class_name(selector)
            elif by == 'xpath':
                el = self.driver.find_element_by_xpath(selector)
            elif by == 'name':
                el = self.driver.find_element_by_name(selector)
            elif by == 'id':
                el = self.driver.find_element_by_id(selector)
            else:
                self.fail('"%s" is not a valid "by" to find the element.' % by)
        except NoSuchElementException:
            if inverse is True:
                return
            self.fail('Element "%s" not found.' % selector)
        if inverse is True:
            self.fail('Element "%s" was unexpectedly found.' % selector)
        return el

    def els(self, by, selector):
        """
        Find and return multiple elements by a given selector.
        """
        try:
            if by == 'link_text':
                el = self.driver.find_elements_by_link_text(selector)
            elif by == 'tag_name':
                el = self.driver.find_elements_by_tag_name(selector)
            elif by == 'class_name':
                el = self.driver.find_elements_by_class_name(selector)
            elif by == 'xpath':
                el = self.driver.find_elements_by_xpath(selector)
            elif by == 'name':
                el = self.driver.find_elements_by_name(selector)
            else:
                self.fail(
                    '"%s" is not a valid "by" to find the elements.' % by)
        except NoSuchElementException:
            self.fail('Elements "%s" not found.' % selector)
        return el

    def url(self, url):
        return '%s%s' % (self.BASE_URL, url)

    def create_activity(
            self, values={}, no_submit=False, create_inv=False, inv_values={},
            known_inv=[]):
        """

        """
        self.open_form('activities', reset=True)
        if TITLE_LOGIN_VIEW in self.driver.title:
            self.login(form_present=True)

        dd1 = values['dd1'] if 'dd1' in values else '[A] Value A1'
        nf1 = values['nf1'] if 'nf1' in values else 123.45

        map = self.el('class_name', 'olMapViewport')
        map_click = ActionChains(self.driver).move_to_element_with_offset(
            map, random.randrange(map.size.get('width', 10) - 9),
            random.randrange(map.size.get('height', 10) - 9)).click()
        map_click.perform()
        self.el(
            'xpath', "//select[@name='[A] Dropdown 1']/option[@value='%s']"
            % dd1).click()
        self.el('id', 'activityformstep_2').click()

        self.el('xpath', "//input[@name='[A] Numberfield 1']").send_keys(
            str(nf1))

        if create_inv is True:
            self.el('id', 'activityformstep_3').click()
            inv_button = self.els('class_name', 'accordion-toggle')
            for btn in inv_button:
                btn.click()
                time.sleep(1)
            if len(known_inv) > 0:
                for k in known_inv:
                    self.el('class_name', 'ui-autocomplete-input').\
                        send_keys(k['name'])
                    self.el('xpath', "//a[contains(text(), '%s')]" %
                            k['name']).click()
            else:
                self.el('name', 'createinvolvement_primaryinvestor').\
                    click()
                self.create_stakeholder(
                    values=inv_values, form_present=True, return_uid=False)

        if 'cat4' in values:
            self.el('id', 'activityformstep_53').click()
            for key in values.get('cat4', {}):
                self.el('xpath', "//select[@name='%s']/option[@value=%s]"
                        % (key, values['cat4'][key])).click()

        if no_submit:
            return

        return self.submit_activity()

    def submit_activity(self):
        self.el('id', 'activityformsubmit').click()

        link = self.el('link_text', LINK_VIEW_DEAL)
        link_href = link.get_attribute('href')
        uid = link_href.split('/')[len(link_href.split('/')) - 1]

        return uid

    def create_stakeholder(
            self, values={}, form_present=False, return_uid=True):
        """

        """
        if not form_present:
            self.open_form('stakeholders', reset=True)
            if TITLE_LOGIN_VIEW in self.driver.title:
                self.login(form_present=True)

        tf1 = values.get('tf1', 'Stakeholder Name')
        nf1 = values.get('nf1', 234.5)

        self.el(
            'xpath', "//input[@name='[SH] Textfield 1']").send_keys(tf1)
        self.el('id', 'stakeholderformstep_15').click()
        self.el('xpath', "//input[@name='[SH] Numberfield 1']").send_keys(
            str(nf1))

        self.el('id', 'stakeholderformsubmit').click()
        self.driver.implicitly_wait(5)

        if return_uid is True:
            link = self.el('link_text', LINK_VIEW_STAKEHOLDER)
            link_href = link.get_attribute('href')
            uid = link_href.split('/')[len(link_href.split('/')) - 1]

            return uid

    def review(self, item_type, uid, reject=False, with_involvement=False):

        self.check_item_type(item_type)
        self.driver.get(self.url('/%s/review/%s' % (item_type, uid)))

        # with_involvement is only valid vor Activities
        if with_involvement is True and item_type == 'activities':
            self.el(
                'xpath',
                "//a[contains(@href, '/stakeholders/review/')]").click()
            self.el(
                'xpath',
                "//button[contains(concat(' ', @class, ' '), ' btn-success ') "
                "and contains(text(), '%s')]" % BUTTON_APPROVE).click()

        if not reject:
            self.el(
                'xpath',
                "//button[contains(concat(' ', @class, ' '), ' btn-success ') "
                "and contains(text(), '%s')]" % BUTTON_APPROVE).click()
        else:
            # TODO
            self.fail(
                'Review decision "reject" is not yet implemented in the '
                'functional tests')

    def open_form(self, item_type, uid=None, reset=True):
        self.check_item_type(item_type)
        url = '/%s/form' % item_type
        if uid is not None:
            url = '/%s/form/%s' % (item_type, uid)
        if reset is True:
            url = '%s%s' % ('/form/clearsession/%s/form?url=' % item_type, url)
        self.driver.get(self.url(url))

    def open_details(self, item_type, uid):
        self.check_item_type(item_type)
        self.driver.get(self.url('/%s/html/%s' % (item_type, uid)))

    def get_existing_item(self, item_type, grid_present=False):
        def get_item(lines):
            r = list(range(1, lines))
            random.shuffle(r)
            for i in r:
                value_1 = self.el(
                    'xpath', "//table/tbody/tr[%s]/td[3]" % i).text
                if value_1 == 'Unknown':
                    continue
                uid_href = self.el(
                    'xpath', "//table/tbody/tr[%s]/td[1]/a" % i).get_attribute(
                        'href')
                uid = uid_href.split('/')[len(uid_href.split('/')) - 1]
                return uid, value_1
            return None, None
        self.check_item_type(item_type)
        if grid_present is False:
            self.login(self.url('/%s/html' % item_type))
        try:
            self.el('tag_name', 'tr')
        except:
            if item_type == 'activities':
                self.create_activity()
            else:
                self.create_stakeholder()
            self.login(self.url('/%s/html' % item_type))
        lines = len(self.els('tag_name', 'tr'))
        return get_item(lines)

    def change_profile(
            self, new_profile, old_profile=None, gui=False, redirect=None):
        """
        Change the profile
        """
        if gui is True:
            if old_profile == 'global':
                old_profile = 'select profile'
            self.el('link_text', old_profile.upper()).click()
            self.el('link_text', new_profile.upper()).click()
            if redirect is not None:
                self.driver.get(self.url(redirect))
        else:
            if redirect is None:
                self.driver.get(
                    self.driver.current_url + '?_PROFILE_=%s' % new_profile)
            else:
                self.driver.get(
                    self.url(redirect + '?_PROFILE_=%s' % new_profile))

    def check_status(self, status):
        if status == 'pending':
            try:
                pending = self.driver.find_element_by_tag_name('h4')
                if TEXT_PENDING_VERSION not in pending.text:
                    return False
            except NoSuchElementException:
                return False
            return True
        if status == 'deleted':
            try:
                note = self.driver.find_element_by_tag_name('h4')
                if TEXT_INACTIVE_VERSION not in note.text:
                    return False
            except NoSuchElementException:
                return False
            return True
        else:
            self.fail('Unknown status: "%s"' % status)

    def find_text(self, text, count=None):
        elements = self.els('xpath', "//*[contains(text(), '%s')]" % text)
        if count is None:
            self.assertTrue(
                len(elements) > 0, 'Text "%s" not found on page' % text)
        else:
            self.assertEqual(
                len(elements), count,
                'Expected appearances of text "%s" on page: %s, found it %s '
                'times' % (text, count, len(elements)))

    def check_item_type(self, item_type):
        valid = ['activities', 'stakeholders']
        self.assertIn(
            item_type, valid, '"%s" is not a valid item_type. Try one of %s'
            % (item_type, ', '.join(valid)))
