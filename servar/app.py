from flask import Flask,request,jsonify
import psycopg2
from functions import register,generate_key,login,save_place,exit_handler,decode
import atexit



app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'


@app.route('/api/register',methods=["POST"])
def register_route():
    if request.method=="POST":
        if request.is_json:
            return jsonify(register(request.json["email"],request.json["password"],cursor,con))


@app.route('/api/login',methods=["POST"])
def login_route():
    if request.method=="POST":
        if request.is_json:
            return jsonify(login(request.json["email"],request.json["password"],cursor,con))


@app.route('/api/decode',methods=["POST"])
def try_decode():
    if request.method=="POST":
        if request.is_json:
            return jsonify(decode(request.json["token"]))


@app.route('/api/set_location',methods=["POST"])
def save_location():
    if request.method=="POST":
        if request.is_json:
            return jsonify(save_place(request.json["token"],"Mere",cursor,con))





if __name__=="__main__":
    con= psycopg2.connect(user = "postgres",
                    password = "parola",
                    host = "127.0.0.1",
                    port = "5432",
                    database = "tilndb")
    cursor = con.cursor()

    app.run(debug=True)
    atexit.register(exit_handler,cursor,con)
