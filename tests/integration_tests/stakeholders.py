# Some helper functions for the Stakeholder tests.

from ..base import *


def getReadManyStakeholders(testcase, format):
    if format == 'json':
        res = testcase.app.get('/stakeholders/json')
        return res.json
    elif format == 'html':
        res = testcase.app.get('/stakeholders/html')
        return res
    else:
        testcase.fail('Unknown format: %s' % format)

def getReadOneStakeholder(testcase, uid, format):
    if format == 'json':
        res = testcase.app.get('/stakeholders/json/%s' % uid)
        return res.json
    else:
        testcase.fail('Unknown format: %s' % format)

def createStakeholder(testcase, diff, returnUid=False):
    ret = testcase.app.post_json('/stakeholders', diff)
    if returnUid is True:
        return ret.json['data'][0]['id']
    return ret

def reviewStakeholder(testcase, identifier, reviewDecision='approve', version=1, 
    comment='', expectErrors=False):
    return testcase.app.post('/stakeholders/review', {
        'identifier': identifier,
        'version': version,
        'review_decision': reviewDecision,
        'review_comment': comment
    }, expect_errors=expectErrors)

def checkReviewStakeholderNotPossibleBcInvolvements(testcase, response):
    # If a review cannot be done, the response still returns a valid HTTP status
    # code and redirects to the history page, but flashes an error message and 
    # does not approve the item.
    response = response.follow()
    testcase.assertEqual(200, response.status_int)
    response.mustcontain(FEEDBACK_INVOLVED_ACTIVITIES_CANNOT_BE_REVIEWED)

def getEditStakeholderDiff(uid, version=1, type=1):
    """
    1: Add a new Taggroup to Stakeholder (based on type 1 from 
        getNewStakeholderDiff)
    """
    if type == 1:
        return {
            'stakeholders': [
              {
                'taggroups': [
                  {
                    'main_tag': {
                      'value': u'[SH] Value D1', 
                      'key': u'[SH] Checkbox 1'
                    }, 
                    'tags': [
                      {
                        'value': u'[SH] Value D1', 
                        'key': u'[SH] Checkbox 1', 
                        'op': 'add'
                      }
                    ], 
                    'op': 'add'
                  }
                ], 
                'version': version, 
                'id': uid
              }
            ]
          }
    else:
        raiseException('Invalid type for Stakeholder diff: %s' % type)

def getNewStakeholderDiff(type=1):
    """
    1: Complete Stakeholder
    2: Incomplete Stakeholder
    """
    if type == 1:
        return {
            'stakeholders': [
                {
                  'taggroups': [
                    {
                      'main_tag': {
                        'value': 123.0, 
                        'key': u'[SH] Numberfield 1'
                      }, 
                      'tags': [
                        {
                          'value': 123.0, 
                          'key': u'[SH] Numberfield 1', 
                          'op': 'add'
                        }
                      ], 
                      'op': 'add'
                    }, {
                      'main_tag': {
                        'value': u'asdf', 
                        'key': u'[SH] Textfield 1'
                      },  
                      'tags': [
                        {
                          'value': u'asdf', 
                          'key': u'[SH] Textfield 1', 
                          'op': 'add'
                        }
                      ], 
                      'op': 'add'
                    }
                  ], 
                  'version': 1
                }
            ]
        }
    elif type == 2:
        return {
            'stakeholders': [
                {
                  'taggroups': [
                    {
                      'main_tag': {
                        'value': 123.0, 
                        'key': u'[SH] Numberfield 1'
                      }, 
                      'tags': [
                        {
                          'value': 123.0, 
                          'key': u'[SH] Numberfield 1', 
                          'op': 'add'
                        }
                      ], 
                      'op': 'add'
                    }
                  ], 
                  'version': 1
                }
            ]
        }
    else:
        raiseException('Invalid type for Stakeholder diff: %s' % type)