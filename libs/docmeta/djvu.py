#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# docmeta - A python module to extract metadata from document files
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
from .utils import executepipe

class DjvuMeta(object):
    def __init__(self, path):
        super(DjvuMeta, self).__init__()
        self.path = os.path.abspath(path)


    def get_metadata(self):
        raw = executepipe([['djvused', "-e", "'print-meta'", self.path]])
        ret = {}

        ma = re.search('Author\s+"(.*?)"', raw)
        if ma: ret['author'] = unicode(ma.group(1))

        mt = re.search('Title\s+"(.*?)"', raw)
        if mt: ret['title'] = unicode(mt.group(1))

        return ret


    def set_metadata(self, title, author):
        metadata = 'Title "%s"; Author "%s"' % (title, author)
        executepipe([['djvused', "-s", "-e", "set-meta; %s" % metadata , self.path]])


    def get_cover(self, size=1024):
        png = executepipe([['ddjvu', "-page=1", "-size=%dx%d" % (size, size), self.path], ['pnmtopng']])
        return png
