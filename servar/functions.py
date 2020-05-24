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
import copy
import inspect


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
    location = os.path.join(os.path.abspath('.'), "Uploads", name+".mp3")
    sound = AudioSegment.from_mp3(location)
    dest = "{}/{}.wav".format(path, name)
    sound.export(dest, format="wav")


def create_mp3_from_text(text, path, name):
    myobj = gTTS(text=text, lang='ro', slow=False)
    myobj.save("{}/{}.mp3".format(path, name))


def get_text_from_audio(path_to_audio, name):
    r = sr.Recognizer()
    with sr.AudioFile("./{}/{}.wav".format(path_to_audio, name)) as source:
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
    prop = replace(phrase["phrase"])

    words = nltk.word_tokenize(prop)

    without_stop_words = [
        word for word in words if (not word in stop_words)]
    without_stop_words = [
        word for word in without_stop_words if (not word in other_words)]

    prop = ''
    for i in without_stop_words:
        prop += " "+i
    prop = prop.strip()
    return prop


def get_time(ask_for_time):
    h = dateparser.parse(ask_for_time, languages=['ro'])
    if h != None:
        return h.strftime("%m/%d/%Y"), h.strftime("%H:%M:%S")
    else:
        return None


def calcuate_time_dif(bd_time, time):

    bd_time = bd_time.strftime("%H:%M:%S")
    db_t = bd_time.split(":")
    t = time.split(":")
    for i in range(3):
        db_t[i] = int(db_t[i])
        t[i] = int(t[i])
    result = []
    result.append(abs(db_t[0]-t[0])*(10**2))
    result.append(abs(db_t[1]-t[1]))
    return sum(result)


def get_location_for_time(dates, ask_time):
    info = None
    closest = float('Inf')
    for i in dates:
        time_dist = calcuate_time_dif(i[4], ask_time)
        if closest > time_dist:
            info = i
            closest = time_dist
    return info


def get_data_from_database(cursor, date, user_id):
    cursor.execute(
        "SELECT * FROM places where date_trunc('day', date) =%s and user_id=%s;", (date, user_id))
    data = cursor.fetchall()
    return data
# SELECT * FROM places where date_trunc('day', date) ='2020-05-14';


def from_text_to_location(user_id, parsed_phrase, cursor):

    time = get_time(parsed_phrase)

    if time != None:
        date, time = time
        db_infos = get_data_from_database(cursor, date, user_id)
        return get_location_for_time(db_infos, time)
    else:
        return None


def generate_answer(path, name, uid, cursor):
    convert_mp3_to_wav(path, name)
    text = get_text_from_audio(path, name)
    parsed_phrase = parse_phrase(text)

    text_parse = copy.deepcopy(parsed_phrase)
    texting = "acum 10 zile"

    location = from_text_to_location(uid, texting, cursor)
    if location != None:
        # Are data
        # print(location)
        return location
    else:
        # Nu are data doar locatie
        # print(location)
        return location


def replace(phrase):
    to_change = [
        ["un an", "1 an"],
        ["o luna", " luna"],
        ["o saptamana", "1 saptamana"],
        ["o zi", "1 zi"],
        ["o ora", "1 ora"],
        ["acuma", 'acum'],
        ['două', "2"],
        ['trei', "3"],
        ["patru", "4"],
        ["cinci", "5"],
        ["șase", "6"],
        ["șapte", "7"],
        ["opt", "8"],
        ["nouă", "9"],
        ["zece", '10']
    ]
    for i in to_change:
        phrase = phrase.replace(i[0], i[1])
    return phrase
