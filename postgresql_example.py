import psycopg2

try:
    conn = psycopg2.connect("dbname='rateme' user='rateme' host='localhost' password='1'")
    
    cur = conn.cursor()
    cur.execute("""SELECT * from rateme_rating""")
    rows = cur.fetchall()

    for row in rows:
        print(row)

except:
    print("I am unable to connect to the database")
