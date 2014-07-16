from ..base import *

def doLogin(testcase, redirect=None):
    params = {
        'login': USERNAME, 
        'password': PASSWORD, 
        'form.submitted': 'true'
    }
    res = testcase.app.post('/login', params=params)
    return res.follow()
    
def getStatusFromItemJSON(json, pos=0):
    return json['data'][pos]['status']

def getInvolvementsFromItemJSON(json, pos=0):
    try:
        return json['data'][pos]['involvements']
    except KeyError:
        return []
