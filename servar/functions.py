import jwt
import os 
import datetime
def register(email,password,cursor,con):
    cursor.execute("SELECT * FROM users WHERE email=%s;",(email,))
    data=cursor.fetchall()
    if len(data)>0:
        return {
            "message":"faile",
            "error":"User already exists"}
    cursor.execute("INSERT INTO users (email,password) VALUES (%s,%s);",(email,password))
    con.commit()
    return {
        "message":"succes"
    }



def login(email,password,cursor,con):
    cursor.execute("SELECT * FROM users WHERE email=%s;",(email,))
    data=cursor.fetchall()
    if len(data)==0:
        return {
            "message":"faile",
            "error":"User does not exists"}
    if data[0][2].strip()==password:
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': data[0][0]
            }
            token= jwt.encode(
                payload,
                open('SECRET_KEY.txt','r+').read(),
                algorithm='HS256'
            )

            return {
                "message":"succes",
                "token":token.decode("UTF-8")
            }
        except Exception as e:
            return e

def decode(token):
    """
    Decodes the auth token
    :param token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(token, open('SECRET_KEY.txt','r+').read())
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def save_place(token,place_data,cursor,con):
    resp=decode(token)
    if(type(resp)==str):
        return{
            "message":"fail",
            "error":resp
            }
    cursor.execute("INSERT INTO places (user_id,lat,lon,place_name,date) VALUES(%s,%s,%s,%s,%s)",(resp,place_data["lat"],place_data["lon"],place_data["place_name"],place_data["date"]))
    con.commit()
    return {
        "message":"succes"
    } 




def generate_key():
    f=os.urandom(24)
    open("SECRET_KEY.txt",'w').write(str(f))
    


def exit_handler(cursor,con):
    print ('My application is ending! Closing cursor and conn!!!')
    cursor.close()
    con.close()
    print("All clossed")