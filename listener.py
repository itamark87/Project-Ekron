
from pymongo import MongoClient


def init(cluster):

    global db
    client = MongoClient(cluster)
    db = client["group_scraper_new"]


if __name__ == '__main__':

    with open('cluster.txt', 'r') as file:
        cluster = file.readline()

    init(cluster)

    for change in db.watch(full_document='updateLookup'):
        print(change)


