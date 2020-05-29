from flask import Flask, request, jsonify, send_from_directory, abort
import psycopg2
from functions import register, generate_key, login, save_place, exit_handler, decode, response_to_location_request
import atexit
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './Uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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


@app.route("/get_info", methods=["POST"])
def get_image():
    if request.method == "POST":
        return response_to_location_request(request, cursor)


@app.route("/get_info/<sound_name>")
def get_sound(sound_name):
    try:
        return send_from_directory("./Uploads", filename=sound_name, as_attachment=False)
    except FileNotFoundError:
        abort(404)


if __name__ == "__main__":
    con = psycopg2.connect(user="postgres",
                           password="parola",
                           host="127.0.0.1",
                           port="5432",
                           database="TILNDB")
    cursor = con.cursor()

    app.run(debug=True, host="192.168.0.111")
    atexit.register(exit_handler, cursor, con)
