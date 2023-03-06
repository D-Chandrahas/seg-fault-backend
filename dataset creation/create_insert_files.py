import random
import string
from randomtimestamp import randomtimestamp

# ! run from script directory only


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

with open("../database management/insert_posts.sql", "w") as f, open("../database management/insert_post_votes.sql", "w") as f2:

    f.write("INSERT INTO posts (user_id, title, tags, body, upvotes, time) VALUES\n")
    f2.write("INSERT INTO post_votes VALUES\n")

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
            time = randomtimestamp(start_year = 2000, pattern = "%Y-%m-%d %H:%M:%S", text=True)
            f.write(f"({user_id}, '{title}', char(10) || '{tags}' || char(10), '{body}', {upvotes}, '{time}'),\n")
            total_posts += 1
            if upvotes != 0:
                vote_char = "'u'" if upvotes > 0 else "'d'"
                vote_user_ids = random.sample(range(1,10001), k = abs(upvotes) + 2 * random.randint(0, abs(upvotes)))
                for vote_user_id in vote_user_ids[:abs(upvotes)]:
                    f2.write(f"({total_posts}, {vote_user_id}, {vote_char}),\n")
                for vote_user_id1, vote_user_id2 in zip(vote_user_ids[abs(upvotes) : abs(upvotes) + ((len(vote_user_ids) - abs(upvotes))//2)], vote_user_ids[abs(upvotes) + ((len(vote_user_ids) - abs(upvotes))//2):]):
                    f2.write(f"({total_posts}, {vote_user_id1}, 'u'),\n")
                    f2.write(f"({total_posts}, {vote_user_id2}, 'd'),\n")
            else:
                vote_user_ids = random.sample(range(1,10001), k = 2 * random.randint(0, 5))
                for vote_user_id1, vote_user_id2 in zip(vote_user_ids[:len(vote_user_ids)//2], vote_user_ids[len(vote_user_ids)//2:]):
                    f2.write(f"({total_posts}, {vote_user_id1}, 'u'),\n")
                    f2.write(f"({total_posts}, {vote_user_id2}, 'd'),\n")

    user_id = 10000
    user_posts = 1
    title_len = random.randint(5, 20)
    title = ' '.join(random.choice(wordlist) for _ in range(title_len))
    title = title[:500]
    tags_len = random.randint(1, 5)
    tags = "' || char(10) || '".join(random.choice(tagslist) for _ in range(tags_len))
    body_len = random.randint(20, 100)
    body = ' '.join(random.choice(wordlist) for _ in range(body_len))
    upvotes = 1
    time = randomtimestamp(start_year = 2000, pattern = "%Y-%m-%d %H:%M:%S", text=True)
    f.write(f"({user_id}, '{title}', char(10) || '{tags}' || char(10), '{body}', {upvotes}, '{time}')")
    total_posts += 1
    f2.write(f"({total_posts}, {random.randint(1,10000)}, 'u')")

total_replies = 0

with open("../database management/insert_replies.sql", "w") as f, open("../database management/insert_reply_votes.sql", "w") as f2:

    f.write("INSERT INTO replies (post_id, user_id, body, upvotes, time) VALUES\n")
    f2.write("INSERT INTO reply_votes VALUES\n")

    for i in range(total_posts-1):
        post_id = i + 1
        post_replies = random.randint(0, 10)
        for _ in range(post_replies):
            user_id = random.randint(1, 10000)
            body_len = random.randint(20, 100)
            body = ' '.join(random.choice(wordlist) for _ in range(body_len))
            upvotes = random.randint(-3, 10)
            time = randomtimestamp(start_year = 2000, pattern = "%Y-%m-%d %H:%M:%S", text=True)
            f.write(f"({post_id}, {user_id}, '{body}', {upvotes}, '{time}'),\n")
            total_replies += 1
            if upvotes != 0:
                vote_char = "'u'" if upvotes > 0 else "'d'"
                vote_user_ids = random.sample(range(1,10001), k = abs(upvotes) + 2 * random.randint(0, abs(upvotes)))
                for vote_user_id in vote_user_ids[:abs(upvotes)]:
                    f2.write(f"({total_replies}, {vote_user_id}, {vote_char}),\n")
                for vote_user_id1, vote_user_id2 in zip(vote_user_ids[abs(upvotes) : abs(upvotes) + ((len(vote_user_ids) - abs(upvotes))//2)], vote_user_ids[abs(upvotes) + ((len(vote_user_ids) - abs(upvotes))//2):]):
                    f2.write(f"({total_replies}, {vote_user_id1}, 'u'),\n")
                    f2.write(f"({total_replies}, {vote_user_id2}, 'd'),\n")
            else:
                vote_user_ids = random.sample(range(1,10001), k = 2 * random.randint(0, 5))
                for vote_user_id1, vote_user_id2 in zip(vote_user_ids[:len(vote_user_ids)//2], vote_user_ids[len(vote_user_ids)//2:]):
                    f2.write(f"({total_replies}, {vote_user_id1}, 'u'),\n")
                    f2.write(f"({total_replies}, {vote_user_id2}, 'd'),\n")
    
    post_id = total_posts
    post_replies = 1
    user_id = random.randint(1, 10000)
    body_len = random.randint(20, 100)
    body = ' '.join(random.choice(wordlist) for _ in range(body_len))
    upvotes = 1
    time = randomtimestamp(start_year = 2000, pattern = "%Y-%m-%d %H:%M:%S", text=True)
    f.write(f"({post_id}, {user_id}, '{body}', {upvotes}, '{time}')")
    total_replies += 1
    f2.write(f"({total_replies}, {random.randint(1,10000)}, 'u')")


