# -*- coding: utf-8 -*-
"""
    fileparser
    ~~~~~~~~~~

    parse SQL file making use of special comments
    that defines dependencies & variables...

    :copyright: (c) 2014 by sc AmvTek srl
    :email: devel@amvtek.com
"""

import re
from os.path import abspath

from jinja2 import Environment  # see PyPI jinja2


class ContentParser(object):
    """Allows to parse resource out of file content"""

    _lineTokenSep = ","

    _extractDEPS = re.compile(r"^--#\s*DEPS\s*:(.*)$", re.MULTILINE)
    _isDEPSLine = re.compile(r"^--#\s*DEPS\s*:.*$", re.MULTILINE)

    _extractVARS = re.compile(r"^--#\s*VARS\s*:(.*)$", re.MULTILINE)
    _isVARSLine = re.compile(r"^--#\s*VARS\s*:.*$", re.MULTILINE)
    _extractVarDef = re.compile(r"^\s*(\w+)(?:\=\s*(\w+)){0,1}$")

    def split_token(self, contentline):
        """return list of token"""

        return [tok.strip() for tok in contentline.split(self._lineTokenSep)]

    def list_dependencies(self, content):
        """return list of dependencies found on content DEPS lines"""

        # local alias
        split = self.split_token

        rv = []
        for data in self._extractDEPS.findall(content):
            rv.extend([s for s in split(data) if s])

        return rv

    def cleanup_deps_and_vars(self, content):
        """remove DEPS and VARS lines from content"""

        rv = self._isDEPSLine.sub("", content)
        rv = self._isVARSLine.sub("", rv)
        return rv.strip()

    def list_variables(self, content):
        """return list of variables definition found on content VARS lines"""

        # local alias
        split = self.split_token

        rv = []
        for data in self._extractVARS.findall(content):
            rv.extend([s for s in split(data) if s])

        return rv

    def compile_template(self, content):
        """return template string and default context..."""

        # extract variable definitions from content
        vardefs = self.list_variables(content)

        defaultCtx = {}
        tplString = self.cleanup_deps_and_vars(content)
        for vardef in vardefs:

            m = self._extractVarDef.match(vardef)
            if m is None:
                raise ValueError("Invalid VARS token : %s" % vardef)
            tok, repl = m.groups()

            # set repl
            if repl is None:
                repl = tok
            defaultCtx[repl] = tok
            repl = "{{%s}}" % repl

            # set tokPattern
            tokPattern = r"\b%s\b" % tok  # RMQ: always use r".." format

            # replace in content
            tplString = re.sub(tokPattern, repl, tplString)

        return tplString, defaultCtx

    def __call__(self, content):
        """parse content and return dependencies, defaults, tplstring..."""

        dependencies = self.list_dependencies(content)

        tplstring, defaults = self.compile_template(content)

        return (dependencies, tplstring, defaults)


def render_resource(fpath, parser=None, **kwargs):
    """render a single file resource"""

    # extract content
    with open(abspath(fpath)) as f:
        content = f.read()

    # prepare parser
    parse = parser or ContentParser()
    if not callable(parse):
        raise ValueError("Invalid parser !")

    # compile resource template
    tplEnv = Environment(line_statement_prefix="--#")
    deps, tplstr, defaults = parse(content)
    tpl = tplEnv.from_string(tplstr)

    # prepare rendering context
    ctx = dict(defaults)
    ctx.update(kwargs)

    return tpl.render(ctx)
