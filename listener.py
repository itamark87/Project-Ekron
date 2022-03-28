from pymongo import MongoClient
import random
from datetime import datetime
from rich import print
from predict import predict


# Initiate cluster and db
def init(cluster):

    global db
    client = MongoClient(cluster, connect=False)
    db = client["group_scraper_new"]


# Inspect text and return a label
def inspect(text):
    return predict(text)
    # return random.randint(0, 1)


# Initiate a MongoDB change stream, send string attributes to inspect
# If a post is found to be relevant, print the text, a link to the post and a link to the user
def listen():
    count = 0
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"[red]{dt_string} Listener initiated")
    for change in db.watch(full_document='updateLookup'):

        count += 1
        if change['operationType'] == 'insert':
            d = change['fullDocument']
        elif change['operationType'] == 'update':
            d = change['updateDescription']['updatedFields']
        else:
            continue
        if change['fullDocument']['post_id'] == '0' or change['fullDocument']['label'] == 1:
            continue
        d['operation'] = change['operationType']
        d['coll'] = change['ns']['coll']
        d['post_id'] = change['fullDocument']['post_id']
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"\n[red]{dt_string} Post {d['post_id']} in group {d['coll']} ({str(count)})[/]")
        labels = {}

        # Begin inspection of text variables
        if 'text' in d.keys() and d['text'] and inspect(d['text']):
            labels['text'] = d['text']
        if 'shared_text' in d.keys() and d['shared_text'] and inspect(d['shared_text']):
            labels['shared_text'] = d['shared_text']
        if 'images_description' in d.keys():
            images = {}
            for i in range(len(d['images_description'])):
                if d['images_description'][i] and inspect(d['images_description'][i]):
                    images[i] = d['images_description'][i]
            if images:
                labels['images'] = images

        # If any of the text attributes is classified as 1, print it, add links and add label in DB
        if labels:
            print("Post found to be relevant, here is why:\n")
            if 'text' in labels.keys() and labels['text']:
                print(f'* Post text:\n{labels["text"]}\n')
            if 'shared_text' in labels.keys() and labels['shared_text']:
                print(f'* Shared text:\n{labels["shared_text"]}\n')
            if 'images' in labels.keys() and labels['images']:
                print("* Images description:")
                for key, val in labels['images'].items():
                    print(f'{key}. {val}')

            group_id = str(db[d['coll']].find_one({'post_id': '0'})['group_id'])
            print(f"\nLink to post: https://www.facebook.com/groups/{group_id}/posts/{d['post_id']}/")
            print(f"Contact user: https://www.facebook.com/{str(change['fullDocument']['user_id'])}/")
            if 'shared_text' in labels.keys() and labels['shared_text']:
                print(f"Contact shared post user: https://www.facebook.com/{str(change['fullDocument']['shared_user_id'])}/")

            # db.d['coll'].update_one({'post_id': d['post_id']}, {"$set": {'label': "1"}})
        else:
            print("No relevant content found")
            # db.d['coll'].update_one({'post_id': d['post_id']}, {"$set": {'label': "0"}})


# #### Start Here #### #
# Initiate cluster and run listener
if __name__ == '__main__':

    with open('cluster.txt', 'r') as file:
        cluster = file.readline()

    init(cluster)

    listen()

