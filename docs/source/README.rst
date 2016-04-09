xmldirector.twitter
===================

Integration of 

- Plone (https://www.plone.org)
- XML Director (https://www.xml-director.info) 
- Dropbox

Requirements
------------

- Plone 4.3 (tested)
  
- Plone 5.0 (experimental, in progress)

- XML Director (xmldirector.plonecore)


Usage
-----

First you need to register your own App as Dropbox developer
on https://twitter.com/developer. Your application must be configured
for full twitter access. The application key and application secret
must be configured globally inside your Plone site setup -> XML Director
Dropbox setting.

A ``Connector`` instance must be authorized with Dropbox (see ``Dropbox``
tab/action).

The connection URL for a ``Connector`` connected to Dropbox must be
``twitter://twitter.com/``.


License
-------
This package is published under the GNU Public License V2 (GPL 2)

Source code
-----------
See https://github.com/xml-director/xmldirector.twitter

Bugtracker
----------
See https://github.com/xml-director/xmldirector.twitter


Author
------
| Andreas Jung/ZOPYX
| Hundskapfklinge 33
| D-72074 Tuebingen, Germany
| info@zopyx.com
| www.zopyx.com

