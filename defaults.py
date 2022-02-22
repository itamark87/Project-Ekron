
# Set this to be the number of posts scraped and known to the DB before scraping terminates
# For lower likelihood of missing new and relevant posts set a higher number
MAX_KNOWN_POSTS = 6

# Set this to be the general number of posts scraped before scraping terminates
# For lower risk of account ban set a lower number
MAX_NEW_POSTS = 60

# Number of seconds navigator waits before running next instance
# For lower risk of account ban set a higher number
BREAK_TIME = 60*2

# List of attributes that db_handler will update and save older values of.
# Post will not be considered as updated.
COMMON_SAVE = ['likes', 'shares']

# List of attributes that db_handler will update and will not save older values of.
# Post will not be considered as updated.
COMMON_NO_SAVE = ['link', 'links']

# List of attributes that db_handler will update, save older values of.
# Post will be considered as updated.
# If all attributes on that list, and only them, are updated, db_handler will not save older values and
# post will not be considered as updated.
COMMON_CHANGES_SHARE = ['text', 'shared_text']

# List of attributes that will not be inserted into the database by db_handler.
EXCLUSIONS = ['image_id', 'image', 'image_lowquality', 'images', 'images_lowquality', 'images_lowquality_description',
              'video', 'video_id', 'videos', 'available', 'post_url', 'user_url', 'shared_post_url', 'shared_time',
              'timestamp', 'with', 'comments', 'factcheck', 'listing_title', 'listing_price', 'listing_location']

POST_ATTRIBUTES = ['post_id', 'text', 'time', 'user_id', 'username', '']

# List of comment attributes that *will* be inserted into the database by db_handler
COMMENT_ATTRIBUTES = ['comment_id', 'commenter_id', 'commenter_name', 'comment_text']

# If only one cookies file is used
COOKIES = 'cookies.txt'
