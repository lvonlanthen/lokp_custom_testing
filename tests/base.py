# Login credentials for the test
USERNAME = 'admin'
PASSWORD = 'asdfasdf'

# Strings needed during testing as found in the templates
BUTTON_APPROVE = 'Approve'
BUTTON_DENY = 'Deny'
BUTTON_DOWNLOAD = 'Download'
BUTTON_LOGIN = 'Login'.upper()
BUTTON_REMOVE_STAKEHOLDER = 'Remove the Stakeholder'
BUTTON_SHOW_ONLY_PENDING = 'Show only pending'.upper()
BUTTON_USERNAME = USERNAME.upper()
PROJECT_TITLE = 'Land Observatory'
FEEDBACK_FORM_ERROR = 'There was a problem with your submission'
FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED = \
    'At least one of the involvements prevents automatic revision.'
FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED_FROM_STAKEHOLDER = \
    'This version contains changed involvements which prevent automatic '
'revision.'
FEEDBACK_INVOLVED_ACTIVITIES_CANNOT_BE_REVIEWED = \
    'At least one of the involved Activities cannot be reviewed'
FEEDBACK_INVOLVED_STAKEHOLDERS_CANNOT_BE_REVIEWED = \
    'At least one of the involved Stakeholders cannot be reviewed'
FEEDBACK_LOGIN_FAILED = 'Login failed'
FEEDBACK_LOGIN_NEEDED = 'Please login'
FEEDBACK_MANDATORY_KEYS_MISSING = 'Not all mandatory keys are provided'
FEEDBACK_NO_GEOMETRY_PROVIDED = 'No geometry provided!'
FEEDBACK_NO_VERSION = 'No version to display.'
FEEDBACK_NOT_VALID_FORMAT = 'Not a valid format'
FEEDBACK_USER_SETTINGS_UPDATED = 'Your user settings were updated.'
FILTER_MAP_EXTENT = 'Map Extent'
FILTER_PROFILE = 'Profile'
LINK_DEAL_SHOW_INVOLVEMENT = 'View Stakeholder'
LINK_REVIEW = 'Review'
LINK_STAKEHOLDER_SHOW_INVOLVEMENT = 'View Deal'
LINK_VIEW_DEAL = 'View the Deal.'
LINK_VIEW_STAKEHOLDER = 'View the Stakeholder'
STATUS_ACTIVE = 'active'
STATUS_DELETED = 'deleted'
STATUS_EDITED = 'edited'
STATUS_INACTIVE = 'inactive'
STATUS_PENDING = 'pending'
TEXT_INACTIVE_VERSION = 'TODO'
TEXT_PENDING_VERSION = 'Pending version'.upper()
TITLE_DEAL_DETAILS = 'Activity Details'
TITLE_DEAL_EDITOR = 'Deal Editor'
TITLE_DEAL_MODERATION = 'Deal Moderation'
TITLE_DEAL_DOWNLOAD = 'Download Activities'
TITLE_GRID_ACTIVITIES = 'Activities'.upper()
TITLE_GRID_STAKEHOLDERS = 'Stakeholders'.upper()
TITLE_HISTORY_VIEW = 'History'
TITLE_LOGIN_VIEW = 'Login'
TITLE_MAP_VIEW = 'Map View'
TITLE_NOTHING_FOUND = 'Nothing found'
TITLE_STAKEHOLDER_DETAILS = 'Stakeholder Details'
TITLE_STAKEHOLDER_EDITOR = 'Stakeholder Editor'
TITLE_STAKEHOLDER_MODERATION = 'Investor Moderation'
TITLE_STAKEHOLDER_DOWNLOAD = 'Download Stakeholders'
TITLE_USER_ACCOUNT_VIEW = 'User Account'

from pyramid.paster import get_appsettings


def get_settings():
    config_uri = 'integration_tests.ini'
    return get_appsettings(config_uri)
