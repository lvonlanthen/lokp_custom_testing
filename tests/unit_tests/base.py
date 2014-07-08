CONFIG_FILE = 'unit_tests.ini'
USERNAME = 'admin'
PASSWORD = 'asdf'

def doLogin(testcase, redirect=None):
    params = {
        'login': USERNAME, 
        'password': PASSWORD, 
        'form.submitted': 'true'
    }
    res = testcase.app.post('/login', params=params)
    return res.follow()
    
def getStatusFromItemJSON(json):
    return json['data'][0]['status']

def getInvolvementsFromItemJSON(json):
    return json['data'][0]['involvements']