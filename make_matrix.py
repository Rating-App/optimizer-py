import numpy, scipy.sparse
from sparsesvd import sparsesvd
import psycopg2

conn = psycopg2.connect("dbname='rateme' user='rateme' host='localhost' password='1'")

cur = conn.cursor()
cur.execute("""SELECT * from rateme_rating""")
rows = cur.fetchall()

users = []
users_set = set()
movies = []
movies_set = set()

for row in rows:
    # (66870, 432, 'neutral', 1545)
    rating_id, user_id, rating_val, movie_id = row

    user_id = int(user_id)
    movie_id = int(movie_id)
    
    if user_id not in users_set:
        users.append(user_id)
        users_set.add(user_id)
    
    if movie_id not in movies_set:
        movies.append(movie_id)
        movies_set.add(movie_id)

print("There are " + str(len(users)) + " users and " + str(len(movies)) + " movies")


