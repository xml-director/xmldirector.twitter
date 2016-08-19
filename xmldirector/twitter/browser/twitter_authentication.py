# -*- coding: utf-8 -*-

################################################################
# xmldirector.twitter
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################


import datetime 

from twython import Twython
from twython import TwythonError
from twython import TwythonAuthError

from zope.component import getUtility
from zope.interface import alsoProvides
from zope.annotation import IAnnotations
from Products.Five.browser import BrowserView
from plone.registry.interfaces import IRegistry
from plone.protect.interfaces import IDisableCSRFProtection

from xmldirector.twitter.interfaces import ITwitterSettings
from xmldirector.twitter.i18n import MessageFactory as _


TWITTER_TOKEN = 'xmldirector.twitter.token'
TWITTER_TOKEN_SECRET = 'xmldirector.twitter.token_secret'
TWITTER_DATA = 'xmldirector.twitter.data'
TWITTER_DATA_LAST_UPDATED = 'xmldirector.twitter.last_updated'


class TwitterAuthentication(BrowserView):

    def __init__(self, context, request):
        # fuck all Plone protection shit!
        alsoProvides(request, IDisableCSRFProtection)
        super(TwitterAuthentication, self).__init__(context, request)

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
        self.context.plone_utils.addPortalMessage(_(u'Twitter access authorized'))
        self.request.response.redirect(self.context.absolute_url() + '/authorize-twitter')

    def deauthorize(self):
        """ Deauthorize Twitter access """
        annotation = IAnnotations(self.context)
        for key in (TWITTER_TOKEN, TWITTER_TOKEN_SECRET, TWITTER_DATA, TWITTER_DATA_LAST_UPDATED):
            try:
                del annotation[key]
            except KeyError:
                pass
        self.context.plone_utils.addPortalMessage(_(u'Twitter access deauthorized'))
        self.request.response.redirect(self.context.absolute_url() + '/authorize-twitter')

    def twitter_info(self, force=False):
        """ Return Twitter information associated with the current token """

        annotation = IAnnotations(self.context)
        data = annotation.get(TWITTER_DATA)
        if data and not force:
            last_accessed = annotation[TWITTER_DATA_LAST_UPDATED]
            if (datetime.datetime.utcnow() - last_accessed).seconds < 15 * 60: # 15 minutes
                return data

        session = self.twitter_session
        try:
            data = session.verify_credentials()
        except TwythonAuthError:
            data = None

        annotation[TWITTER_DATA] = data
        annotation[TWITTER_DATA_LAST_UPDATED] = datetime.datetime.utcnow()
        return data

    @property
    def twitter_settings(self):
        registry = getUtility(IRegistry)
        return registry.forInterface(ITwitterSettings)

    def twitter_configured(self):
        settings = self.twitter_settings
        return settings.twitter_app_key and settings.twitter_app_secret

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

    def post_to_twitter(self, text):

        twitter = self.twitter_session
        try:
            twitter.update_status(status=text)
            self.context.plone_utils.addPortalMessage(_(u'Post to Twitter successful'))
            self.request.response.redirect(self.context.absolute_url() + '/authorize-twitter')
        except TwythonError as e:
            self.context.plone_utils.addPortalMessage(_(u'Post to Twitter failed - ' + str(e)), 'error')
            self.request.response.redirect(self.context.absolute_url() + '/authorize-twitter?text={}'.format(text))

