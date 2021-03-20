import sqlite3
# from reneQRcode import getID
# from sortingModel import sortingResult

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def update_task(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE user
              SET points = points + 1 
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

def delete_task(conn):
    sql = ''' DELETE from user'''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def main():
    database = "database.db"

    # get the ID of the user from the QR code
    # ID = getID()
    ID = 1

    # get the result of the sorting
    # result = sortingResult()
    # result = 'recycling'

    # create a database connection
    conn = create_connection(database)
    with conn:
        # for updating a user's reward total
        update_task(conn, (ID,))

        # for wiping all users from the db
        # delete_task(conn)


if __name__ == '__main__':
    main()