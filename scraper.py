from facebook_scraper import get_posts
from facebook_scraper import exceptions

import db_handler

import random
import time


def run(**kwargs):

    try:
        total_count = 0
        known_count = 0

        posts = get_posts(group=kwargs['g_id'], cookies=kwargs['g_cookies'], pages=10000, timeout=40,
                          options={"comments": False, 'posts_per_page': 14})

        for post in posts:

            # if post['comments_full']:
            #     comments = post['comments_full']
            #     for comment in comments:
            #         time.sleep(random.uniform(1.5, 3))
            #         if comment['replies']:
            #             replies = comment['replies']
            #             for reply in replies:
            #                 time.sleep(random.uniform(1.5, 3))

            print(post)
            time.sleep(random.uniform(10, 15))

            if db_handler.handle_post(post):
                known_count += 1
                print("\n" + str(known_count) + "\n")
            else:
                known_count = 0
            total_count += 1
            if known_count == kwargs['g_max_known']:
                print("Scraping of", kwargs['g_name'], "terminated after it's gone through",
                      kwargs['g_max_known'], "known posts")
                break
            if total_count == kwargs['g_max_new']:
                pass
                # print("Scraping of", kwargs['g_name'], "terminated after it's gone through",
                #       kwargs['g_max_new'], "posts")
                # break
                # time.sleep(random.uniform(60*1.5, 60*2.5))
                # total_count = 0
            #time.sleep(random.uniform(1.5, 3))
            if total_count%10 == 0:
                print(total_count)
        return 1

    except exceptions.TemporarilyBanned:
        print("Temporarily banned, sleeping for 24h")
        time.sleep(60*60*12)
        return 1


def scrape(**kwargs):
    with open('cluster.txt', 'r') as file:
        cluster = file.readline()
    db_handler.init(cluster, kwargs['g_name'])
    return run(**kwargs)



