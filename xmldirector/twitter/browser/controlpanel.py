# -*- coding: utf-8 -*-


################################################################
# xmldirector.twitter
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

from plone.app.registry.browser import controlpanel

from xmldirector.twitter.interfaces import ITwitterSettings
from xmldirector.twitter.i18n import MessageFactory as _


class TwitterSettingsEditForm(controlpanel.RegistryEditForm):

    schema = ITwitterSettings
    label = _(u'XML Director - Twitter settings')
    description = _(u'')

    def updateFields(self):
        super(TwitterSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(TwitterSettingsEditForm, self).updateWidgets()


class TwitterSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = TwitterSettingsEditForm
