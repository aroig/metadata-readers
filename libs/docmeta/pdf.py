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

import os
import re
from .utils import executepipe
# import pyPdf


class PdfMeta(object):
    def __init__(self, path):
        super(PdfMeta, self).__init__()
        self.path = os.path.abspath(path)


    def get_arxiv_id(self):
        raw_content = executepipe([['pdftotext', '-f', '1', '-l', '2', self.path, '-']])
        m = re.search("arXiv:([^\s]*)\s", raw_content)

        if m != None: arxiv_id = m.group(1)
        else:         arxiv_id = None

        return arxiv_id


    def get_cover(self, size=1024):
        png = executepipe([['pdftoppm', '-png', '-f', '1', '-l', '1',
                            '-scale-to', str(size), self.path]])
        return png
