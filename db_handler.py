from pymongo import MongoClient
from datetime import datetime
import config


# Initiate cluster, db and collection
def init(cluster, g_name, g_id):

    global collection
    client = MongoClient(cluster)
    db = client["group_scraper_new"]
    collection = db[g_name]

    group_dict = collection.find_one({'post_id': "0"})
    if not group_dict:
        collection.insert_one({'post_id': "0", 'group_id': str(g_id)})


# When scarping with comments, remove unneeded attributes
def comments_cleanup(comments):

    new_comments = []

    for comment in comments:

        new_comment = {}
        for key in comment:
            if key in config.COMMENT_ATTRIBUTES:
                new_comment[key] = comment[key]
                continue
            if key == "replies" and comment['replies']:
                new_comment['replies'] = comments_cleanup(comment['replies'])
        new_comments.append(new_comment)

    return new_comments


# If post is known to the DB, update it and save older information in an array
def post_known(scraped_post, db_post, older_list, update_time):

    changed = {}

    for key, val in scraped_post.items():
        if key not in db_post:
            if val and key in config.POST_ATTRIBUTES:
                changed[key] = ''
                collection.update_one({'post_id': scraped_post['post_id']}, {"$set": {key: val}})
            continue
        if str(db_post[key]) != str(val):
            if val:
                collection.update_one({'post_id': scraped_post['post_id']}, {"$set": {key: val}})
            else:
                collection.update_one({'post_id': scraped_post['post_id']}, {"$unset": {key: 1}})

            changed[key] = db_post[key]

    collection.update_one({'post_id': scraped_post['post_id']}, {"$set": {'update_time': datetime.now()}})

    if changed:
        changed['update_time'] = update_time
        older_list.append(changed)
        collection.update_one({'post_id': scraped_post['post_id']}, {"$set": {'older': older_list}})
        changed.pop("update_time")

    return 1


# If post is unknown to the DB, insert the post with the desirable attributes
def insert_post(post):

    inserted_post = {}

    for key, val in post.items():
        if val and key in config.POST_ATTRIBUTES:
            inserted_post[key] = val

    inserted_post['label'] = "Not Yet Reviewed"
    inserted_post['update_time'] = datetime.now()
    collection.insert_one(inserted_post)
    return 0


# Main function of db_handler
# Receives the scraped post and checks if it is a known post to DB
def handle_post(scraped_post):

    if not scraped_post['post_id']:
        return 0

    if scraped_post['comments_full']:
        scraped_post['comments_full'] = comments_cleanup(scraped_post['comments_full'])

    db_post = collection.find_one({'post_id': scraped_post['post_id']})

    if db_post:
        difference = (datetime.now() - db_post['update_time'])
        if difference.total_seconds() < 60:
            return 0
        del db_post['_id']
        older_list = db_post.pop('older', [])
        update_time = db_post.pop('update_time')
        return post_known(scraped_post, db_post, older_list, update_time)

    return insert_post(scraped_post)
