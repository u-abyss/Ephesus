import mysql.connector as mydb

conn = mydb.connect(
    host="localhost",
    port="3306",
    user="root",
    password="Okyu8-0449",
    database="spotify",
)

conn.ping(reconnect=True)

# DB操作のカーソル
cur = conn.cursor()

cur.execute("SELECT * FROM playlist WHERE num_followers >= 100;")

rows = cur.fetchall()
for row in rows:
    print(row)

