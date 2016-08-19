xmldirector.twitter
===================

Integration of 

- Plone (https://www.plone.org)
- Twitter

Requirements
------------

- Plone 4.3 (tested)
  
- Plone 5.0 (tested)

- XML Director 2.0 (xmldirector.plonecore)


Usage
-----

First you need to register your own App as Twitter developer.
on https://apps.twitter.com/. Your application must be configured
for full twitter access. The application key and application secret
must be configured globally inside your Plone site setup -> XML Director
Twitter setting.

A ``Connector`` instance must be authorized with Twitter (see ``Twitter``
tab/action).

The connection URL for a ``Connector`` connected to Twitter must be
``twitter://twitter.com/``.


License
-------
This package is published under the GNU Public License V2 (GPL 2)

Source code
-----------
See https://github.com/xml-director/xmldirector.twitter

Bugtracker
----------
See https://github.com/xml-director/xmldirector.twitter/issues


Author
------
| Andreas Jung/ZOPYX
| Hundskapfklinge 33
| D-72074 Tuebingen, Germany
| info@zopyx.com
| www.zopyx.com

