import pytest

from .base import (
    LmkpTestCase
)
from ..base import (
    PASSWORD,
    USERNAME
)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
class LoginTests(LmkpTestCase):

    def test_login_page_is_available(self):
        """
        The Login page is available.
        """
        res = self.app.get('/login')
        self.assertEqual(res.status_int, 200)
        res.mustcontain('Login')

    def test_login_form_cannot_be_submitted_empty(self):
        """
        The Login form cannot be submitted with empty values.
        """
        res = self.app.get('/login')
        form = res.form
        form['login'] = ''
        form['password'] = ''
        res = form.submit('form.submitted')

        self.assertEqual(res.status_int, 200)
        res.mustcontain('Login failed')

    def test_login_form_submit(self):
        """
        The Login form can be submitted with correct credentials.
        """
        res = self.app.get('/login')
        form = res.form

        form['login'] = USERNAME
        form['password'] = PASSWORD
        res = form.submit('form.submitted')
        self.assertEqual(res.status_int, 302)
        res = res.follow()

        self.assertEqual(res.status_int, 200)
        res.mustcontain('Land Observatory')
        self.assertNotIn(b'Login', res.body)
        res.mustcontain(USERNAME)
