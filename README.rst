================
metadata-readers
================
A collection of metadata reader plugins for calibre.

Plugins
-------
:pdf-metadata:
   A pdf metadata extraction plugin for calibre. This plugin is a replacement
   for the stock pdf metadata plugin, that parses the contents for arxiv
   identifiers. If one is found the the first pages, it is added in the Ids
   field.

:djvu-metadata:
   A djvu metadata extraction plugin for calibre. Extracts cover from djvu files.


Dependencies
------------
These plugins have two external dependencies:
  - pdftotext: for extracting content
  - pdftoppn: for getting the cover
  - djvulibre: for manipulating djvu files

``pdftotext`` and ``pdftopnm`` are both provided by the package ``poppler`` on
Arch, ``poppler-utils`` on Ubuntu, or maybe ``xpdf`` on windows (untested)


Installation
------------

Just go to the plugin directory and type::
  
  make install

This makes a zip package with the code and installs it in the user's calibre
directory (``~/.config/calibre`` on Arch linux)


Links
-----
- http://www.foolabs.com/xpdf/download.html
- http://calibre-ebook.com/
- http://djvu.sourceforge.net/
