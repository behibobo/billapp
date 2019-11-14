import sqlite3

DB_PATH = './bills.db'


def add_item(row):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('insert into bills(customer_serial, bill_serial,payment_serial,amount,customer,valid_to,chasis_serial) values(?,?,?,?,?,?,?)', 
        (row[0], row[1],row[2],row[3],row[4],row[5],row[6]))
        conn.commit()
    except Exception as e:
        print('Error: ', e)
        return None

def get_bill(bill_serial):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select * from bills where bill_serial='%s' or customer_serial = '%s'" %(bill_serial, bill_serial))
        result = c.fetchone()
        return result
    except Exception as e:
        print('Error: ', e)
        return None

def get_all_bills():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select * from bills")
        result = c.fetchall()
        return result
    except Exception as e:
        print('Error: ', e)
        return None