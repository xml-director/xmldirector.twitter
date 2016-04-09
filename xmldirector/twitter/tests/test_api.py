# -*- coding: utf-8 -*-

################################################################
# xmldirector.twitter
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################


import os
import json
import zipfile
import tempfile
import requests

import transaction
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD

from xmldirector.plonecore.tests.apibase import TestBase


cwd = os.path.dirname(__file__)


class TestCRexAPI(TestBase):

    def test_dummy(self):
        pass

