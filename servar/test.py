from functions import select_by_location, create_mp3_from_text
import psycopg2
import sys
import os


create_mp3_from_text("Cand am fost in podul?", "./Uploads", "test_final")
# con = psycopg2.connect(user="postgres",
#                        password="parola",
#                        host="127.0.0.1",
#                        port="5432",
#                        database="tilndb")
# cursor = con.cursor()
# data = select_by_location(cursor, 1)
# for i in data:
#     print(i)


# cursor.close()
# con.close()
