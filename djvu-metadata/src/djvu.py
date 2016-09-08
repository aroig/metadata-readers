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

import os
import re
import shutil
import subprocess

from calibre import prints
from calibre.ptempfile import TemporaryDirectory
from calibre.customize import MetadataReaderPlugin
from calibre.customize import MetadataWriterPlugin
from calibre.ebooks.metadata.book.base import Metadata
from calibre.utils.ipc.simple_worker import fork_job, WorkerError
from calibre.ebooks.metadata import (MetaInformation, string_to_authors)


def get_djvu_metadata_worker(outputdir, get_cover):
    ''' Read info dict and cover from a djvu file named src.djvu in outputdir.
    Note that this function changes the cwd to outputdir and is therefore not
    thread safe. Run it using fork_job. This is necessary as there is no safe
    way to pass unicode paths via command line arguments.'''
    os.chdir(outputdir)

    try:
        raw = subprocess.check_output(['djvused', '-e', 'print-meta', 'src.djvu'])

    except subprocess.CalledProcessError as e:
        prints('djvused errored out with return code %d' % e.returncode)
        return None

    try:
        raw = raw.decode('utf-8')
    except UnicodeDecodeError:
        prints('djvused returned non UTF-8 data')
        return None

    ret = {}

    ma = re.search('Author\s+"(.*?)"', raw)
    if ma: ret['author'] = ma.group(1)

    mt = re.search('Title\s+"(.*?)"', raw)
    if mt: ret['title'] = mt.group(1)

    if get_cover:
        size = 1024
        try:
            subprocess.check_call(['ddjvu', '-page=1', '-format=pnm', '-size=%dx%d' % (size, size), 'src.djvu', 'cover.pnm'])
            with open("cover.jpg", "w") as fd:
                subprocess.check_call(['pnmtojpeg', 'cover.pnm'], stdout=fd)
        except subprocess.CalledProcessError as e:
            prints('ddjvu errored out with return code: %d'%e.returncode)

    return ret


def set_djvu_metadata_worker(self, outputdir, title, author):
    os.chdir(outputdir)
    metadata = []
    metadata.append('Title "%s"' % title)
    metadata.append('Author "%s"' % author)
    subprocess.check_output(['djvused', '-s', '-e', 'set-meta; %s' % '; '.join(metadata), 'src.djvu'])


def get_djvu_metadata(stream, cover=True):
    with TemporaryDirectory('_djvu_metadata_read') as djvupath:
        stream.seek(0)
        with open(os.path.join(djvupath, 'src.djvu'), 'wb') as f:
            shutil.copyfileobj(stream, f)
        try:
            res = fork_job('calibre_plugins.djvu_metadata.djvu', 'get_djvu_metadata_worker', (djvupath, bool(cover)))
        except WorkerError as e:
            prints(e.orig_tb)
            raise RuntimeError('Failed to run djvused')
        info = res['result']
        with open(res['stdout_stderr'], 'rb') as f:
            raw = f.read().strip()
            if raw:
                prints(raw)
        if info == None:
            raise ValueError('Could not read metadata from djvu')
        covpath = os.path.join(djvupath, 'cover.jpg')
        cdata = None
        if cover and os.path.exists(covpath):
            with open(covpath, 'rb') as f:
                cdata = f.read()

    title = info.get('Title', None)
    au = info.get('Author', None)
    if au is None:
        au = [_('Unknown')]
    else:
        au = string_to_authors(au)
    mi = MetaInformation(title, au)

    if cdata:
        mi.cover_data = ('jpg', cdata)

    return mi


class DjvuMetadataReader(MetadataReaderPlugin):
    name                    = 'Get DJVU Metadata'
    description             = _('Reads djvu metadata, including cover')
    author                  = 'Abdó Roig-Maranges'
    version                 = (1,3,0)
    minimum_calibre_version = (2,66,0)
    file_types = ['djvu']


    def get_metadata(self, stream, ftype):
        if self.quick:
            mi = get_djvu_metadata(stream)
        else:
            mi = get_djvu_metadata(stream, cover=True)

        mi.tags = []
        return mi

