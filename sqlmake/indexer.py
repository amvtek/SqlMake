# -*- coding: utf-8 -*-
"""
    sqlmake.indexer
    ~~~~~~~~~~~~~~~

    index sql files inside a certain folder

    :copyright: (c) 2014 by sc AmvTek srl
    :email: devel@amvtek.com
"""

import re
import os
from os.path import exists, basename, abspath, normpath, relpath, join

from jinja2 import Environment  # see PyPI jinja2
from toposort import toposort_flatten  # see PyPI toposort


from .fileparser import ContentParser


class Resource(str):
    """filesystem resource..."""

    def __new__(cls, path, tplstr="", tpldefaults=None):

        return str.__new__(cls, path)

    def __init__(self, path, tplstr="", tpldefaults=None):

        self.tplstr = tplstr
        self.tpldefaults = tpldefaults or {}


class ProjectIndexer(object):
    """index all resource inside a folder"""

    _isPublic = re.compile(r"^[^\._].*")

    _fileHead = "\n-- +++\n" "-- source %s\n\n%s"

    def __init__(self, rootpath, rfext="sql", parser=None):

        self.rootpath = abspath(rootpath)

        rfpattern = r".*\.%s$" % rfext
        self._isRsrc = re.compile(rfpattern)
        self.rfext = rfext
        self.addextfmt = "%s.{}".format(rfext)

        if parser is None:
            parser = ContentParser()
        if not callable(parser):
            raise ValueError("Invalid parser !")
        self.parse = parser

    def is_public(self, path):
        """return True is path basename does not starts with '.' or '_'"""

        # extract filename
        filename = basename(path.rstrip("/"))
        return self._isPublic.match(filename)

    def is_resource(self, path):
        """return True if path corresponds to resource file"""

        if self._isRsrc.match(path):
            return True

    def get_rpath(self, path):
        """return path relative to project root"""

        return relpath(path, self.rootpath)

    def resolve_dependencies(self, refpath, *deps):
        """return absolute depency path or None if it can not be found"""

        rv = []

        for deppath in deps:

            deppath = normpath(join(refpath, deppath))

            if exists(deppath):
                rv.append(deppath)

            # check if appending extension allows to find deppath
            deppathext = self.addextfmt % deppath
            if exists(deppathext):
                rv.append(deppathext)

        return set(rv)

    def build_index(self):
        """return index dict"""

        rdp = self.resolve_dependencies  # local alias

        rsrIdx = {}
        for fpath, subfolders, files in os.walk(self.rootpath):

            # filter out private subfolder(s)...
            subfolders[:] = [fp for fp in subfolders if self.is_public(fp)]

            # create folder dependency set...
            folddeps = rdp(fpath, *subfolders)

            # index resource files
            rfiles = [fp for fp in files if self.is_resource(fp)]
            for rp in rfiles:

                path = join(fpath, rp)

                # parse file
                with open(path) as f:
                    content = f.read()
                deps, tplstr, defaults = self.parse(content)

                if deps or tplstr:

                    # add resource to folder dependencies
                    folddeps.add(path)

                    # index resource
                    rsrIdx[Resource(path, tplstr, defaults)] = rdp(fpath, *deps)

            if folddeps:

                # index folder
                rsrIdx[Resource(fpath)] = folddeps

        # filter empty dependencies
        # TODO : it maybe that empty dependencies have value
        for depset in list(rsrIdx.values()):

            rmlist = []
            for dep in depset:

                if dep not in rsrIdx:
                    rmlist.append(dep)

            for nulldep in rmlist:
                depset.remove(nulldep)

        return rsrIdx

    def render_schema(self, **kwargs):
        """return full SQL schema built rendering indexed resources"""

        # construct templating environment
        tplEnv = Environment(line_statement_prefix="--#")

        # build resource index
        rsrIdx = self.build_index()

        # iterates resource in 'topological' sorted order
        buf = []
        for rsr in toposort_flatten(rsrIdx):

            # process resource template if any
            if rsr.tplstr:

                # add source informations to tplstr
                tplstr = self._fileHead % (self.get_rpath(rsr), rsr.tplstr)

                # compile template
                tpl = tplEnv.from_string(tplstr)

                # prepare rendering context
                ctx = {}
                ctx.update(rsr.tpldefaults)
                ctx.update(kwargs)

                # render template
                buf.append(tpl.render(ctx))

        return "\n".join(buf)
