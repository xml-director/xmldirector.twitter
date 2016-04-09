# -*- coding: utf-8 -*-

################################################################
# xmldirector.twitter
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################


from twitter import session

from zope.component import getUtility
from Products.Five.browser import BrowserView
from plone.registry.interfaces import IRegistry
from zope.annotation import IAnnotations

from xmldirector.twitter.interfaces import IDropboxSettings


DROPBOX_TOKEN_KEY = 'xmldirector.twitter.token_key'
DROPBOX_TOKEN_SECRET = 'xmldirector.twitter.token_secret'
DROPBOX_TEMP_TOKEN = 'xmldirector.twitter.oauth_temporary_token'


class DropboxAuthentication(BrowserView):

    def authorize(self, oauth_token):
        
        annotation = IAnnotations(self.context)
        s = self.twitter_session
        a = s.obtain_access_token(annotation[DROPBOX_TEMP_TOKEN])
        token_key, token_secret = a.key, a.secret
        annotation[DROPBOX_TOKEN_KEY] = a.key
        annotation[DROPBOX_TOKEN_SECRET] = a.secret

        self.context.plone_utils.addPortalMessage(u'Dropbox access authorized')
        self.request.response.redirect(self.context.absolute_url() + '/authorize-twitter')

    def deauthorize(self):
        annotation = IAnnotations(self.context)
        try:
            del annotation[DROPBOX_TOKEN_KEY]
        except KeyError:
            pass

        try:
            del annotation[DROPBOX_TOKEN_SECRET]
        except KeyError:
            pass

        self.context.plone_utils.addPortalMessage(u'Dropbox access deauthorized')
        self.request.response.redirect(self.context.absolute_url() + '/authorize-twitter')

    @property
    def twitter_settings(self):
        registry = getUtility(IRegistry)
        return registry.forInterface(IDropboxSettings)

    @property
    def twitter_session(self):
        settings = self.twitter_settings
        return session.DropboxSession(
                settings.twitter_app_key, 
                settings.twitter_app_secret, 
                'twitter')

    def get_oauth_token(self):
        annotation = IAnnotations(self.context)
        return annotation.get(DROPBOX_TOKEN_KEY)

    def get_oauth_url(self):
        s = self.twitter_session
        t = s.obtain_request_token()
        IAnnotations(self.context)[DROPBOX_TEMP_TOKEN] = t
        authorize_url = s.build_authorize_url(t, self.context.absolute_url() + '/authorize-twitter-action')
        return authorize_url

