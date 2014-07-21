Working with SqlMake
====================

A SqlMake project consists of files called **resources** stored in a folder.
Every file with *.sql* extension, in project folder or subfolders are project
resources. 

SqlMake allows to add special instructions to a resource file, in a non
obtrusive way : 

SQL comment line starts with :: 

    --

SqlMake instructions starts with ::

    --#

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
add the followings DEPS instruction at the top of the *mytable.sql* file.

.. code-block:: sql

    --# DEPS: init, ../public

    CREATE TABLE t_mytable(
	...

Renaming schema elements (VARS)
-------------------------------

SqlMake resources maybe used during development as *normal* SQL file without the
help of the **sqlmake** command. The **VARS** instruction allows to define which
*name* maybe redefined when compiling the schema. The **sqlmake** command allows to
redefine some of the schema name by means of the **--def option**.

Renaming example
~~~~~~~~~~~~~~~~

Let's assume that in file mytable.sql, we want to allows renaming at *compilation
time* the table t_mytable into something else and also to change table owner
amvtek into another role defined by variable schema_owner. A **VARS**
instruction will be added at the top of the file to make this possible.

.. code-block:: sql

    --# DEPS: init, ../public
    --# VARS: t_mytable, amvtek=owner_role

    create table t_mytable(
	id integer primary key,

	name varchar(80) not null,
	...
    );

    -- set table owner to role amvtek
    alter table t_mytable owner to amvtek;

To rename t_mytable into t_othertable and amvtek role into titus, one may use
the sqlmake command like so ::

    sqlmake --def t_mytable=t_othertable --def owner_role=titus path/to/mytable.sql

Unleashing the power of Jinja templates
---------------------------------------

SqlMake is built on top of the well known `Jinja template engine`_ . You may use
any of the statements exported by Jinja such as if/endif, for/endfor embedding
those in SQL comment line that starts with ::

    --#

Jinja instruction example
~~~~~~~~~~~~~~~~~~~~~~~~~

Assumes that when in development we want our example table to be created in
schema tests, and that tests shall be recreated each time we are loading the
mytable.sql file in the development database. When compiling the full schema
using **sqlmake** the commands necessary for this to happen shall not be
executed.

A simple Jinja conditional block, will make this a snapp :

.. code-block:: sql

    --# DEPS: init, ../public
    --# VARS: t_mytable, amvtek=owner_role

    --# if __development__ : 
    
    -- sqlmake will not render this block 
    -- as long as __development__ stays undefined...

    drop schema if exists tests;
    create schema tests;
    set search_path to tests, public;

    --# endif

    create table t_mytable(
	id integer primary key,

	name varchar(80) not null,
	...
    );

    -- set table owner to role amvtek
    alter table t_mytable owner to amvtek;

.. _Jinja template engine: http://jinja.pocoo.org/docs/
