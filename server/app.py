from flask import Flask,request
import sqlite3

app = Flask(__name__)

con = sqlite3.connect("../database/cqadb.sqlite",check_same_thread=False)
con.execute("PRAGMA foreign_keys = ON")
cur = con.cursor()

@app.route("/login")
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    res = cur.execute("SELECT * FROM users WHERE username = ? AND password = ?",(username,password))
    if res.fetchone() is None:
        return {"auth_status":False}
    else:
        return {"auth_status":True}

@app.route("/register")
def register():
    username = request.args.get("username")
    password = request.args.get("password")
    res = cur.execute("SELECT * FROM users WHERE username = ?",(username,))
    if res.fetchone() is None:
        cur.execute("INSERT INTO users(username,password) VALUES (?,?)",(username,password))
        con.commit()
        return {"register_status":True}
    else:
        return {"register_status":False}
