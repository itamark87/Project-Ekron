import defaults

from scraper import scrape


class FacebookGroups:

    reg_list = []

    def __init__(self, group_name, group_id, cookies=defaults.COOKIES,
                 max_known=defaults.MAX_KNOWN_POSTS, max_new=defaults.MAX_NEW_POSTS):
        self.g_name = group_name
        self.g_id = group_id
        self.g_cookies = cookies
        self.g_max_known = max_known
        self.g_max_new = max_new
        self.g_runs = 0
        self._registry.append(self)

    def scrape_group(self):
        kwargs = self.__dict__
        return scrape(**kwargs)















