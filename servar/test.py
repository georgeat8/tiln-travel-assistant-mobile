from functions import from_text_to_location,generate_answer,create_mp3_from_text,get_time
import psycopg2
import sys
import os
create_mp3_from_text("Unde am fost acum 9 zile ","./Uploads","test_final")

con = psycopg2.connect(user="postgres",
                           password="parola",
                           host="127.0.0.1",
                           port="5432",
                           database="tilndb")
cursor = con.cursor()
# os.system("start ./Uploads/test.mp3")
# raw=get_data_from_database(cursor,'2020-05-23',1)
# # print(raw)
text="acum 9 zile"
# date,time=get_time(text)
# print(date,time)
# h=from_text_to_location(1,text,cursor)
h=generate_answer("./Uploads","test_final",1,cursor)
print(h)
# text.replace('o saptamana','1 saptamana')
# print(text)
# print(replace(text))
# # print(date[4],time)
# raw=calcuate_time_dif(raw[0][4],time)
# print(raw)
# response(1,"acum 1 ora",cursor)
cursor.close()
con.close()