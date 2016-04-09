# -*- coding: utf-8 -*-


################################################################
# xmldirector.twitter
# (C) 2016,  Andreas Jung, www.zopyx.com, Tuebingen, Germany
################################################################

from plone.app.registry.browser import controlpanel

from xmldirector.twitter.interfaces import IDropboxSettings
from xmldirector.twitter.i18n import MessageFactory as _


class DropboxSettingsEditForm(controlpanel.RegistryEditForm):

    schema = IDropboxSettings
    label = _(u'Dropbox Policy settings')
    description = _(u'')

    def updateFields(self):
        super(DropboxSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(DropboxSettingsEditForm, self).updateWidgets()


class DropboxSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = DropboxSettingsEditForm
