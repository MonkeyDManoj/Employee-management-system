from flask import g
import sqlite3

def connect_to_data():
    sql = sqlite3.connect('C:/Users/demoa/OneDrive/Desktop/project/data.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_data():
    if not hasattr(g, 'data_db'):
        g.data_db = connect_to_data()
    return g.data_db