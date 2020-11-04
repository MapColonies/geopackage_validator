import sqlite3


def init(geo_file) -> object:
    """
    initialize instance of sql cursor object to the package
    """
    conn = sqlite3.connect(geo_file)
    return conn.cursor()


def get_tables(cursor) -> list:
    """ query that scan all tables included on given geopackage"""
    cursor.execute("SELECT name FROM sqlite_master where type = 'table'")
    return [table[0] for table in cursor]


def get_indices(cursor) -> list:
    """ query that scan all indices included on given geopackage"""
    cursor.execute("SELECT name FROM sqlite_master where type = 'index'")
    return [table[0] for table in cursor]


def get_triggers(cursor):
    """ query that scan all triggers included on given geopackage"""
    cursor.execute("SELECT name FROM sqlite_master where type = 'trigger'")
    return [table[0] for table in cursor]


def list_table_columns(cursor, table_name):
    """ query that return all columns name in main table of content in geopackage"""
    cursor.execute("SELECT * FROM " + table_name)
    return list(map(lambda x: x[0], cursor.description))


def list_tile_matrix_data(cursor, table_name="gpkg_tile_matrix"):
    """ query that return all data included on gpkg_tile_matrix table """
    cursor.execute("SELECT * FROM "+table_name)
    return cursor.fetchall()
