#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/ASMD/")

from ASMD import app as application
application.secret_key = 'ef$74c00E9_0'
