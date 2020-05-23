from flask import Flask, request, jsonify
import psycopg2
from functions import register, generate_key, login, save_place, exit_handler, decode
import atexit
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './Uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello')
def hello():
    return 'Hello, World'


@app.route('/api/register', methods=["POST"])
def register_route():
    if request.method == "POST":
        if request.is_json:
            return jsonify(register(request.json["email"], request.json["password"], cursor, con))


@app.route('/api/login', methods=["POST"])
def login_route():
    if request.method == "POST":
        if request.is_json:
            return jsonify(login(request.json["email"], request.json["password"], cursor, con))


@app.route('/api/decode', methods=["POST"])
def try_decode():
    if request.method == "POST":
        if request.is_json:
            return jsonify(decode(request.json["token"]))


@app.route('/api/set_location', methods=["POST"])
def save_location():
    if request.method == "POST":
        if request.is_json:
            return jsonify(save_place(request.json["token"], request.json["data"], cursor, con))


@app.route('/test_get_data', methods=["POST"])
def test_get_data():
    if request.method == "POST":
    #     if request.is_json:
    #         return jsonify(save_place(request.json["token"], request.json["data"], cursor, con))
    # return jsonify({"message": "succes"})
     # check if the post request has the file part
        if 'file' not in request.files:
            return {"message":"faile",
            "error":"No file"}
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return {"message":"faile",
            "error":"No name"}
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return {"message":"success",
            "status":"Save successfuly"}


@app.route('/test', methods=["GET"])
def test():
    # if request.method == "POST":
    #     if request.is_json:
    #         return jsonify(save_place(request.json["token"], request.json["data"], cursor, con))
    return jsonify({"message": "succes"})


if __name__ == "__main__":
    con = psycopg2.connect(user="postgres",
                           password="parola",
                           host="127.0.0.1",
                           port="5432",
                           database="tilndb")
    cursor = con.cursor()

    app.run(debug=True)
    atexit.register(exit_handler, cursor, con)
