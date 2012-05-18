# Nice print stuff
TAB = 12*' '

NLTAB = ',\n'+TAB

USAGE = """usage: autoload.py [options]

Generates python code for a given database schema.

options:
    -h, --help                      Show this help
    -u URL,         --url URL       Database url (e.g.: postgresql+psycopg2://postgres:user@password/Database)
    -o FILE,        --output FILE   Where to put the output (default is stdout)
    -s NAME,        --schema NAME   Name of the schema to output (default is 'default')
    -t T1,T2,.. ,   --tables T1,T2  Name of tables to inspect (default is 'all').
                                    Support globbing character to select more tables.
                                    ex.: -t Download* will generate a model for all tables starting with Download

    -i              --noindex       Do not generate index information
    -g              --generic-types Generate generic column types rather than database-specific type
    -e              --example       Generate code with examples how to access data
    -3              --z3c           Generate code for use with z3c.sqlalchemy
"""

HEADER = """\
# -*- coding: %(encoding)s -*-
## File autogenerated by SQLAutoCode
## see http://code.google.com/p/sqlautocode/

from sqlalchemy import *
%(dialect)s
metadata = MetaData()
"""

HEADER_Z3C = """\
# -*- coding: %(encoding)s -*-
## File autogenerated by SQLAutoCode
## see http://code.google.com/p/sqlautocode/
## Export type: z3c.sqlalchemy

from sqlalchemy import *
%(dialect)s
from z3c.sqlalchemy import Model
from z3c.sqlalchemy.mapper import MappedClassBase

def getModel(metadata):
    model = Model()
"""

PG_IMPORT = """\
try:
    from sqlalchemy.dialects.postgresql import *
except ImportError:
    from sqlalchemy.databases.postgres import *
"""

FOOTER_Z3C = """
    return model
"""

FOOTER_EXAMPLE = """
# some example usage
if __name__ == '__main__':
    db = create_engine(%(url)r)
    metadata.bind = db

    # fetch first 10 items from %(tablename)s
    s = %(tablename)s.select().limit(10)
    rs = s.execute()
    for row in rs:
        print row
"""

TABLE = """ Table('%(name)s', metadata,
    %(columns)s,
    %(constraints)s
    %(schema)s
    )
"""

COLUMN = """Column(%(name)r, %(type)s%(constraints)s%(args)s)"""

FOREIGN_KEY = """ForeignKeyConstraint(%(names)s, %(specs)s, name=%(name)s)"""

INDEX = """Index(%(name)s, %(columns)s, unique=%(unique)s)"""

CHECK_CONSTRAINT = """CheckConstraint('%(sqltext)s')"""

HEADER_DECL = """#autogenerated by sqlautocode

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation

engine = create_engine('%s')
DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
metadata.bind = engine

"""

EXAMPLE_DECL = """#example on how to query your Schema
from sqlalchemy.orm import sessionmaker
session = sessionmaker(bind=engine)()
objs = session.query(%s).all()
print 'All %s objects: %%s'%%objs
"""

INTERACTIVE = """
print 'Trying to start IPython shell...',
try:
    from IPython.Shell import IPShellEmbed
    print 'Success! Press <ctrl-d> to exit.'
    print 'Available models:%%s'%%%s
    print '\\nTry something like: session.query(%s).all()'
    ipshell = IPShellEmbed()
    ipshell()
except:
    'Failed. please easy_install ipython'
"""

