# Some helper functions for the Activity tests.
import decimal
import random


def getReadManyActivities(testcase, format):
    if format == 'json':
        res = testcase.app.get('/activities/json')
        return res.json
    elif format == 'html':
        res = testcase.app.get('/activities/html')
        return res
    else:
        testcase.fail('Unknown format: %s' % format)

def getReadOneActivity(testcase, uid, format):
    if format == 'json':
        res = testcase.app.get('/activities/json/%s' % uid)
        return res.json
    else:
        testcase.fail('Unknown format: %s' % format)

def createActivity(testcase, diff, returnUid=False):
    ret = testcase.app.post_json('/activities', diff)
    if returnUid is True:
        return ret.json['data'][0]['id']
    return ret

def reviewActivity(testcase, identifier, reviewDecision='approve', version=1, 
    comment='', expectErrors=False):
    return testcase.app.post('/activities/review', {
        'identifier': identifier,
        'version': version,
        'review_decision': reviewDecision,
        'review_comment': comment
    }, expect_errors=expectErrors)

def createGeometry(country):
    if country == 'laos':
        return {
            'type': 'Point',
            'coordinates': [
              float(102 + decimal.Decimal(str(random.random()))),
              float(19 + decimal.Decimal(str(random.random())))
            ]
        }
    else:
        raiseException('Invalid country for geometry: %s' % country)

def getNewActivityDiff(type=1, data={}):
    """
    1: Complete Activity with its Point somewhere in Laos.
    2: Incomplete Activity with its Point somewhere in Laos.
    3: Complete Activity with an Involvement (from 'data' dict)
    """
    if type == 1:
        return {
            'activities': [
                {
                  'geometry': createGeometry('laos'),
                  'taggroups': [
                    {
                      'main_tag': {
                        'value': u'[A] Value A1', 
                        'key': u'[A] Dropdown 1'
                      }, 
                      'tags': [
                        {
                          'value': u'[A] Value A1', 
                          'key': u'[A] Dropdown 1', 
                          'op': 'add'
                        }
                      ], 
                      'op': 'add'
                    }, {
                      'main_tag': {
                        'value': 123.45, 
                        'key': u'[A] Numberfield 1'
                      },  
                      'tags': [
                        {
                          'value': 123.45, 
                          'key': u'[A] Numberfield 1',
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
            'activities': [
                {
                  'geometry': createGeometry('laos'),
                  'taggroups': [
                    {
                      'main_tag': {
                        'value': u'[A] Value A1', 
                        'key': u'[A] Dropdown 1'
                      }, 
                      'tags': [
                        {
                          'value': u'[A] Value A1', 
                          'key': u'[A] Dropdown 1', 
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
    elif type == 3:
        return {
            'activities': [
                {
                  'geometry': createGeometry('laos'),
                  'taggroups': [
                    {
                      'main_tag': {
                        'value': u'[A] Value A1', 
                        'key': u'[A] Dropdown 1'
                      }, 
                      'tags': [
                        {
                          'value': u'[A] Value A1', 
                          'key': u'[A] Dropdown 1', 
                          'op': 'add'
                        }
                      ], 
                      'op': 'add'
                    }, {
                      'main_tag': {
                        'value': 123.45, 
                        'key': u'[A] Numberfield 1'
                      },  
                      'tags': [
                        {
                          'value': 123.45, 
                          'key': u'[A] Numberfield 1',
                          'op': 'add'
                        }
                      ], 
                      'op': 'add'
                    }
                  ], 
                  'version': 1,
                  'stakeholders': [
                    {
                      'id': data['id'],
                      'version': data['version'],
                      'role': data['role'],
                      'op': 'add'
                    }
                  ]
                }
            ]
        }
    else:
        raiseException('Invalid type for Activity diff: %s' % type)