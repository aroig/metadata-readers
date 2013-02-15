#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# pdf-metadata - metadata extraction from pdf files
# Copyright 2012 Abdó Roig-Maranges <abdo.roig@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (unicode_literals, division)

import re
import os

from .docmeta import PdfMeta

from calibre.customize import MetadataReaderPlugin
from calibre.ebooks.metadata.book.base import Metadata
from calibre.ebooks.metadata.pdf import get_metadata, get_quick_metadata



class PDFMetadataReader2(MetadataReaderPlugin):
    name                    = 'Get PDF Metadata'
    description             = _('Reads a PDF metadata, including arxiv ID when present')
    author                  = 'Abdó Roig-Maranges'
    version                 = (1,2,0)
    minimum_calibre_version = (0,8,0)
    file_types = ['pdf']

    def get_metadata(self, stream, type):
        if hasattr(stream, 'name'): fname = os.path.abspath(stream.name)

        if self.quick:
            mi = get_quick_metadata(stream)
        else:
            mi = get_metadata(stream, cover=False)
            pdfm = PdfMeta(fname)
            arxiv_id = pdfm.get_arxiv_id()
            if arxiv_id: mi.set_identifier('arxiv', arxiv_id)

            mi.cover_data = ('png', pdfm.get_cover())

        mi.tags = []
        return mi
