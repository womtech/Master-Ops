#!/usr/bin/env python3
import psycopg2, sys
sys.path.insert(0,'/projects/mops')
from collections import namedtuple

from libraries.ErrorHandler import ErrorLogger
#import ErrorLogger


# Usage: Common Class For DB Operations
# Author: MD <danish@whackedout.in>
# Date Written: Dec 31, 2018
# Usage: [Obj]._custom("Select * ....")

class PostgreSQLConnector:

  def create_record(self, obj, fields):
    Record = namedtuple("Record", fields)
    mapping = dict(zip(fields, obj))
    return Record(**mapping)

  def __init__( self ):
    self.con = psycopg2.connect(dbname='mops', user='mops', host='localhost', password='P@$$w0rd100%', port=5432)

  # response_type = json or named_tuple
  def _custom( self, query, op_type, response_type = "json" ):
    cur = self.con.cursor( )
    updated_row = 0
    res = {}
    try:
      cur.execute( query )
      if op_type == "select":
        result = []
        temp = cur.fetchall( )
        if response_type == "named_tuple":
          col_names = [desc[0] for desc in cur.description]
          for row in temp:
            result.append(self.create_record(row, col_names))
          res = {"columns": col_names, "data": result, "count": cur.rowcount }
        else:
          res = { "data": temp }
      elif op_type == "update":
        res = { "affected_rows": cur.rowcount }
        self.con.commit()
        self.con.close()
      return res
    except psycopg2.OperationalError as e:
      ErrorLogger( "Error: PostgreSQLConnector:: " + e )
      return "Error!"

