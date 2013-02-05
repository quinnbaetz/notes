# Inferno sample data model

# Python Imports
import logging as log
import pprint
import threading

# Extern Imports
import inferno.database

# Project Imports
import config

dbconns = threading.local()
def db():
    if not hasattr(dbconns, 'conn'):
        dbconns.conn = inferno.database.Connection.connect()
    return dbconns.conn

# This class just for helloworld, for developing database functionality
class SqlDiff(inferno.database.Row):
    @classmethod
    def scan(clz):
        sql = 'SELECT * FROM sql_diff ORDER BY applied ASC'
        return db().query(sql, clz=clz)

    def display(self):
        return 'Name: %s  --  Created: %s  --  Applied: %s' % (self.diff_name, self.created, self.applied)

    @classmethod
    def get(clz, diff_name):
        sql = 'SELECT * FROM sql_diff WHERE diff_name=%s'
        return db().get(sql, diff_name, clz=clz)

    @classmethod
    def create(clz, diff_name):
        sql = "INSERT INTO sql_diff (diff_type, diff_name, created) VALUES ('helloworld', %s, NOW())"
        return db().execute(sql, diff_name)

    @classmethod
    def delete(clz, diff_name):
        sql = 'DELETE FROM sql_diff WHERE diff_name=%s'
        return db().execute(sql, diff_name)

    @classmethod
    def iter(clz):
        sql = 'SELECT * FROM sql_diff ORDER BY diff_type, diff_name'
        new_conn = inferno.database.Connection.connect(force=True)
        return new_conn.iter(sql, clz=clz)
