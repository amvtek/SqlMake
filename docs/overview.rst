Overview
========

Who needs SqlMake ?
-------------------

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


Installing SqlMake
------------------

Installing the **sqlmake** CLI tool currently requires you have some
familiarities with the way python packages are distributed. For now **sqlmake**
has been tested only with python **2.7** interpreter.

To install SqlMake and its dependencies using pip, run ::

    pip install SqlMake

Running the sqlmake CLI
-----------------------

Getting help ::

    sqlmake -h

Compiling a schema from a set of resources ::

    sqlmake --out=myschema.sql path/to/project/folder
