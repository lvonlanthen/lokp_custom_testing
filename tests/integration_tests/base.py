import decimal
import random
from unittest import TestCase

from ..base import (
    FEEDBACK_INVOLVED_ACTIVITIES_CANNOT_BE_REVIEWED,
    FEEDBACK_INVOLVED_STAKEHOLDERS_CANNOT_BE_REVIEWED,
    PASSWORD,
    USERNAME,
)
from lmkp.views.form import checkValidItemjson
from lmkp.views.form_config import getCategoryList


class LmkpTestCase(TestCase):

    def login(self, redirect=None):
        params = {
            'login': USERNAME,
            'password': PASSWORD,
            'form.submitted': 'true'
        }
        res = self.app.post('/login', params)
        return res.follow()

    def create(
            self, item_type, diff, return_uid=False, expect_errors=False):
        url = get_base_url_by_item_type(item_type)
        ret = self.app.post_json(url, diff, expect_errors=expect_errors)
        if return_uid is True:
            return ret.json['data'][0]['id']
        return ret

    def read_one(self, item_type, uid, format):
        url = get_base_url_by_item_type(item_type)
        if format == 'json':
            res = self.app.get('%s/json/%s' % (url, uid))
            return res.json
        elif format == 'html':
            return self.app.get('%s/html/%s' % (url, uid))
        else:
            self.fail('Unknown format: %s' % format)

    def read_many(self, item_type, format, params={}):
        url = get_base_url_by_item_type(item_type)
        url_params = [
            '%s=%s' % (key, value) for key, value in params.iteritems()]
        if format == 'json':
            res = self.app.get('%s/json?%s' % (url, '&'.join(url_params)))
            return res.json
        elif format == 'html':
            res = self.app.get('%s/html?%s' % (url, '&'.join(url_params)))
            return res
        else:
            self.fail('Unknown format: %s' % format)

    def review(
            self, item_type, identifier, decision='approve', version=1,
            comment='', expect_errors=False):
        url = get_base_url_by_item_type(item_type)
        return self.app.post('%s/review' % url, {
            'identifier': identifier,
            'version': version,
            'review_decision': decision,
            'review_comment': comment
        }, expect_errors=expect_errors)

    def review_not_possible(self, item_type, reason, response):
        item_type = get_valid_item_type(item_type)
        if item_type == 'a':
            # The Activity cannot be reviewed because of the Stakeholder. In
            # this case, the response still returns a valid HTTP status code
            # and redirects to the history page, but flashes an error message
            # and does not approve the item.
            response = response.follow()
            self.assertEqual(200, response.status_int)
            response.mustcontain(
                FEEDBACK_INVOLVED_STAKEHOLDERS_CANNOT_BE_REVIEWED)
        elif item_type == 'sh':
            # The Stakeholder cannot be reviewed because it contains
            # involvement changes. As above, a valid HTTP status is returned.
            response = response.follow()
            self.assertEqual(200, response.status_int)
            response.mustcontain(
                FEEDBACK_INVOLVED_ACTIVITIES_CANNOT_BE_REVIEWED)

    def check_item_json(self, item_type, item_json):
        item_type = get_valid_item_type(item_type)
        if item_type == 'a':
            try:
                category_list = self.a_list
            except AttributeError:
                self.a_list = getCategoryList(self.request, 'activities')
                category_list = self.a_list
        elif item_type == 'sh':
            try:
                category_list = self.sh_list
            except AttributeError:
                self.sh_list = getCategoryList(self.request, 'stakeholders')
                category_list = self.sh_list
        check = checkValidItemjson(category_list, item_json)
        self.assertEqual(
            check.get('errorCount', 0), 0, '%s\n%s' % (item_json, check))


def get_status_from_item_json(json, pos=0):
    return json['data'][pos]['status']


def get_involvements_from_item_json(json, pos=0):
    try:
        return json['data'][pos]['involvements']
    except:
        return []


def get_taggroup_by_main_tag(taggroups_json, key, value=None):
    for tg in taggroups_json:
        if key != tg['main_tag']['key']:
            continue
        if value and value != tg['main_tag']['value']:
            continue
        return tg
    return None


def get_role_id_from_involvement_json(json, pos=0):
    try:
        return json[pos]['role_id']
    except:
        return None


def get_version_from_involvement_json(json, pos=0):
    try:
        return json[pos]['version']
    except:
        return None


def find_key_value_in_taggroups_json(
        taggroups_json, key, value=None, main_tag=False, return_value=False):
    for taggroup in taggroups_json:
        for tag in taggroup['tags']:
            if tag['key'] == key:
                if value and tag['value'] == value:
                    if (main_tag and taggroup['main_tag']['key'] == key
                            and taggroup['main_tag']['value'] == value):
                        if return_value is True:
                            return tag['value']
                        return True
                    else:
                        if return_value is True:
                            return tag['value']
                        return True
                elif (not value and main_tag
                      and taggroup['main_tag']['key'] == key):
                    if return_value is True:
                        return tag['value']
                    return True
                elif not value:
                    if return_value is True:
                        return tag['value']
                    return True
    return False


def get_valid_item_type(item_type):
    if item_type in ['a', 'activity', 'activities']:
        return 'a'
    elif item_type in ['sh', 'stakeholder', 'stakeholders']:
        return 'sh'
    raise Exception('Unknown item type: "{}"'.format(item_type))


def get_base_url_by_item_type(item_type):
    item_type = get_valid_item_type(item_type)
    if item_type == 'a':
        return '/activities'
    else:
        return '/stakeholders'


def create_geometry(country):
    if country == 'laos':
        return {
            'type': 'Point',
            'coordinates': [
                float(102 + decimal.Decimal(str(random.random()))),
                float(19 + decimal.Decimal(str(random.random())))
            ]
        }
    else:
        raise Exception('Invalid country for geometry: %s' % country)
