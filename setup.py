# -*- coding: utf-8 -*-
"""setup installer for the SqlMake project"""

from setuptools import setup

if __name__ == "__main__":
    try:
        setup()
    except:  # noqa
        print(
            "\n\nAn error occurred while building the project, "
            "please ensure you have the most updated version of pip, setuptools "
            "and wheel with:\n"
            "   pip install -U pip setuptools wheel\n\n"
        )
        raise
