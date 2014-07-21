import time
from selenium.common.exceptions import NoSuchElementException    

from ..base import *

BASE_URL = 'http://localhost:6543'

def openItemDetailsPage(testcase, itemType, uid):
    checkValidItemType(testcase, itemType)
    testcase.driver.get(createUrl('/%s/html/%s' % (itemType, uid)))

def openItemFormPage(testcase, itemType, uid=None, reset=True):
    checkValidItemType(testcase, itemType)
    url = '/%s/form' % itemType
    if uid is not None:
        url = '/%s/form/%s' % (itemType, uid)
    if reset is True:
        url = '%s%s' % ('/form/clearsession/%s/form?url=' % itemType, url)
    testcase.driver.get(createUrl(url))

def checkValidItemType(testcase, itemType):
    valid = ['activities', 'stakeholders']
    testcase.assertIn(itemType, valid, '"%s" is not a valid itemType. Try one of %s' % (itemType, ', '.join(valid)))

def createUrl(url):
    return '%s%s' % (BASE_URL, url)

def checkEl(testcase, by, selector):
    try:
        getEl(testcase, by, selector)
    except:
        return False
    return True

def getEl(testcase, by, selector, inverse=False):
    try:
        if by == 'link_text':
            el = testcase.driver.find_element_by_link_text(selector)
        elif by == 'tag_name':
            el = testcase.driver.find_element_by_tag_name(selector)
        elif by == 'class_name':
            el = testcase.driver.find_element_by_class_name(selector)
        elif by == 'xpath':
            el = testcase.driver.find_element_by_xpath(selector)
        elif by == 'name':
            el = testcase.driver.find_element_by_name(selector)
        else:
            testcase.fail('"%s" is not a valid "by" to find the element.' % by)
    except NoSuchElementException:
        if inverse is True:
            return
        testcase.fail('Element "%s" not found.' % selector)
    if inverse is True:
        testcase.fail('Element "%s" was unexpectedly found.' % selector)
    return el

def checkIsPending(testcase):
    try:
        pending = testcase.driver.find_element_by_tag_name('h4')
        if TEXT_PENDING_VERSION not in pending.text:
            return False
    except NoSuchElementException:
        return False
    return True

def findTextOnPage(testcase, text, count=None):
    els = testcase.driver.find_elements_by_xpath("//*[contains(text(), '%s')]" % text)
    if count is None:
        testcase.assertTrue(len(els) > 0, 'Text "%s" not found on page' % text)
    else:
        testcase.assertEqual(len(els), count, 'Expected appearances of text "%s" on page: %s, found it %s times' % (text, count, len(els)))

def doLogin(testcase, redirect=None, gotForm=False, password=None):
    """
    Do the Login procedure.
    """
    if gotForm is False:
        testcase.driver.get(createUrl('/login'))
    if checkEl(testcase, 'name', 'login') is False:
        # Already logged in
        if redirect is not None:
            testcase.driver.get(redirect)
        return
    pwd = PASSWORD if password is None else password
    testcase.driver.find_element_by_name('login').send_keys(USERNAME)
    testcase.driver.find_element_by_name('password').send_keys(pwd)
    if redirect is not None:
        testcase.driver.execute_script(\
            "document.getElementsByName('came_from')[0].value='%s'" % redirect)
    testcase.driver.find_element_by_name('form.submitted').click()

def doCreateActivity(testcase, dd1='[A] Value A1', nf1=123.45, cat4={}, 
    noSubmit=False, createSH=False, shValues={}, knownSh=[]):
    openItemFormPage(testcase, 'activities', reset=True)
    if TITLE_LOGIN_VIEW in testcase.driver.title:
        doLogin(testcase, gotForm=True)
    testcase.driver.find_element_by_class_name('olMapViewport').click()
    testcase.driver.find_element_by_xpath("//select[@name='[A] Dropdown 1']/option[@value='%s']" % dd1).click()
    testcase.driver.find_element_by_id('activityformstep_2').click()
    testcase.driver.find_element_by_xpath("//input[@name='[A] Numberfield 1']").send_keys(str(nf1))
    
    if createSH is True:
        testcase.driver.find_element_by_id('activityformstep_3').click()
        shbtn = testcase.driver.find_elements_by_class_name('accordion-toggle')
        for el in shbtn:
            el.click()
            time.sleep(1)
        if len(knownSh) > 0:
            for k in knownSh:
                getEl(testcase, 'class_name', 'ui-autocomplete-input').send_keys(k['name'])
                testcase.driver.implicitly_wait(10)
                getEl(testcase, 'xpath', "//a[contains(text(), '%s')]" % k['name']).click()
        else:
            testcase.driver.find_element_by_name('createinvolvement_primaryinvestor').click()
            doCreateStakeholder(testcase, shValues=shValues)
    
    if cat4 != {}:
        testcase.driver.find_element_by_id('activityformstep_53').click()
        for key in cat4:
            testcase.driver.find_element_by_xpath("//select[@name='%s']/option[@value=%s]" % (key, cat4[key])).click()
    
    if noSubmit is True:
        return
        
    testcase.driver.find_element_by_id('activityformsubmit').click()
    
    link = testcase.driver.find_element_by_link_text(LINK_VIEW_DEAL).get_attribute('href')
    uid = link.split('/')[len(link.split('/'))-1]
    
    return uid

def doActivitySubmit(testcase):
    testcase.driver.find_element_by_id('activityformsubmit').click()
    
    link = testcase.driver.find_element_by_link_text(LINK_VIEW_DEAL).get_attribute('href')
    uid = link.split('/')[len(link.split('/'))-1]
    
    return uid

def doCreateStakeholder(testcase, tf1='Stakeholder Name', nf1=234.5, 
    shValues={}):
    
    if shValues != {}:
        tf1 = shValues['tf1'] if 'tf1' in shValues else tf1
        nf1 = shValues['nf1'] if 'nf1' in shValues else nf1
    
    testcase.driver.find_element_by_xpath("//input[@name='[SH] Textfield 1']").send_keys(tf1)
    testcase.driver.find_element_by_id('stakeholderformstep_15').click()
    testcase.driver.find_element_by_xpath("//input[@name='[SH] Numberfield 1']").send_keys(str(nf1))
    testcase.driver.find_element_by_id('stakeholderformsubmit').click()


def doReview(testcase, aOrSh, uid, reject=False, withInv=False):
    
    type = 'activities'
    if aOrSh == 'sh':
        type = 'stakeholders'
    
    testcase.driver.get(createUrl('/%s/review/%s' % (type, uid)))
    
    # withInv is only valid vor Activities
    if withInv is True and aOrSh == 'a':
        testcase.driver.find_element_by_xpath("//a[contains(@href, '/stakeholders/review/')]").click()
        testcase.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE).click()
        testcase.driver.find_element_by_link_text('Click here to return to the Activity and review it.').click()
    
    if reject is False:
        testcase.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE).click()
    else:
        # TODO
        pass
