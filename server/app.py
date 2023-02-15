from flask import Flask, request, Response
import sqlite3
import math


app = Flask(__name__)

con = sqlite3.connect("../database/cqadb.sqlite",check_same_thread=False)
con.execute("PRAGMA foreign_keys = ON")
cur = con.cursor()

with open("../database/tags.txt",'r') as f:
    all_tags = f.read().splitlines()

# * /login?username=<string:250>&password=<string:250>
@app.route("/login",methods=["GET"])
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    if username is None or password is None:
        return Response(status=400)
    res = cur.execute("SELECT * FROM users WHERE username = ? AND password = ?",(username,password))
    row = res.fetchone()
    if row is None:
        return {"auth_status":False, "user_id":None}
    else:
        return {"auth_status":True, "user_id":row[0]}
# {
#     "auth_status": <bool>
#     "user_id": <int/null>
# }
# * ----------------------------------------------

# * /register?username=<string:250>&password=<string:250>
@app.route("/register",methods=["POST"])
def register():
    username = request.args.get("username")
    password = request.args.get("password")
    if username is None or password is None:
        return Response(status=400)
    res = cur.execute("SELECT * FROM users WHERE username = ?",(username,))
    if res.fetchone() is None:
        cur.execute("INSERT INTO users(username,password) VALUES (?,?)",(username,password))
        con.commit()
        return {"register_status":True}
    else:
        return {"register_status":False}
# {
#     "register_status": <bool>
# }
# * ----------------------------------------------

# * /post/upvote?post_id=<int>
@app.route("/post/upvote",methods=["POST"])
def upvote_post():
    post_id = request.args.get("post_id",type=int)
    if post_id is None:
        return Response(status=400)
    cur.execute("UPDATE posts SET upvotes = upvotes + 1 WHERE post_id = ?",(post_id,))
    con.commit()
    return Response(status=202)
# no response body
# * ----------------------------------------------

# * /post/downvote?post_id=<int>
@app.route("/post/downvote",methods=["POST"])
def downvote_post():
    post_id = request.args.get("post_id",type=int)
    if post_id is None:
        return Response(status=400)
    cur.execute("UPDATE posts SET upvotes = upvotes - 1 WHERE post_id = ?",(post_id,))
    con.commit()
    return Response(status=202)
# no response body
# * ----------------------------------------------

# * /reply/upvote?reply_id=<int>
@app.route("/reply/upvote",methods=["POST"])
def upvote_reply():
    reply_id = request.args.get("reply_id",type=int)
    if reply_id is None:
        return Response(status=400)
    cur.execute("UPDATE replies SET upvotes = upvotes + 1 WHERE reply_id = ?",(reply_id,))
    con.commit()
    return Response(status=202)
# no response body
# * ----------------------------------------------

# * /reply/downvote?reply_id=<int>
@app.route("/reply/downvote",methods=["POST"])
def downvote_reply():
    reply_id = request.args.get("reply_id",type=int)
    if reply_id is None:
        return Response(status=400)
    cur.execute("UPDATE replies SET upvotes = upvotes - 1 WHERE reply_id = ?",(reply_id,))
    con.commit()
    return Response(status=202)
# no response body
# * ----------------------------------------------

# * /post/create
# {
#     "user_id": <int>,
#     "title": <string:500>,
#     "tags": [
#         <string:30> :10
#     ],
#     "body": <string>
# }
@app.route("/post/create",methods=["POST"])
def create_post():
    if request.json is None:
        return Response(status=400)
    user_id = request.json.get("user_id")
    title = request.json.get("title")
    if request.json.get("tags") is None:
        tags = []
    else:
        tags = request.json.get("tags")
    for i,tag in enumerate(tags):
        if tag not in all_tags:
            tags.pop(i)
    tags = "\n".join(tags)
    body = request.json.get("body")
    if user_id is None or title is None or body is None:
        return Response(status=400)
    cur.execute("INSERT INTO posts(user_id,title,tags,body) VALUES (?,?,?,?)",(user_id,title,tags,body))
    con.commit()
    return Response(status=202)
# no response body
# * ----------------------------------------------

# * /post/edit
# {
#     "post_id": <int>,
#     "title": <string:500>,
#     "tags":[
#         <string:30> :10
#     ],
#     "body": <string>
# }
@app.route("/post/edit",methods=["POST"])
def edit_post():
    if request.json is None:
        return Response(status=400)
    post_id = request.json.get("post_id")
    title = request.json.get("title")
    if request.json.get("tags") is None:
        tags = []
    else:
        tags = request.json.get("tags")
    for i,tag in enumerate(tags):
        if tag not in all_tags:
            tags.pop(i)
    tags = "\n".join(tags)
    body = request.json.get("body")
    if post_id is None or title is None or body is None:
        return Response(status=400)
    cur.execute("UPDATE posts SET title = ?, tags = ?, body = ? WHERE post_id = ?",(title,tags,body,post_id))
    con.commit()
    return Response(status=202)
# no response body
# * ----------------------------------------------

# * /post/delete?post_id=<int>
@app.route("/post/delete",methods=["POST"])
def delete_post():
    post_id = request.args.get("post_id",type=int)
    if post_id is None:
        return Response(status=400)
    cur.execute("DELETE FROM replies WHERE post_id = ?",(post_id,))
    cur.execute("DELETE FROM posts WHERE post_id = ?",(post_id,))
    con.commit()
    return Response(status=202)
# no response body
# * ----------------------------------------------

# * /reply/create
# {
#     "post_id": <int>,
#     "user_id": <int>,
#     "body": <string>,
# }
@app.route("/reply/create",methods=["POST"])
def create_reply():
    if request.json is None:
        return Response(status=400)
    post_id = request.json.get("post_id")
    user_id = request.json.get("user_id")
    body = request.json.get("body")
    if post_id is None or user_id is None or body is None:
        return Response(status=400)
    cur.execute("INSERT INTO replies(post_id,user_id,body) VALUES (?,?,?)",(post_id,user_id,body))
    con.commit()
    return Response(status=202)
# no response body
# * ----------------------------------------------

# * /reply/edit
# {
#     "reply_id": <int>,
#     "body": <string>,
# }
@app.route("/reply/edit",methods=["POST"])
def edit_reply():
    if request.json is None:
        return Response(status=400)
    reply_id = request.json.get("reply_id")
    body = request.json.get("body")
    if reply_id is None or body is None:
        return Response(status=400)
    cur.execute("UPDATE replies SET body = ? WHERE reply_id = ?",(body,reply_id))
    con.commit()
    return Response(status=202)
# no response body
# * ----------------------------------------------

# * /reply/delete?reply_id=<int>
@app.route("/reply/delete",methods=["POST"])
def delete_reply():
    reply_id = request.args.get("reply_id",type=int)
    if reply_id is None:
        return Response(status=400)
    cur.execute("DELETE FROM replies WHERE reply_id = ?",(reply_id,))
    con.commit()
    return Response(status=202)
# no response body
# * ----------------------------------------------

# * /user/posts?user_id=<int>&page=<int>&order_by=<string:[time_asc, time_desc, votes_asc, votes_desc]>
@app.route("/user/posts",methods=["GET"])
def get_user_posts():
    POSTS_PER_PAGE = 15
    user_id = request.args.get("user_id",type=int)
    order_by = request.args.get("order_by",type=str)
    page = request.args.get("page",type=int)
    if user_id is None or order_by is None or page is None:
        return Response(status=400)
    if page < 1:
        return Response(status=400)
    if order_by == "time_asc": order_by = "time ASC"
    elif order_by == "time_desc": order_by = "time DESC"
    elif order_by == "votes_asc": order_by = "upvotes ASC"
    elif order_by == "votes_desc": order_by = "upvotes DESC"
    else: return Response(status=400)
    posts = {}
    res = cur.execute("SELECT COUNT(*) FROM posts WHERE user_id = ?",(user_id,))
    posts["total_pages"] = math.ceil(res.fetchone()[0]/POSTS_PER_PAGE)
    posts["posts"] = []
    if posts["total_pages"] == 0:
        return posts
    if page > posts["total_pages"]:
        return Response(status=400)
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
#                 <string:30> :10
#             ],
#             "body": <string>
#             "upvotes": <int>,
#             "time": <string:19>
#         } :$POSTS_PER_PAGE
#     ]
# }
# * ----------------------------------------------

# * /search/user?username=<string:250>&page=<int>
@app.route("/search/user",methods=["GET"])
def search_user():
    USERNAMES_PER_PAGE = 15
    username = request.args.get("username")
    page = request.args.get("page",type=int)
    if username is None or page is None:
        return Response(status=400)
    if page < 1:
        return Response(status=400)
    username = username.strip().replace(" ","%")
    usernames = {}
    res = cur.execute("SELECT COUNT(*) FROM users WHERE username LIKE ?",("%"+username+"%",))
    usernames["total_pages"] = math.ceil(res.fetchone()[0]/USERNAMES_PER_PAGE)
    usernames["usernames"] = []
    if usernames["total_pages"] == 0:
        return usernames
    if page > usernames["total_pages"]:
        return Response(status=400)
    res = cur.execute("SELECT username FROM users WHERE username LIKE ? LIMIT ? OFFSET ?",("%"+username+"%", USERNAMES_PER_PAGE,(page-1)*USERNAMES_PER_PAGE))
    for row in res:
        usernames["usernames"].append(row[0])
    return usernames
# {
#     "total_pages": <int>,
#     "usernames": [
#         <string:250> :$USERNAMES_PER_PAGE
#     ]
# }
# * ----------------------------------------------

# * /search/tags
# {
#     "tags": [
#         <string:30> :1674
#     ]
#     "page": <int>,
#     "order_by": <string:[time_asc, time_desc, votes_asc, votes_desc]>
# }
@app.route("/search/tags",methods=["GET"])
def search_tags():
    pass



# * /all_tags
@app.route("/all_tags",methods=["GET"])
def get_all_tags():
    return {"all_tags": all_tags}
# {
#     "all_tags": [
#         <string:30> :1674
#     ]
# }
# * ----------------------------------------------
