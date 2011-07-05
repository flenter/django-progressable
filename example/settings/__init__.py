import djcelery
djcelery.setup_loader()

try:
    from settings.base import *
except ImportError, e:
    print "#"*80
    print """
    Fatal: could not import settings.base. Forgot to move settings.py to 
    settings/base.py ?
    """
    print "#"*80
    raise e

import sys

from settings.celery_settings import *

from settings.shared import *

if 'runserver' in sys.argv or 'runserver_plus':
  from settings.development import *
else:
  from settings.live import *


