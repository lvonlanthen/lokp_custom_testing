# LOKP Customization 
## for testing purposes only!

---

Please refer to the documentation found at http://lokp.rtfd.org.

Clone this repository in the customization folder (lmkp/customization) of an
instance of the Land Observatory Knowledge Platform
(https://github.com/CDE-UNIBE/lokp).

Don't forget to adapt the settings in the application's .ini file.

### Tests

#### Setup:

The following configuration files and databases are needed:

**Database**

* `<integration_test_db>`: The database for the integration tests. This is 
  basically an empty database, only the necessary schemas (`data` and `context` 
  need to be created. This database is emptied after each test run.
* `<functional_test_db>`: The database for the functional tests. This database 
  not only requires the necesssary schemas (`data` and `context`), but also some
  values in it. Use `populate_lmkp functional_tests.ini` to create the tables 
  and run `scripts/populate_keyvalues.sql` to populate the database. This 
  database is not emptied after the test runs.

**Configuration files**

* `integration_tests.ini`: Points to the database for the integration tests (see
  above).
* `functional_tests.ini`: Points to the database for the functional tests (see 
  above).

#### Run
To run the tests, use:

```bash
# Run all tests
py.test lmkp/customization/testing/tests
# Run only selected tests based on markers
py.test lmkp/customization/testing/tests -m "functional"  # Only functional tests
py.test lmkp/customization/testing/tests -m "integration" # Only integration tests
# ...
```