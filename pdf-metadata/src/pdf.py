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

import re
import os
import shutil
import subprocess

from calibre import prints
from calibre.ptempfile import TemporaryDirectory
from calibre.customize import MetadataReaderPlugin
from calibre.ebooks.metadata.book.base import Metadata
from calibre.ebooks.metadata.pdf import get_metadata, get_quick_metadata
from calibre.utils.ipc.simple_worker import fork_job, WorkerError


def get_arxiv_id_worker(outputdir, get_cover):
    ''' Read info dict and cover from a pdf file named src.pdf in outputdir.
    Note that this function changes the cwd to outputdir and is therefore not
    thread safe. Run it using fork_job. This is necessary as there is no safe
    way to pass unicode paths via command line arguments. This also ensures
    that if poppler crashes, no stale file handles are left for the original
    file, only for src.pdf.'''
    os.chdir(outputdir)

    ret = {}
    try:
        raw = subprocess.check_output(['pdftotext', '-f', '1', '-l', '2', 'src.pdf', '-'])
    except subprocess.CalledProcessError as e:
        prints('pdftotext errored out with return code: %d'%e.returncode)
        return None

    try:
        raw = raw.decode('utf-8')
    except UnicodeDecodeError:
        prints('pdftotext returned no UTF-8 data')
        return None

    if get_cover:
        size = 1024
        try:
            subprocess.check_call(['pdftoppm', '-jpeg', '-singlefile', '-scale-to', str(size), 'src.pdf', 'cover'])
        except subprocess.CalledProcessError as e:
            prints('pdftoppm errored out with return code: %d'%e.returncode)

    m = re.search("arXiv:([^\s]*)\s", raw)
    if m:
        ret['arxiv_id'] = m.group(1).strip()

    return ret


def get_arxiv_metadata(stream, cover=True):
    with TemporaryDirectory('_pdf_metadata_read_arxiv') as pdfpath:
        stream.seek(0)
        with open(os.path.join(pdfpath, 'src.pdf'), 'wb') as f:
            shutil.copyfileobj(stream, f)
        try:
            res = fork_job('calibre_plugins.pdf_metadata.pdf', 'get_arxiv_id_worker', (pdfpath, bool(cover)))
        except WorkerError as e:
            prints(e.orig_tb)
            raise RuntimeError('Failed to run pdftotext')
        info = res['result']
        with open(res['stdout_stderr'], 'rb') as f:
            raw = f.read().strip()
            if raw:
                prints(raw)
        if info is None:
            raise ValueError('Could not read arxiv ID from PDF')

        covpath = os.path.join(pdfpath, 'cover.jpg')
        cdata = None
        if cover and os.path.exists(covpath):
            with open(covpath, 'rb') as f:
                cdata = f.read()

    mi = get_metadata(stream, cover=False)
    arxiv_id = info.get('arxiv_id', None)

    if arxiv_id:
        mi.set_identifier('arxiv', arxiv_id)

    if cdata:
        mi.cover_data = ('jpg', cdata)

    return mi


class PDFMetadataReader2(MetadataReaderPlugin):
    name                    = 'Get PDF Metadata'
    description             = _('Reads a PDF metadata, including arxiv ID when present')
    author                  = 'Abdó Roig-Maranges'
    version                 = (1,3,0)
    minimum_calibre_version = (2,66,0)
    file_types = ['pdf']

    def get_metadata(self, stream, ftype):
        if self.quick:
            mi = get_arxiv_metadata(stream, cover=False)

        else:
            mi = get_arxiv_metadata(stream, cover=True)

        mi.tags = []
        return mi
