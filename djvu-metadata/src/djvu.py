#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# get-djvu-metadata - metadata extraction from djvu files
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

from .docmeta import DjvuMeta
import os

from calibre.customize import MetadataReaderPlugin
from calibre.customize import MetadataWriterPlugin
from calibre.ebooks.metadata.book.base import Metadata


class DjvuMetadataReader(MetadataReaderPlugin):
    name                    = 'Get DJVU Metadata'
    description             = _('Reads djvu metadata, including cover')
    author                  = 'Abdó Roig-Maranges'
    version                 = (1,2,0)
    minimum_calibre_version = (0,8,0)
    file_types = ['djvu']


    def get_metadata(self, stream, type):
        mi = Metadata(_('Unknown'))

        if hasattr(stream, 'name'): fname = os.path.abspath(stream.name)
        else:                       return mi

        djvum = DjvuMeta(fname)
        meta = djvum.get_metadata()
        if 'title' in meta.keys(): mi.title = meta['title']
        if 'author' in meta.keys(): mi.authors = [au.strip() for au in meta['author'].split(',')]

        if not self.quick:
            mi.cover_data = ('png', djvum.get_cover())

        return mi
