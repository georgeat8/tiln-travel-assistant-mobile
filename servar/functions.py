import jwt
import os
import datetime
from gtts import gTTS
from pydub import AudioSegment
import speech_recognition as sr
import dateparser
import io
from nltk.corpus import stopwords
import nltk


def register(email, password, cursor, con):
    cursor.execute("SELECT * FROM users WHERE email=%s;", (email,))
    data = cursor.fetchall()
    if len(data) > 0:
        return {
            "message": "faile",
            "error": "User already exists"}
    cursor.execute(
        "INSERT INTO users (email,password) VALUES (%s,%s);", (email, password))
    con.commit()
    return {
        "message": "succes"
    }


def login(email, password, cursor, con):
    cursor.execute("SELECT * FROM users WHERE email=%s;", (email,))
    data = cursor.fetchall()
    if len(data) == 0:
        return {
            "message": "faile",
            "error": "User does not exists"}
    if data[0][2].strip() == password:
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
            token = jwt.encode(
                payload,
                open('SECRET_KEY.txt', 'r+').read(),
                algorithm='HS256'
            )

            return {
                "message": "succes",
                "token": token.decode("UTF-8")
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
        payload = jwt.decode(token, open('SECRET_KEY.txt', 'r+').read())
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def save_place(token, place_data, cursor, con):
    resp = decode(token)
    if(type(resp) == str):
        return{
            "message": "fail",
            "error": resp
        }
    cursor.execute("INSERT INTO places (user_id,lat,lon,place_name,date) VALUES(%s,%s,%s,%s,NOW())",
                   (resp, place_data["lat"], place_data["lon"], place_data["place_name"]))
    con.commit()
    return {
        "message": "succes"
    }


def generate_key():
    f = os.urandom(24)
    open("SECRET_KEY.txt", 'w').write(str(f))


def exit_handler(cursor, con):
    print('My application is ending! Closing cursor and conn!!!')
    cursor.close()
    con.close()
    print("All clossed")


def convert_mp3_to_wav(path, name):
    sound = AudioSegment.from_mp3("{}/{}.mp3".format(path, name))
    sound.export("{}/{}.wav".format(path, name), format="wav")


def create_mp3_from_text(text, path, name):
    myobj = gTTS(text=text, lang='ro', slow=False)
    myobj.save("{}/{}.mp3".format(path, name))


def get_text_from_audio(path_to_audio):
    r = sr.Recognizer()
    with sr.AudioFile("./data.wav") as source:
        audio = r.listen(source, phrase_time_limit=5)
    try:
        propozitie = r.recognize_google(audio, language='ro-RO')
        return {"message": "success",
                "phrase": propozitie}
    except LookupError:
        # print("Could not understand audio")
        return {"message": "faile",
                "error": "Could not understand audio"}
    except sr.UnknownValueError:
        # print("I did not understand you")
        return {"message": "faile",
                "error": "I did not understand you"}
    except sr.RequestError as e:
        # print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return {"message": "faile",
                "error": "Could not request results from Google Speech Recognition service; {0}".format(e)
                }


def parse_phrase(phrase):
    stop_words = set(stopwords.words("romanian"))
    other_words = ["ora", "Unde"]

    words = nltk.word_tokenize(phrase)
    without_stop_words = [
        word for word in words if (not word in stop_words)]
    without_stop_words = [
        word for word in without_stop_words if (not word in other_words)]

    prop = ''
    for i in without_stop_words:
        prop += " "+i
    prop = prop.strip()


def get_time(prop):
    h = dateparser.parse(prop, languages=['ro'])
    return h
