# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='SqlMake',
    version='0.2.2',
    author='AmvTek developers',
    author_email='devel@amvtek.com',
    packages=['sqlmake'],
    scripts=['bin/sqlmake'],
    url='https://github.com/amvtek/SqlMake/',
    license='MIT',
    description='Command line tool to build a sql schema',
    long_description=open('README.rst').read(),
    install_requires=[
        "Jinja2==2.7.3",
        "toposort==1.0.0",
    ],
)
