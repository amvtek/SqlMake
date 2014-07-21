Invocation of sqlmake
=====================

::

    usage: sqlmake [-h] [-d name=value] [--out OUTFILE] [--ext EXT] IPATH

    build a SQL schema from a set of files

    positional arguments:
      IPATH                 path to folder or file that contains schema
			    definitions

    optional arguments:
      -h, --help            show this help message and exit
      -d name=value, --def name=value
			    list variable definition as name=value
      --out OUTFILE         file in which SQL will be saved (default -)
      --ext EXT             file extension for schema resources (default sql)
