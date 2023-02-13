from flask import Flask, request, Response
import sqlite3

app = Flask(__name__)

con = sqlite3.connect("../database/cqadb.sqlite",check_same_thread=False)
con.execute("PRAGMA foreign_keys = ON")
cur = con.cursor()

# * /login1?username=<username>&password=<password>
@app.route("/login1")
def login1():
    username = request.args.get("username")
    password = request.args.get("password")
    res = cur.execute("SELECT * FROM users WHERE username = ? AND password = ?",(username,password))
    if res.fetchone() is None:
        return {"auth_status":False}
    else:
        return {"auth_status":True}
# {
#     "auth_status":<bool>
# }


# * /login2
# {
#   "username": <string>,
#   "password": <string>
# }
@app.route("/login2")
def login1():
    username = request.json.get("username")
    password = request.json.get("password")
    res = cur.execute("SELECT * FROM users WHERE username = ? AND password = ?",(username,password))
    if res.fetchone() is None:
        return {"auth_status":False}
    else:
        return {"auth_status":True}
# {
#     "auth_status":<bool>
# }


# * /register?username=<string>&password=<string>
@app.route("/register",methods=["POST"])
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
# {
#     "register_status":<bool>
# }


# * /upvote/post?post_id=<int>
@app.route("/upvote/post",methods=["POST"])
def upvote_post():
    post_id = request.args.get("post_id")
    cur.execute("UPDATE posts SET upvotes = upvotes + 1 WHERE post_id = ?",(post_id,))
    con.commit()
    return Response(status=204)
# no response body


# * /downvote/post?post_id=<int>
@app.route("/downvote/post",methods=["POST"])
def downvote_post():
    post_id = request.args.get("post_id")
    cur.execute("UPDATE posts SET upvotes = upvotes - 1 WHERE post_id = ?",(post_id,))
    con.commit()
    return Response(status=204)
# no response body


# * /upvote/reply?reply_id=<int>
@app.route("/upvote/reply",methods=["POST"])
def upvote_reply():
    reply_id = request.args.get("reply_id")
    cur.execute("UPDATE replies SET upvotes = upvotes + 1 WHERE reply_id = ?",(reply_id,))
    con.commit()
    return Response(status=204)
# no response body


# * /downvote/reply?reply_id=<int>
@app.route("/downvote/reply",methods=["POST"])
def downvote_reply():
    reply_id = request.args.get("reply_id")
    cur.execute("UPDATE replies SET upvotes = upvotes - 1 WHERE reply_id = ?",(reply_id,))
    con.commit()
    return Response(status=204)
# no response body
