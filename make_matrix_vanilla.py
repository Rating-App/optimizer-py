import numpy as np
from scipy.sparse import csc_matrix
from sparsesvd import sparsesvd
import psycopg2
import time
import sys

RANK = 100

conn = psycopg2.connect("dbname='rateme' user='rateme' host='localhost' password='1'")

cur = conn.cursor()
cur.execute("""SELECT * from rateme_rating""")
rows = cur.fetchall()

users = {}
cards = {}

for row in rows:
    # (66870, 432, 'neutral', 1545)
    rating_id, user_id, rating_val, card_id = row

    user_id = int(user_id)
    card_id = int(card_id)
    
    if user_id not in users:
        users[user_id] = len(users)
    
    if card_id not in cards:
        cards[card_id] = len(cards)

num_users = len(users)
num_cards = len(cards)

print("There are " + str(num_users) + " users and " + str(num_cards) + " cards")

def todata(rating_val):
    if rating_val == "completely not interested":
        return -2
    elif rating_val == "not interested":
        return -1
    elif rating_val == "neutral":
        return 0
    elif rating_val == "interested":
        return 1
    elif rating_val == "very interested":
        return 2
    else:
        print("ERROR")
        return 0

# Rows: users, Columns: cards
# I.e. users x cards

mrow = []
mcol = []
data = []

for row in rows:
    # (66870, 432, 'neutral', 1545)
    rating_id, user_id, rating_val, card_id = row

    mrow.append(users[user_id])
    mcol.append(cards[card_id])
    data.append(todata(rating_val))

def project_low_rank(matrix):
    ut, s, vt = sparsesvd(csc_matrix(matrix), RANK)

    return ut.T @ np.diag(s) @ vt

observed_padded = csc_matrix((data, (mrow, mcol)), shape=(num_users, num_cards))
mask = csc_matrix((np.ones(len(data)), (mrow, mcol)), shape=(num_users, num_cards)).toarray()
M = csc_matrix((np.zeros(len(data)), (mrow, mcol)), shape=(num_users, num_cards)).toarray()
N = csc_matrix((np.zeros(len(data)), (mrow, mcol)), shape=(num_users, num_cards)).toarray()

print("iter, time, step, dist")
starting_time = time.time()
for i in range(100):
    M = project_low_rank(M + (observed_padded - M*mask))

    print(i, time.time() - starting_time,
                np.linalg.norm(N-M),
                np.linalg.norm(M - observed_padded - M*(1-mask)))
    N = M
