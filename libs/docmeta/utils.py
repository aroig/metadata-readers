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

import re
import sys
import subprocess


class CommandError(Exception):
    """Conversion error"""
    def __init__(self, desc, cmdlist, retlist, stderrlist):
        Exception.__init__(self, desc)
        self.desc = desc
        self.cmdlist = cmdlist
        self.retlist = retlist
        self.stderrlist = stderrlist
        print("Command Error !!!")
        print("  cmd:    %s" % ' | '.join([' '.join(c) for c in self.cmdlist]))
        print("  ret:    %s" % str(self.retlist))
        print("  stderr: %s" % str(self.stderrlist))



def executepipe(cmdlst, outfile=None, checkreturn=True):
    N = len(cmdlst)
    p = []
    for n in range(0,N):
        cmd = cmdlst[n]

        if n == 0: sin = None
        else:      sin = plast.stdout
        if n < N-1:
            sout = subprocess.PIPE
        else:
            if outfile != None: sout = open(outfile, 'w')
            else:               sout = subprocess.PIPE
        serr = subprocess.PIPE

        plast = subprocess.Popen(cmd, stdout=sout, stderr=serr, stdin=sin)
        p.append(plast)

    ret,err = plast.communicate()

    if checkreturn and plast.returncode != 0:
        raise CommandError("Command produced errors", cmdlst, plast.returncode, err)

    if outfile == None:
        if sys.version_info[0] >= 3: return ret.decode('utf-8')
        else:                        return ret
    else:
        sout.close()
        return None
