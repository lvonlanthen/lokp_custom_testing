# Some helper functions for the Stakeholder tests.

def getReadManyStakeholders(testcase, format):
    if format == 'json':
        res = testcase.testapp.get('/stakeholders/json')
        return res.json
    elif format == 'html':
        res = testcase.testapp.get('/stakeholders/html')
        return res
    else:
        testcase.fail('Unknown format: %s' % format)

def getReadOneStakeholder(testcase, uid, format):
    if format == 'json':
        res = testcase.testapp.get('/stakeholders/json/%s' % uid)
        return res.json
    else:
        testcase.fail('Unknown format: %s' % format)

def createStakeholder(testcase, diff, returnUid=False):
    ret = testcase.testapp.post_json('/stakeholders', diff)
    if returnUid is True:
        return ret.json['data'][0]['id']
    return ret

def reviewStakeholder(testcase, identifier, reviewDecision='approve', version=1, 
    comment='', expectErrors=False):
    return testcase.testapp.post('/stakeholders/review', {
        'identifier': identifier,
        'version': version,
        'review_decision': reviewDecision,
        'review_comment': comment
    }, expect_errors=expectErrors)

def getStakeholderDiff(type=1):
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