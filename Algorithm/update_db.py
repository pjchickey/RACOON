import psycopg2
# from reneQRcode import getUsername
# from sortingModel import sortingResult

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = psycopg2.connect('postgresql://iyrxjafwmybqog:047647631db0ac1b3d727d7edd5b9e4c299586131585e1b6d41b2bc98e412521@ec2-52-7-115-250.compute-1.amazonaws.com:5432/dfmfctp63eg654')
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
    sql = ''' UPDATE users
              SET points = points + %s 
              WHERE username = %s;'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

def delete_task(conn):
    sql = ''' DELETE from user'''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def main(username):
    database = "database.db"

    # get the ID of the user from the QR code
    # username = getUsername()
    #username = 'pjchickey'

    # get the result of the sorting
    # result = sortingResult()
    result = 'trash'
    if result == 'recycling':
        points = 2
    else:
        points = 1

    # create a database connection
    conn = create_connection(database)
    with conn:
        # for updating a user's reward total
        update_task(conn, (points, username))

        # for wiping all users from the db
        # delete_task(conn)


if __name__ == '__main__':
    main('pjchickey')