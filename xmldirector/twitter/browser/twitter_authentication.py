# -*- coding: utf-8 -*-

################################################################
# xmldirector.twitter
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

from twython import Twython

from zope.component import getUtility
from Products.Five.browser import BrowserView
from plone.registry.interfaces import IRegistry
from zope.annotation import IAnnotations

from xmldirector.twitter.interfaces import ITwitterSettings

TWITTER_TOKEN = 'xmldirector.twitter.token'
TWITTER_TOKEN_SECRET = 'xmldirector.twitter.token_secret'


class TwitterAuthentication(BrowserView):

    def authorize(self, oauth_token):
        
        annotation = IAnnotations(self.context)
        settings = self.twitter_settings

        oauth_verifier = self.request['oauth_verifier']
        twitter = Twython(
                settings.twitter_app_key, 
                settings.twitter_app_secret,
                annotation[TWITTER_TOKEN],
                annotation[TWITTER_TOKEN_SECRET])
        final_step = twitter.get_authorized_tokens(oauth_verifier)
        annotation[TWITTER_TOKEN] = final_step['oauth_token']
        annotation[TWITTER_TOKEN_SECRET] = final_step['oauth_token_secret']

        self.context.plone_utils.addPortalMessage(u'Twitter access authorized')
        self.request.response.redirect(self.context.absolute_url() + '/authorize-twitter')

    def deauthorize(self):
        annotation = IAnnotations(self.context)
        try:
            del annotation[TWITTER_TOKEN]
        except KeyError:
            pass

        try:
            del annotation[TWITTER_TOKEN_SECRET]
        except KeyError:
            pass

        self.context.plone_utils.addPortalMessage(u'Twitter access deauthorized')
        self.request.response.redirect(self.context.absolute_url() + '/authorize-twitter')

    @property
    def twitter_settings(self):
        registry = getUtility(IRegistry)
        return registry.forInterface(ITwitterSettings)

    @property
    def twitter_session(self):
        settings = self.twitter_settings
        annotation = IAnnotations(self.context)
        return Twython(
                settings.twitter_app_key, 
                settings.twitter_app_secret, 
                annotation[TWITTER_TOKEN],
                annotation[TWITTER_TOKEN_SECRET])

    def get_oauth_token(self):
        annotation = IAnnotations(self.context)
        return annotation.get(TWITTER_TOKEN)

    def get_oauth_url(self):

        settings = self.twitter_settings
        twitter = Twython(settings.twitter_app_key, settings.twitter_app_secret)
        callback_url = self.context.absolute_url() + '/authorize-twitter-action'
        auth = twitter.get_authentication_tokens(callback_url=callback_url)
        oauth_token = auth['oauth_token']
        oauth_token_secret = auth['oauth_token_secret']
        annotation = IAnnotations(self.context)
        annotation[TWITTER_TOKEN] = oauth_token
        annotation[TWITTER_TOKEN_SECRET] = oauth_token_secret
        return auth['auth_url']

