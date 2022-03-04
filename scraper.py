from facebook_scraper import get_posts
from facebook_scraper import exceptions
from group_class import FacebookGroups
import defaults
import db_handler
import random
import time


# Run scraper and pass all posts to db_handler
def run(**kwargs):

    try:

        posts = get_posts(group=kwargs['g_id'], cookies=kwargs['g_cookies'], pages=10000, timeout=40,
                          options={"comments": kwargs['comments'], 'posts_per_page': 14})

        known_count = 0
        for post in posts:

            if kwargs['comments']:
                if post['comments_full']:
                    comments = post['comments_full']
                    for comment in comments:
                        time.sleep(random.uniform(1.5, 3))
                        if comment['replies']:
                            replies = comment['replies']
                            for reply in replies:
                                time.sleep(random.uniform(1.5, 3))

            print(post)

            FacebookGroups.batch_posts += 1
            if FacebookGroups.batch_posts == defaults.MAX_NEW_POSTS:
                db_handler.handle_post(post)
                return 0

            if db_handler.handle_post(post):
                known_count += 1
                print(f"Post known to database - {str(known_count)}# occurrence in a row")
                if known_count == kwargs['g_max_known']:
                    return 1
            else:
                known_count = 0

            time.sleep(random.uniform(20, 30))

    except exceptions.TemporarilyBanned:
        return 2


# Initiate a MongoDB cluster and run scraper
def scrape(**kwargs):
    with open('cluster.txt', 'r') as file:
        cluster = file.readline()
    db_handler.init(cluster, kwargs['g_name'], kwargs['g_id'])
    return run(**kwargs)



