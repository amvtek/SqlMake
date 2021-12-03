#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    sqlmake.__main__
    ~~~~~~~~~~~~~~~~

    command line tool that builds a complete SQL database schema
    from a set of files contained in a folder.

    the tool outputs SQL instructions :
        * after sorting out declared dependencies
        * after renaming internal variables

    :copyright: (c) 2014 by sc AmvTek srl
    :email: devel@amvtek.com
"""

import re
import os
import sys
import argparse

from .indexer import ProjectIndexer
from .fileparser import render_resource


_kvRe = re.compile(r"\s*([a-zA-z0-9_-]+)\s*=\s*([a-zA-Z0-9_]*)\s*$")


def input_path(fp):
    """make fp an absolute path and checks it exist"""

    cwd = os.path.abspath(os.getcwd())
    fp = os.path.normpath(os.path.join(cwd, fp))
    if not os.path.exists(fp):
        raise ValueError("Invalid path !")
    return fp


def key_value_pair(s):
    """if s matches k=v return (k,v) tuple"""

    m = _kvRe.match(s)
    if m is None:
        raise ValueError("Invalid definition, needs key=value !")
    return m.groups()


def parse_command_line():
    """read and parse command line"""

    parser = argparse.ArgumentParser(
        prog="sqlmake", description="build a SQL schema from a set of files"
    )

    parser.add_argument(
        "ipath",
        metavar="IPATH",
        type=input_path,
        help="path to folder or file that contains schema definitions",
    )

    parser.add_argument(
        "-d",
        "--def",
        metavar="name=value",
        dest="context",
        action="append",
        type=key_value_pair,
        help="list variable definition as name=value",
    )

    parser.add_argument(
        "--out",
        dest="outfile",
        type=argparse.FileType("wb", 0),
        default="-",
        help="file in which SQL will be saved (default %(default)s)",
    )

    parser.add_argument(
        "--ext",
        default="sql",
        help="file extension for schema resources (default %(default)s)",
    )

    return parser.parse_args()


def main():
    """handle command line"""

    args = parse_command_line()
    sql = ""

    print("---")
    context = dict(args.context or [])

    if os.path.isdir(args.ipath):

        print("Now indexing project in %s " % args.ipath)

        project = ProjectIndexer(args.ipath, args.ext)
        sql = project.render_schema(**context)

    elif os.path.isfile(args.ipath):

        print("Preparing rendering of file %s" % args.ipath)

        sql = render_resource(args.ipath, **context)

    if not sql:

        print("Found no content, nothing to save")
        sys.exit(1)

    print("Now savings compiled SQL")
    args.outfile.write(bytes(sql, "utf-8"))
    print("")
    print("***")


if __name__ == "__main__":

    main()
