from settings import DB_LOCATION
import sqlite3

"""
    The DatabaseConnection module provides a slightly higher-level abstraction for making database queries.
    When the module is loaded, a database connection is initialized and scripts are run to ensure the database tables exist.
    
    TODO: we may at some point want to replace this with something more robust
"""

CREATE_GAME_TABLE_SCRIPT = '''
    CREATE TABLE IF NOT EXISTS game(
      p1_type TEXT,
      p2_type TEXT,
      date_played DATE,
      num_moves INTEGER
    );
'''

CREATE_BOARD_TABLE_SCRIPT = '''
    CREATE TABLE IF NOT EXISTS board(
      id TEXT PRIMARY KEY,
      p00 TINYINT, p01 TINYINT, p02 TINYINT, p03 TINYINT, p04 TINYINT, p05 TINYINT, p06 TINYINT, p07 TINYINT, p08 TINYINT,
      p10 TINYINT, p11 TINYINT, p12 TINYINT, p13 TINYINT, p14 TINYINT, p15 TINYINT, p16 TINYINT, p17 TINYINT, p18 TINYINT,
      p20 TINYINT, p21 TINYINT, p22 TINYINT, p23 TINYINT, p24 TINYINT, p25 TINYINT, p26 TINYINT, p27 TINYINT, p28 TINYINT,
      p30 TINYINT, p31 TINYINT, p32 TINYINT, p33 TINYINT, p34 TINYINT, p35 TINYINT, p36 TINYINT, p37 TINYINT, p38 TINYINT,
      p40 TINYINT, p41 TINYINT, p42 TINYINT, p43 TINYINT, p44 TINYINT, p45 TINYINT, p46 TINYINT, p47 TINYINT, p48 TINYINT,
      p50 TINYINT, p51 TINYINT, p52 TINYINT, p53 TINYINT, p54 TINYINT, p55 TINYINT, p56 TINYINT, p57 TINYINT, p58 TINYINT,
      p60 TINYINT, p61 TINYINT, p62 TINYINT, p63 TINYINT, p64 TINYINT, p65 TINYINT, p66 TINYINT, p67 TINYINT, p68 TINYINT,
      p70 TINYINT, p71 TINYINT, p72 TINYINT, p73 TINYINT, p74 TINYINT, p75 TINYINT, p76 TINYINT, p77 TINYINT, p78 TINYINT,
      p80 TINYINT, p81 TINYINT, p82 TINYINT, p83 TINYINT, p84 TINYINT, p85 TINYINT, p86 TINYINT, p87 TINYINT, p88 TINYINT,
      next_player TINYINT,
      wins INTEGER,
      losses INTEGER,
      ties INTEGER,
      FOREIGN KEY(game_id) REFERENCES game(rowid)
    ) WITHOUT ROWID;
'''

_connection = None
_connection_open = False


def init():
    """ Initializes tables used by this application """
    global _connection, _connection_open
    connection = None
    if _connection and _connection_open:
        connection = _connection
    else:
        connection = sqlite3.connect(DB_LOCATION)
        _connection = connection
        _connection_open = True

    cursor = connection.cursor()
    cursor.execute(CREATE_GAME_TABLE_SCRIPT)
    cursor.execute(CREATE_BOARD_TABLE_SCRIPT)

    connection.commit()


def query(sql):
    """ Executes the given sql statement and returns the cursor object with the results """
    global _connection, _connection_open
    if not (_connection and _connection_open):
        close()
        init()

    cursor = _connection.cursor()
    return cursor.execute(sql)


def execute(sql):
    """ Executes the given sql statement """
    global _connection, _connection_open
    if not (_connection and _connection_open):
        close()
        init()

    cursor = _connection.cursor()
    cursor.execute(sql)
    _connection.commit()


def close():
    """ Closes the connection until init, query, or execute is called again"""
    global _connection, _connection_open
    if _connection:
        _connection.close()
        _connection_open = False


# Call init when the module is loaded
init()
