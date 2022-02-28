from group_class import FacebookGroups
import defaults

import time


def run_instances():

    list_size = len(FacebookGroups.reg_list)
    i = 0
    while True:
        print("Run:", i+1, "\nGroup name:", FacebookGroups.reg_list[i].g_name)

        state = FacebookGroups.reg_list[i % list_size].scrape_group()
        if not state:
            print("Breaking after reaching max number of posts per batch. Scraping of next batch will begin in"
                  + str(defaults.BREAK_TIME/60/60) + "hrs")
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
                  + str(defaults.BAN_SLEEP/60/60) + "hrs")
            time.sleep(defaults.BAN_SLEEP)

        i += 1
        if i % list_size == 0:
            print("Breaking after covering all groups. Scraping of next batch will begin in"
                  + str(defaults.BREAK_TIME/60/60) + "hrs")
            FacebookGroups.batch_posts = 0
            time.sleep(defaults.BREAK_TIME)


if __name__ == '__main__':
    jackson_heights = FacebookGroups('Jackson Heights New', 35851988964)
    ilsington = FacebookGroups('Ilsington', 743308202528264)
    uppereast = FacebookGroups('Upper East Side', 'uppereastside35andolder')

    run_instances()





# Potential groups not yet approved:
    #astoria = FacebookGroups('Astoria', 2212914039)
    #florentin = FacebookGroups('Florentin Residents', 35950422406)

# Hebrew groups:
    # florentin_small = FacebookGroups('Florentin Residents Small', 166176720391064)
    # secret_tlv = FacebookGroups('Secret Tel Aviv', 327483250942)
    # yemen_vineyard = FacebookGroups('Yemenite Vineyard Residents', 560107510706998)
    # center_tlv = FacebookGroups('Center TLV Residents', 820474844639551)



