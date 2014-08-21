import decimal
import random
from unittest import TestCase

from ..base import (
    FEEDBACK_INVOLVED_ACTIVITIES_CANNOT_BE_REVIEWED,
    FEEDBACK_INVOLVED_STAKEHOLDERS_CANNOT_BE_REVIEWED,
    PASSWORD,
    USERNAME,
)


class LmkpTestCase(TestCase):

    def login(self, redirect=None):
        params = {
            'login': USERNAME,
            'password': PASSWORD,
            'form.submitted': 'true'
        }
        res = self.app.post('/login', params=params)
        return res.follow()

    def create(self, item_type, diff, return_uid=False):
        url = get_base_url_by_item_type(item_type)
        ret = self.app.post_json(url, diff)
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

    def read_many(self, item_type, format):
        url = get_base_url_by_item_type(item_type)
        if format == 'json':
            res = self.app.get('%s/json' % url)
            return res.json
        elif format == 'html':
            res = self.app.get('%s/html' % url)
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
        if item_type == 'a' and reason == 1:
            # The Activity cannot be reviewed because of the Stakeholder. In
            # this case, the response still returns a valid HTTP status code
            # and redirects to the history page, but flashes an error message
            # and does not approve the item.
            response = response.follow()
            self.assertEqual(200, response.status_int)
            response.mustcontain(
                FEEDBACK_INVOLVED_STAKEHOLDERS_CANNOT_BE_REVIEWED)
        elif item_type == 'sh' and reason == 1:
            # The Stakeholder cannot be reviewed because it contains
            # involvement changes. As above, a valid HTTP status is returned.
            response = response.follow()
            self.assertEqual(200, response.status_int)
            response.mustcontain(
                FEEDBACK_INVOLVED_ACTIVITIES_CANNOT_BE_REVIEWED)


def get_status_from_item_json(json, pos=0):
    return json['data'][pos]['status']


def get_involvements_from_item_json(json, pos=0):
    try:
        return json['data'][pos]['involvements']
    except KeyError:
        return []


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
