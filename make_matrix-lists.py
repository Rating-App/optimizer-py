import psycopg2

conn = psycopg2.connect("dbname='rateme' user='rateme' host='localhost' password='1'")

cur = conn.cursor()
cur.execute("""SELECT * from rateme_rating""")
rows = cur.fetchall()

users = []
movies = []

for row in rows:
    # (66870, 432, 'neutral', 1545)
    rating_id, user_id, rating_val, movie_id = row

    user_id = int(user_id)
    movie_id = int(movie_id)
    
    if user_id not in users:
        users.append(user_id)
    
    if movie_id not in movies:
        movies.append(movie_id)

print("There are " + str(len(users)) + " users and " + str(len(movies)) + " movies")

