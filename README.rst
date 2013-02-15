================
get-pdf-metadata
================
A pdf metadata extraction plugin for calibre.

This plugin is a replacement for the stock pdf metadata plugin, that parses the
contents for arxiv identifiers. If one is found the the first pages, it is added
in the Ids field.


Dependencies
------------
This plugin has two external dependencies:
- pdftotext: for extracting content
- pdftoppn: for getting the cover

Both programs are provided by the package ``poppler`` on Arch, ``poppler-utils``
on Ubuntu, or maybe ``xpdf`` on windows (untested)


Installation
------------

Just type::
  
  make install

This makes a zip package with the code and installs it in the user's calibre
directory (``~/.config/calibre`` on Arch linux)


Links
-----
- http://www.foolabs.com/xpdf/download.html
- http://calibre-ebook.com/
