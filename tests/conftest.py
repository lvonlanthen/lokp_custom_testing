# Somewhat based on:
# http://blog.lostpropertyhq.com/testing-with-sqlalchemy-and-pytest/
# and
# http://blogs.gnome.org/danni/2012/11/15/combining-py-test-and-
# selenium-to-test-webapps/

import pytest
import os
from pyramid.paster import get_app
from pyramid.paster import get_appsettings
from selenium import webdriver
from sqlalchemy import engine_from_config
from webtest.app import TestApp

from lmkp.scripts.populate import _populate
from lmkp.models import meta

# Specify the INI configuration files for the tests to run.
INTEGRATION_TESTS_INI = 'integration_tests.ini'
FUNCTIONAL_TESTS_INI = 'functional_testing.ini'

# Activate the browsers you want to run the functional tests with.
browsers = {
    # Firefox: No plugins needed.
    # 'firefox': webdriver.Firefox,

    # Internet Explorer
    # In order to run this on Windows, download IEDriverServer from
    # http://selenium-release.storage.googleapis.com/index.html and add it to
    # the PATH.
    # See also: https://code.google.com/p/selenium/wiki/InternetExplorerDriver
    # If typing runs very slow and you are running the 64bit version of the
    # IEDriver, try using the 32bit version instead.
    # 'ie': webdriver.Ie,

    # Chrome
    # In order to run this on Windows, download ChromeDriver from
    # http://chromedriver.storage.googleapis.com/index.html and add it to the
    # PATH.
    # See also: http://code.google.com/p/selenium/wiki/ChromeDriver
    # 'chrome': webdriver.Chrome,
}


@pytest.fixture(scope='session')
def connection(request):
    """
    Fixture to set up a database connection and create the tables.
    """
    config_uri = INTEGRATION_TESTS_INI
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')

    meta.Base.metadata.create_all(engine)
    connection = engine.connect()
    meta.DBSession.registry.clear()
    meta.DBSession.configure(bind=connection)
    meta.Base.metadata.bind = engine

    _populate(engine, settings)

    request.addfinalizer(meta.Base.metadata.drop_all)
    return connection


@pytest.fixture
def db_session(request, connection):
    """
    Fixture to roll back the database after tests. Also populates database with
    initial keys, values and other data.
    """
    from transaction import abort
    trans = connection.begin()

    here = os.path.dirname(__file__)
    location = os.path.join(here, '..', 'scripts', 'populate_keyvalues.sql')

    sql_file = open(location, 'r')
    sql_query = sql_file.read()
    sql_file.close()
    connection.execute(sql_query)

    request.addfinalizer(trans.rollback)
    request.addfinalizer(abort)

    from lmkp.models.meta import DBSession
    return DBSession


@pytest.fixture(scope='function')
def app(request, db_session):
    """
    Use this fixture to retreive a TestApp object which can be used as self.app
    in the test functions.
    """
    request.cls.app = TestApp(get_app(INTEGRATION_TESTS_INI))
    request.cls.db_session = db_session
    return request


@pytest.fixture(scope='function')
def app_functional(request, db_session):
    request.cls.app = TestApp(get_app(FUNCTIONAL_TESTS_INI))
    request.cls.db_session = db_session
    request.cls.driver = webdriver.Firefox()
    request.addfinalizer(lambda *args: request.cls.driver.quit())
    return request
