import sqlite3
from sqlite3 import Error


def create_connection(db_file:'database file') -> 'Connection object':
    """ create a database connection to the SQLite database
        specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn:'Connection object', create_table_sql: 'create_table_sql: a CREATE TABLE statement') -> None:
    """ create a table from the create_table_sql statement"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def database_creation():
    database = r"dataBase.db"

    sql_create_ingredients_table = """ CREATE TABLE IF NOT EXISTS ingredients (
                                        id_ing integer PRIMARY KEY AUTOINCREMENT,
                                        name text NOT NULL,
                                        price real NOT NULL,
                                        date DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
                                        weight real NOT NULL,
                                        note text
                                    ); """

    sql_create_dish_table = """CREATE TABLE IF NOT EXISTS dish (
                                    id_dish integer PRIMARY KEY AUTOINCREMENT,
                                    name text NOT NULL,
                                    price real NOT NULL,
                                    date DATETIME NOT NULL DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')),
                                    weight real NOT NULL,
                                    note text
                                );"""

    sql_create_amount_table = """CREATE TABLE IF NOT EXISTS amount (
                                    ing_amount real NOT NULL,
                                    ing_quanity integer NOT NULL,
                                    id_ing integer NOT NULL,
                                    id_dish integer NOT NULL ,
                                    foreign key (id_ing) references ingredients(id_ing),
	                            foreign key (id_dish)references dish(id_dish),
	                            primary key (id_ing, id_dish)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create tables
        create_table(conn, sql_create_ingredients_table)
        create_table(conn, sql_create_dish_table)
        create_table(conn, sql_create_amount_table)

    else:
        print("Error! cannot create the database connection.")


class UseBaseData:
    def __init__(self,conn) -> None:
        self.connect = conn
        self.cursor = conn.cursor()

    def __enter__(self) -> 'cursor':
        return self.cursor 
        

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        self.connect.commit()

def create_ingredient(conn:'param conn', ingredient:'(name, price, weight, note)') -> None:
    """    Create a new ingredient into the ingredients table"""
    sql = ''' INSERT INTO ingredients (name, price, weight, note)
              VALUES(?,?,?,?) '''
    with UseBaseData(conn) as cursor:
        cursor.execute(sql, ingredient)
        

def create_dish(conn:'param conn', dish:'(name,price,weight,note)') -> None:
    """    Create a new dish"""
    sql = ''' INSERT INTO dish(name,price,weight,note)
              VALUES(?,?,?,?) '''
    with UseBaseData(conn) as cursor:
        cursor.execute(sql, dish)


def create_amount(conn:'param conn', amount:'(ing_amount, ing_quanity, id_ing, id_dish') -> None:
    """    Create a new amount"""
    sql = ''' INSERT INTO amount(ing_amount, ing_quanity, id_ing, id_dish)
              VALUES(?,?,?,?) '''
    with UseBaseData(conn) as cursor:
        cursor.execute(sql, amount)


def update_ingredient(conn:'param conn', ingredient:'(name, price, weight, note, id_ing)') -> None:
    """    update ingredient    """
    sql = ''' UPDATE ingredients
              SET name = ? ,
                  price = ? ,
                  weight = ? ,
                  note = ? 
              WHERE id_ing = ?'''
    with UseBaseData(conn) as cursor:
        cursor.execute(sql, ingredient)


def update_dish(conn:'param conn', dish:'(name,price,weight,note, id_dish )') -> None:
    """    update dish    """
    sql = ''' UPDATE dish
              SET name = ? ,
                  price = ? ,
                  weight = ? ,
                  note = ? 
              WHERE id_dish = ?'''
    with UseBaseData(conn) as cursor:
        cursor.execute(sql, dish)


def update_amount(conn:'param conn', amount:'(ing_amount, ing_quanity, id_ing, id_dish') -> None:
    """    update amount    """
    sql = ''' UPDATE amount
              SET ing_amount = ? ,
                  ing_quanity = ? 
              WHERE id_ing = ? AND id_dish = ?'''
    with UseBaseData(conn) as cursor:
        cursor.execute(sql, amount)


def select_all_ingredients(conn) -> list:
    """    Query all ingredient    """
    with UseBaseData(conn) as cursor:
        cursor.execute("SELECT * FROM ingredients")
        rows = cursor.fetchall()
        ingredients = []
        ingredients = [row for row in rows]
        return ingredients


def select_all_dish(conn) -> list:
    """    Query all dish    """
    with UseBaseData(conn) as cursor:
        cursor.execute("SELECT * FROM dish")
        rows = cursor.fetchall()
        dishes = []
        dishes = [row for row in rows]
        return dishes


def select_ingredients(conn,id_dish) -> list:
    """    Query ingredients for dish    """
    with UseBaseData(conn) as cursor:
        cursor.execute("SELECT * FROM amount WHERE id_dish=?", (id_dish,))
        rows = cursor.fetchall()
        ingredients = []
        ingredients = [row for row in rows]
        return ingredients 
    

def main():
    database = r"dataBase.db"

    # create a database connection
    conn = create_connection(database)
    database_creation()
    with conn:
        print(select_all_ingredients(conn))
        print(select_all_dish(conn))
        print(select_ingredients(conn,515))

main()
