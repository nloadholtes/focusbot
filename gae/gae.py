import datetime

from google.appengine.api import datastore_types
from google.appengine.api import xmpp
from google.appengine.ext import ndb
from google.appengine.ext.webapp import xmpp_handlers
import webapp2
from webapp2_extras import jinja2