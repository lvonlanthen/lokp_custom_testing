import pytest
from mock import patch
from pyramid import testing

from lmkp.authentication import (
    get_user_privileges,
)
from ..integration_tests.base import (
    LmkpTestCase,
)
from ..base import get_settings


@pytest.mark.unittest
@pytest.mark.authentication
class AuthenticationGetUserPrivilegesTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.authentication.effective_principals')
    def test_get_user_privileges_calls_effective_principals(
            self, mock_effective_principals):
        get_user_privileges(self.request)
        mock_effective_principals.assert_called_once_with(self.request)

    @patch('lmkp.authentication.effective_principals')
    def test_get_user_privileges_returns_none_if_not_logged_in(
            self, mock_effective_principals):
        mock_effective_principals.return_value = []
        logged_in, is_moderator = get_user_privileges(self.request)
        self.assertIsNone(logged_in)
        self.assertIsNone(is_moderator)

    @patch('lmkp.authentication.effective_principals')
    def test_get_user_privileges_returns_none_if_not_logged_in_2(
            self, mock_effective_principals):
        mock_effective_principals.return_value = ['foo', 'bar']
        logged_in, is_moderator = get_user_privileges(self.request)
        self.assertFalse(logged_in)
        self.assertFalse(is_moderator)

    @patch('lmkp.authentication.effective_principals')
    def test_get_user_privileges_returns_logged_in(
            self, mock_effective_principals):
        mock_effective_principals.return_value = [
            'system.Authenticated', 'group:moderators']
        logged_in, is_moderator = get_user_privileges(self.request)
        self.assertTrue(logged_in)
        self.assertTrue(is_moderator)

    @patch('lmkp.authentication.effective_principals')
    def test_get_user_privileges_returns_is_moderator(
            self, mock_effective_principals):
        mock_effective_principals.return_value = ['system.Authenticated']
        logged_in, is_moderator = get_user_privileges(self.request)
        self.assertTrue(logged_in)
        self.assertFalse(is_moderator)
