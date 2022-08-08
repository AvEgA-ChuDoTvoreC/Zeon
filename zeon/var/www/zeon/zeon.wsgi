#!/usr/bin/python3
import sys


# Add <path> to PYTHONPATH to let python find packages
sys.path.insert(0, '/var/www/zeon')

# This import is for Apache2 which search object 'application' in *.wsgi file to run server.
from run import app as application
