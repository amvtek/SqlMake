#######
SqlMake
#######

Command line tool that builds a SQL schema from a set of sql files.

Who needs SqlMake ?
===================

You will benefit from SqlMake if you are confortable with SQL and see the value
of defining your sql schemas (tables, stored functions, indexes, roles...)
directly in sql and not through an ORM system like the Django ORM, SqlAlchemy or
Hibernate to name a few.

What SqlMake allows you to do is to split your SQL schema accross multiples sql
files accurately defining **dependencies** which may exist in between such files by
mean of special SQL comments. When in need to recreate your database schema, the
**sqlmake** tool will collect all files resources that composes the schema,
parse them and emit the SQL commands they contain in optimal order so as to
respect the dependencies that have been defined. 

Once your schema has been split in between several files, it will be very easy
to read and maintain. If you archive it in a version control system like git,
subversion or mercurial it will also be very easy to prepare **migration**
scripts. 

Preparing your files for SqlMake
================================

A SqlMake project consists of files called **resources** stored in a folder.
Every file with *.sql* extension, in project folder or subfolders are project
resources. 

SqlMake allows to add special instructions to a resource file, in a non
obtrusive way : 

* SQL comment line starts with **--**.
* SqlMake instructions starts with **--#**

Defining dependencies (DEPS)
----------------------------

To add dependencies to a resource file you add **DEPS** instructions at the top
of the file. Each **DEPS** instruction provides a comma separated list of
relative paths to resource files or folder in your project. If you are using
folder dependency, SqlMake will automatically assumes that all the resources it
contains are dependencies of the file that defines it.

Dependencies example
~~~~~~~~~~~~~~~~~~~~

Assume the following project structure::

    project/
    ├── appschema
    │   ├── init.sql
    │   └── mytable.sql
    ├── public
    │   ├── add_extensions.sql
    │   └── functions.sql
    ├── README.txt
    └── roles.sql

So as get the *appschema/mytable.sql* resource to depends of the
*appschema/init.sql* resource and of all the resources in the public folder just
add the followings DEPS instruction at the top of the *mytable.sql* file ::

    --# DEPS: init, ../public

    CREATE TABLE t_mytable(
	...

Renaming schema elements (VARS)
-------------------------------



SqlMake is built on top of the well known `Jinja template engine`_ . You may use
any of the statements exported by Jinja such as if/endif, for/endfor embedding
those in SQL comment line that starts with **--#**.

Installing SqlMake
==================


