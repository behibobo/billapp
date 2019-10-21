import sqlite3

DB_PATH = './todo.db'
NOTSTARTED = 'Not Started'
INPROGRESS = 'In Progress'
COMPLETED = 'Completed'

def add_to_list(item):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('insert into items(item, status) values(?,?)', (item, NOTSTARTED))
        conn.commit()
        return {"item": item, "status": NOTSTARTED}
    except Exception as e:
        print('Error: ', e)
        return None

todo_list = {}

def get_all_items():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('select * from items')
        rows = c.fetchall()
        items = []
        for i in rows:
            items.append({"id": i[0], "task": i[1], "status": i[2]})
        return { "count": len(rows), "items": items }
    except Exception as e:
        print('Error: ', e)
        return None

def get_item(item_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("select * from items where id='%d'" % item_id)
        result = c.fetchone()
        return result
    except Exception as e:
        print('Error: ', e)
        return None
    
def update_status(id, task):
    
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('update items set item=? where id=?', (task, id))
        conn.commit()
        return {task: task}
    except Exception as e:
        print('Error: ', e)
        return None

def delete_item(id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('delete from items where id=?', (id,))
        conn.commit()
        return {'item': id}
    except Exception as e:
        print('Error: ', e)
        return None