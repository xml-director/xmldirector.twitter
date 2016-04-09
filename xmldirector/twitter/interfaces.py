# -*- coding: utf-8 -*-

################################################################
# xmldirector.twitter
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################


from zope.interface import Interface
from zope import schema
from xmldirector.twitter.i18n import MessageFactory as _


class IBrowserLayer(Interface):
    """A brower layer specific to my product """


class IDropboxSettings(Interface):
    """ Dropbox settings """

    twitter_app_key = schema.TextLine(
        title=_(u'Dropbox application key'),
        required=True
    )

    twitter_app_secret = schema.TextLine(
        title=_(u'Dropbox application secret'),
        required=True
    )
