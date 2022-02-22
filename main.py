from group_class import FacebookGroups
import defaults

import time


def run_instances():

    list_size = len(FacebookGroups.reg_list)
    i = 0
    while True:
        print("Run:", i+1, "\nGroup name:", FacebookGroups.reg_list[i % list_size].g_name)
        if not FacebookGroups.reg_list[i % list_size].scrape_group():
            continue
        FacebookGroups.reg_list[i % list_size].g_runs += 1
        i += 1
        if i == 1:
            exit()
        print("Breaking for " + str(defaults.BREAK_TIME) + "s before moving on to next group")
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



