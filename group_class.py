import defaults


class FacebookGroups:

    reg_list = []
    batch_posts = 0

    def __init__(self, group_name, group_id, cookies=defaults.COOKIES,
                 max_known=defaults.MAX_KNOWN_POSTS, max_new=defaults.MAX_NEW_POSTS, comments=defaults.COMMENTS):
        self.g_name = group_name
        self.g_id = group_id
        self.g_cookies = cookies
        self.g_max_known = max_known
        self.g_max_new = max_new
        self.comments = comments
        FacebookGroups.reg_list.append(self)

    @classmethod
    def get_id(cls, name):
        for group in cls.reg_list:
            if group.g_name == name:
                return group.g_id
        return 0















