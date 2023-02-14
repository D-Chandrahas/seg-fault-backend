from flask import Flask, request, Response
import sqlite3
import math

app = Flask(__name__)

con = sqlite3.connect("../database/cqadb.sqlite",check_same_thread=False)
con.execute("PRAGMA foreign_keys = ON")
cur = con.cursor()

# * /login?username=<string:250>&password=<string:250>
@app.route("/login",methods=["GET"])
def login():
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
# ----------------------------------------------

# * /register?username=<string:250>&password=<string:250>
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
# ----------------------------------------------

# * /post/upvote?post_id=<int>
@app.route("/post/upvote",methods=["POST"])
def upvote_post():
    post_id = request.args.get("post_id",type=int)
    cur.execute("UPDATE posts SET upvotes = upvotes + 1 WHERE post_id = ?",(post_id,))
    con.commit()
    return Response(status=204)
# no response body
# ----------------------------------------------

# * /post/downvote?post_id=<int>
@app.route("/post/downvote",methods=["POST"])
def downvote_post():
    post_id = request.args.get("post_id",type=int)
    cur.execute("UPDATE posts SET upvotes = upvotes - 1 WHERE post_id = ?",(post_id,))
    con.commit()
    return Response(status=204)
# no response body
# ----------------------------------------------

# * /reply/upvote?reply_id=<int>
@app.route("/reply/upvote",methods=["POST"])
def upvote_reply():
    reply_id = request.args.get("reply_id",type=int)
    cur.execute("UPDATE replies SET upvotes = upvotes + 1 WHERE reply_id = ?",(reply_id,))
    con.commit()
    return Response(status=204)
# no response body
# ----------------------------------------------

# * /reply/downvote?reply_id=<int>
@app.route("/reply/downvote",methods=["POST"])
def downvote_reply():
    reply_id = request.args.get("reply_id",type=int)
    cur.execute("UPDATE replies SET upvotes = upvotes - 1 WHERE reply_id = ?",(reply_id,))
    con.commit()
    return Response(status=204)
# no response body
# ----------------------------------------------

# * /post/create
# {
#     "user_id": <int>,
#     "title": <string:500>,
#     "tags": [
#         <string:50> :10
#     ],
#     "body": <string>
# }
@app.route("/post/create",methods=["POST"])
def create_post():
    user_id = request.json.get("user_id")
    title = request.json.get("title")
    tags = "\n".join(request.json.get("tags"))
    body = request.json.get("body")
    cur.execute("INSERT INTO posts(user_id,title,tags,body) VALUES (?,?,?,?)",(user_id,title,tags,body))
    con.commit()
    return Response(status=204)
# no response body
# ----------------------------------------------

# * /post/edit
# {
#     "post_id": <int>,
#     "title": <string:500>,
#     "tags":[
#         <string:50> :10
#     ],
#     "body": <string>
# }
@app.route("/post/edit",methods=["POST"])
def edit_post():
    post_id = request.json.get("post_id")
    title = request.json.get("title")
    tags = "\n".join(request.json.get("tags"))
    body = request.json.get("body")
    cur.execute("UPDATE posts SET title = ?, tags = ?, body = ? WHERE post_id = ?",(title,tags,body,post_id))
    con.commit()
    return Response(status=204)
# no response body
# ----------------------------------------------

# * /post/delete?post_id=<int>
@app.route("/post/delete",methods=["POST"])
def delete_post():
    post_id = request.args.get("post_id",type=int)
    cur.execute("DELETE FROM replies WHERE post_id = ?",(post_id,))
    cur.execute("DELETE FROM posts WHERE post_id = ?",(post_id,))
    con.commit()
    return Response(status=204)
# no response body
# ----------------------------------------------

# * /reply/create
# {
#     "post_id": <int>,
#     "user_id": <int>,
#     "body": <string>,
# }
@app.route("/reply/create",methods=["POST"])
def create_reply():
    post_id = request.json.get("post_id")
    user_id = request.json.get("user_id")
    body = request.json.get("body")
    cur.execute("INSERT INTO replies(post_id,user_id,body) VALUES (?,?,?)",(post_id,user_id,body))
    con.commit()
    return Response(status=204)
# no response body
# ----------------------------------------------

# * /reply/edit
# {
#     "reply_id": <int>,
#     "body": <string>,
# }
@app.route("/reply/edit",methods=["POST"])
def edit_reply():
    reply_id = request.json.get("reply_id")
    body = request.json.get("body")
    cur.execute("UPDATE replies SET body = ? WHERE reply_id = ?",(body,reply_id))
    con.commit()
    return Response(status=204)
# no response body
# ----------------------------------------------

# * /reply/delete?reply_id=<int>
@app.route("/reply/delete",methods=["POST"])
def delete_reply():
    reply_id = request.args.get("reply_id",type=int)
    cur.execute("DELETE FROM replies WHERE reply_id = ?",(reply_id,))
    con.commit()
    return Response(status=204)
# no response body
# ----------------------------------------------
# ? posts per page const or variable?
# * /user/posts?user_id=<int>&page=<int>&order_by=<string:[time_asc, time_desc, votes_asc, votes_desc]>
@app.route("/user/posts",methods=["GET"])
def get_user_posts():
    POSTS_PER_PAGE = 15
    user_id = request.args.get("user_id",type=int)
    order_by = request.args.get("order_by",type=str)
    page = request.args.get("page",type=int)
    posts = {"posts":[]}
    res = cur.execute("SELECT COUNT(*) FROM posts WHERE user_id = ?",(user_id,))
    posts["total_pages"] = math.ceil(res.fetchone()[0]/POSTS_PER_PAGE)
    if order_by == "time_asc": order_by = "time ASC"
    elif order_by == "time_desc": order_by = "time DESC"
    elif order_by == "votes_asc": order_by = "upvotes ASC"
    elif order_by == "votes_desc": order_by = "upvotes DESC"
    res = cur.execute(f"SELECT * FROM posts WHERE user_id = ? ORDER BY {order_by} LIMIT ? OFFSET ?",(user_id, POSTS_PER_PAGE,(page-1)*POSTS_PER_PAGE))
    for row in res:
        post = {}
        post["post_id"] = row[0]
        post["title"] = row[2]
        post["tags"] = row[3].split("\n")
        post["body"] = row[4]
        post["upvotes"] = row[5]
        post["time"] = row[6]
        posts["posts"].append(post)

    return posts
# {
#     "total_pages": <int>,
#     "posts": [
#         {
#             "post_id": <int>,
#             "title": <string:500>,
#             "tags": [
#                 <string:50> :10
#             ],
#             "body": <string>
#             "upvotes": <int>,
#             "time": <string:19>
#         } :$POSTS_PER_PAGE
#     ]
# }
# ----------------------------------------------

