from deployproj.settings.staging import *

# There should be only minor differences from staging

DATABASES['default']['NAME'] = 'rapidsms'

EMAIL_SUBJECT_PREFIX = '[Deployproj Prod] '
