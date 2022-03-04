from group_class import FacebookGroups
from scraper import scrape
import defaults
import time
import random


# Running instances, the main functions determines which group will be scraped and when
# When a group scraping terminates, main will decide what happens next, depending on the cause
def main():

    list_size = len(FacebookGroups.reg_list)
    i = 0
    while True:
        print("Run:", i+1, "\nGroup name:", FacebookGroups.reg_list[i % list_size].g_name)
        kwargs = FacebookGroups.reg_list[i % list_size].__dict__
        state = scrape(**kwargs)
        if not state:
            print("Breaking after reaching max number of posts per batch. Scraping of next batch will begin in"
                  + str(defaults.BREAK_TIME/60/60) + " hrs")
            FacebookGroups.batch_posts = 0
            time.sleep(defaults.BREAK_TIME)
            continue
        elif state == 1:
            print("Scraping of", FacebookGroups.reg_list[i % list_size].g_name,
                  "terminated after it's gone through",
                  FacebookGroups.reg_list[i % len(FacebookGroups.reg_list)].g_max_known, "known posts\n")
            time.sleep(random.uniform(30, 60))
        elif state == 2:
            print("Temporarily banned by Facebook. Scraping of next batch will begin in"
                  + str(defaults.BAN_SLEEP/60/60) + " hrs")
            time.sleep(defaults.BAN_SLEEP)

        i += 1
        if i % list_size == 0:
            print("Breaking after covering all groups. Scraping of next batch will begin in"
                  + str(defaults.BREAK_TIME/60/60) + " hrs")
            FacebookGroups.batch_posts = 0
            time.sleep(defaults.BREAK_TIME)


# #### START HERE ##### #
# Add group instances, mandatory attributes are group name and group id
# Unless specified, all other attributes will be set as configured at defaults.py
if __name__ == '__main__':
    jackson_heights = FacebookGroups('Jackson Heights New', 35851988964)
    ilsington = FacebookGroups('Ilsington', 743308202528264)
    uppereast = FacebookGroups('Upper East Side', 'uppereastside35andolder')

    main()





