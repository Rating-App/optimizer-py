import numpy as np
from scipy.sparse import csc_matrix
from sparsesvd import sparsesvd
import psycopg2

conn = psycopg2.connect("dbname='rateme' user='rateme' host='localhost' password='1'")

cur = conn.cursor()
cur.execute("""SELECT * from rateme_rating""")
rows = cur.fetchall()

users = []
users_set = set()
cards = []
cards_set = set()

for row in rows:
    # (66870, 432, 'neutral', 1545)
    rating_id, user_id, rating_val, card_id = row

    user_id = int(user_id)
    card_id = int(card_id)
    
    if user_id not in users_set:
        users.append(user_id)
        users_set.add(user_id)
    
    if card_id not in cards_set:
        cards.append(card_id)
        cards_set.add(card_id)

num_users = len(users)
num_cards = len(cards)

print("There are " + str(num_users) + " users and " + str(num_cards) + " cards")

# Rows: users, Columns: cards
# I.e. users x cards

matrix = csc_matrix((num_users, num_cards), dtype=np.int8).toarray()

for row in rows:
    # (66870, 432, 'neutral', 1545)
    rating_id, user_id, rating_val, card_id = row

    
