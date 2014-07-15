#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    sqlmake
    ~~~~~~~

    command line tool that builds a complete SQL database schema
    from a set of files contained in a folder.

    the tool outputs SQL instructions :
        * after sorting out declared dependencies
        * after renaming internal variables

    :copyright: (c) 2014 by sc AmvTek srl
    :email: devel@amvtek.com
"""

import re, os, argparse

_kvRe = re.compile("\s*([a-zA-z_-]+)\s*=\s*([a-zA-Z_]*)\s*$")

def input_path(fp):
    "make fp an absolute path and checks it exist"

    cwd = os.path.abspath(os.getcwd())
    fp = os.path.join(cwd,fp)
    if not os.path.exists(fp):
        raise ValueError("Invalid input path !")
    return fp

def key_value_pair(s):
    "if s matches k=v return (k,v) tuple"

    m = _kvRe.match(s)
    if m is None:
        raise ValueError("Invalid definition, needs key=value !")
    return m.groups()

def parse_command_line():
    "read and parse command line"

    parser = argparse.ArgumentParser(
        description="build a SQL schema parsing all sql files found in a folder"
        )

    parser.add_argument("ipath",
            metavar="IPATH", type=input_path,
            help="path to folder or file that contains schema definitions"
            )

    parser.add_argument("-d", "--def",
            metavar="name=value", dest="context",
            action="append", type=key_value_pair,
            help="list variable definition as name=value"
            )

    return parser.parse_args()

if __name__ == "__main__":

    args = parse_command_line()

    print "CWD is ",os.getcwd()

    print "ARGS = ",args
