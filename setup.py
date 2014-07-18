# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='SqlMake',
    version='0.2.0',
    author='AmvTek developers',
    author_email='devel@amvtek.com',
    packages=['sqlmake'],
    scripts=['bin/sqlmake'],
    url='http://pypi.python.org/pypi/SqlMake/', # not yet released
    license='MIT',
    description='Command line tool to build sql schema',
    long_description=open('README.rst').read(),
    install_requires=[
        "Jinja2==2.7.3",
        "toposort==1.0.0",
    ],
)
