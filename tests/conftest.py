# Somewhat based on:
# http://blog.lostpropertyhq.com/testing-with-sqlalchemy-and-pytest/

import pytest
import os
from pyramid.paster import get_app
from pyramid.paster import get_appsettings
from sqlalchemy import engine_from_config
from webtest import TestApp

from lmkp.scripts.populate import _populate
from lmkp.models import meta

INTEGRATION_TESTS_INI = 'integration_tests.ini'
FUNCTIONAL_TESTS_INI = 'functional_tests.ini'

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
    return request
