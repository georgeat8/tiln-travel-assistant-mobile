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
from string import Template
from random import choice
import datetime as dt
from datetime import date, datetime
from flask import request, jsonify, send_from_directory, abort
from werkzeug.utils import secure_filename


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
                'exp': dt.datetime.utcnow() + dt.timedelta(days=1),
                'iat': dt.datetime.utcnow(),
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
    path = os.path.join(os.path.abspath("."), "Uploads",
                        "{}.mp3".format(name))
    myobj = gTTS(text=text, lang='ro', slow=False)
    myobj.save(path.format(path, name))
    return path


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


def create_time_for_phrase(data_time):
    return data_time.strftime("%m/%d/%Y %H:%M")


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


def select_by_location(cursor, user_id):
    cursor.execute(
        "SELECT * FROM places where user_id=%s order by date desc;", (user_id,))
    data = cursor.fetchall()
    return data


def from_text_to_location(user_id, parsed_phrase, cursor):

    time = get_time(parsed_phrase)

    if time != None:
        date, time = time
        db_infos = get_data_from_database(cursor, date, user_id)
        return get_location_for_time(db_infos, time)
    else:
        return None


def create_phrase(data, locatie):
    adv_timp = ["In data de", "Pe data de", "Pe", "La data de", "La"]

    verbe = ["ai fost la", "ai mers la", "te-ai aflat la",
             "te aflai la", "erai prezent la", "erai la"]

    s = Template('$adv $date, $action $location.')
    time = date.today().strftime("%m/%d/%Y")
    if(time in data):
        return (s.substitute(adv=choice((adv_timp)+["Astazi"]), date=data, action=choice(verbe), location=locatie))
    else:
        return (s.substitute(adv=choice(adv_timp), date=data, action=choice(verbe), location=locatie))


def generate_answer(path, name, uid, cursor):
    convert_mp3_to_wav(path, name)
    text = get_text_from_audio(path, name)
    parsed_phrase = parse_phrase(text)

    text_parse = copy.deepcopy(parsed_phrase)
    # texting = "acum 10 zile"

    location = from_text_to_location(uid, text_parse, cursor)
    if location != None:
        # Are data
        date = location[4]
        locatie = location[3]
        time_and_date = create_time_for_phrase(date)
        result = create_phrase(time_and_date, locatie)
        path = create_mp3_from_text(
            result, "./Uploads", "data{}".format(uid))
        return path
    else:
        data = select_by_location(cursor, uid)
        zona = None
        for i in data:
            if i[3].lower() in text["phrase"]:
                zona = i
                break
        result = ''
        if zona != None:
            date = zona[4]
            locatie = zona[3]
            time_and_date = create_time_for_phrase(date)
            result = create_phrase(time_and_date, locatie)
        else:
            result = "Nu am gasit nimic in istoricul tau"
        path = create_mp3_from_text(
            result, "./Uploads", "data{}".format(uid))
        return path


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


def response_to_location_request(request, cursor):
    if 'file' not in request.files:
        return {"message": "faile",
                "error": "No file"}
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return {"message": "faile",
                "error": "No name"}
    if file:
        filename = secure_filename(file.filename)
        path_of_save = os.path.join(
            "./Uploads")
        print(request.headers)
        uid = decode(request.headers["Authorization"])
        name = "data{}".format(uid)
        file.save(os.path.join(path_of_save, name+".mp3"))
        path_of_result = generate_answer(path_of_save, name, uid, cursor)

        try:
            return send_from_directory(path_of_save, filename=name+".mp3", as_attachment=True)
        except FileNotFoundError:
            abort(404)
