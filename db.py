import mysql.connector
import cr

hostname = cr.hostname
username = cr.username
password = cr.password
database = cr.database


def get_entries():
    conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    cur = conn.cursor()
    cur.execute("""DELETE FROM ftb WHERE end < NOW()""")
    cur.execute("""SELECT brewery, food_truck, start, end FROM ftb ORDER BY end""")
    data = cur.fetchall()
    conn.commit()
    conn.close()
    return data


def get_eid():
    conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    cur = conn.cursor()
    cur.execute("""SELECT eid FROM ftb ORDER BY eid DESC""")
    data = cur.fetchall()
    rowCount = len(data)
    conn.close()
    if rowCount == 0:
        return 0
    else:
        return int(data[0][0]) + 1


def add_scrape(ftb):
    conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    cur = conn.cursor()
    stmt = ("INSERT IGNORE INTO ftb (brewery, food_truck, start, end, eid, uid) VALUES (%s, %s, %s, %s, %s, %s)")
    data = ftb
    cur.executemany(stmt, data)
    conn.commit()
    conn.close()

