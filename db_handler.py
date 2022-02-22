from pymongo import MongoClient
from datetime import datetime

import defaults


def init(cluster, g_name):

    global collection
    client = MongoClient(cluster)
    db = client["group_scraper"]
    collection = db[g_name]


def comments_cleanup(comments):

    new_comments = []

    for comment in comments:

        new_comment = {}
        for key in comment:
            if key in defaults.COMMENT_ATTRIBUTES:
                new_comment[key] = comment[key]
                continue
            if key == "replies" and comment['replies']:
                new_comment['replies'] = comments_cleanup(comment['replies'])
        new_comments.append(new_comment)

    return new_comments


def is_shared_related(scraped_post, db_post):

    for key in defaults.COMMON_CHANGES_SHARE:
        if key not in scraped_post or key not in db_post:
            return 0
        if scraped_post[key] == db_post[key]:
            return 0

    return 1


def post_known(scraped_post, db_post, older_list, update_time):

    changed = {}
    shared_related = is_shared_related(scraped_post, db_post)

    for key, val in scraped_post.items():
        if key not in db_post:
            if val and key not in defaults.EXCLUSIONS:
                changed[key] = ''
                collection.update_one({'post_id': scraped_post['post_id']}, {"$set": {key: val}})
            continue
        if str(db_post[key]) != str(val):
            if val:
                collection.update_one({'post_id': scraped_post['post_id']}, {"$set": {key: val}})
            else:
                collection.update_one({'post_id': scraped_post['post_id']}, {"$unset": {key: 1}})

            if key not in defaults.COMMON_NO_SAVE:
                if not shared_related or key not in defaults.COMMON_CHANGES_SHARE:
                    changed[key] = db_post[key]

    collection.update_one({'post_id': scraped_post['post_id']}, {"$set": {'update_time': datetime.now()}})

    if changed:
        changed['update_time'] = update_time
        older_list.append(changed)
        collection.update_one({'post_id': scraped_post['post_id']}, {"$set": {'older': older_list}})
        changed.pop("update_time")
        if not all(elem in defaults.COMMON_SAVE for elem in list(changed)):
            return 0

    return 1


def insert_post(post):

    inserted_post = {}

    for key, val in post.items():
        if val and key not in defaults.EXCLUSIONS:
            inserted_post[key] = val

    inserted_post['label'] = "Not Yet Reviewed"
    inserted_post['update_time'] = datetime.now()
    collection.insert_one(inserted_post)
    return 0


def handle_post(scraped_post):

    if scraped_post['comments_full']:
        scraped_post['comments_full'] = comments_cleanup(scraped_post['comments_full'])

    db_post = collection.find_one({'post_id': scraped_post['post_id']})

    if db_post:
        # difference = (datetime.now() - db_post['update_time'])
        # if difference.total_seconds() < 60:
        #     return 0
        # del db_post['_id']
        # older_list = db_post.pop('older', [])
        # update_time = db_post.pop('update_time')
        # return post_known(scraped_post, db_post, older_list, update_time)
        ##### Delete later #####
        return 1
        ########################

    return insert_post(scraped_post)