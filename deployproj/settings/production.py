from deployproj.settings.staging import *

# There should be only minor differences from staging

DATABASES['default']['NAME'] = 'deployproj_production'

EMAIL_SUBJECT_PREFIX = '[Deployproj Prod] '

