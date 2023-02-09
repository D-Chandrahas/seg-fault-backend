import random
import string

with open ("names_wordlist.txt", "r") as f:
    names = f.read().splitlines()

names = random.sample(names, k=10000)

with open ("wordlist_small.txt", "r") as f:
    wordlist = f.read().splitlines()

with open ("tags_wordlist.txt", "r") as f:
    tagslist = f.read().splitlines()

with open("../database management/insert_users.sql", "w") as f:

    f.write("INSERT INTO users (username, password) VALUES\n")

    charset = string.ascii_lowercase + string.digits

    for i in range(9999):
        user_name = names[i]
        pass_len = random.randint(5, 10)
        password = ''.join(random.choice(charset) for _ in range(pass_len))
        f.write(f"('{user_name}', '{password}'),\n")
    
    user_name = names[9999]
    pass_len = random.randint(5, 10)
    password = ''.join(random.choice(charset) for _ in range(pass_len))
    f.write(f"('{user_name}', '{password}')")

total_posts = 0

with open("../database management/insert_posts.sql", "w") as f:

    f.write("INSERT INTO posts (user_id, title, tags, body, upvotes) VALUES\n")

    for i in range(10000):
        user_id = i + 1
        user_posts = random.randint(0, 10)
        for _ in range(user_posts):
            title_len = random.randint(5, 20)
            title = ' '.join(random.choice(wordlist) for _ in range(title_len))
            title = title[:500]
            tags_len = random.randint(1, 5)
            tags = "' || char(10) || '".join(random.choice(tagslist) for _ in range(tags_len))
            body_len = random.randint(20, 100)
            body = ' '.join(random.choice(wordlist) for _ in range(body_len))
            upvotes = random.randint(-3, 10)
            f.write(f"({user_id}, '{title}', '{tags}', '{body}', {upvotes}),\n")
            total_posts += 1
        
    user_id = 10000
    user_posts = random.randint(1, 10)
    for i in range(user_posts):
        title_len = random.randint(5, 20)
        title = ' '.join(random.choice(wordlist) for _ in range(title_len))
        title = title[:500]
        tags_len = random.randint(1, 5)
        tags = "' || char(10) || '".join(random.choice(tagslist) for _ in range(tags_len))
        body_len = random.randint(20, 100)
        body = ' '.join(random.choice(wordlist) for _ in range(body_len))
        upvotes = random.randint(-3, 10)
        if i == user_posts - 1:
            f.write(f"({user_id}, '{title}', '{tags}', '{body}', {upvotes})")
        else:
            f.write(f"({user_id}, '{title}', '{tags}', '{body}', {upvotes}),\n")
        total_posts += 1

with open("../database management/insert_replies.sql", "w") as f:

    f.write("INSERT INTO replies (post_id, user_id, body, upvotes) VALUES\n")

    for i in range(total_posts-1):
        post_id = i + 1
        post_replies = random.randint(0, 10)
        for _ in range(post_replies):
            user_id = random.randint(1, 10000)
            body_len = random.randint(20, 100)
            body = ' '.join(random.choice(wordlist) for _ in range(body_len))
            upvotes = random.randint(-3, 10)
            f.write(f"({post_id}, {user_id}, '{body}', {upvotes}),\n")
    
    post_id = total_posts
    post_replies = random.randint(1, 10)
    for i in range(post_replies):
        user_id = random.randint(1, 10000)
        body_len = random.randint(20, 100)
        body = ' '.join(random.choice(wordlist) for _ in range(body_len))
        upvotes = random.randint(-3, 10)
        if i == post_replies - 1:
            f.write(f"({post_id}, {user_id}, '{body}', {upvotes})")
        else:
            f.write(f"({post_id}, {user_id}, '{body}', {upvotes}),\n")

