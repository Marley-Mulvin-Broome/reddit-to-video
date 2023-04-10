import praw
import logging


class Reddit:
    def __init__(self, client_id, client_secret, user_agent, debug=False):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.debug = debug

        if self.debug:
            self._loadLogger()

        self._reddit = praw.Reddit(client_id=self.client_id,
                                   client_secret=self.client_secret,
                                   user_agent=self.user_agent)

    def __repr__(self):
        return f"Reddit({self.client_id}, {self.client_secret}, {self.user_agent})"

    def _load_logger(self):
        handler = logging.StreamHandler()
        logging.basicConfig(level=logging.DEBUG)

        for logger_name in ("praw", "prawcore"):
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(handler)

    def get_top_posts(self, subreddit, time_filter="all", limit=10):
        return self._reddit.subreddit(subreddit).top(time_filter=time_filter, limit=limit)

    def get_hot_posts(self, subreddit, limit=10):
        return self._reddit.subreddit(subreddit).hot(limit=limit)

    @property
    def user(self):
        return self._reddit.user.me()

    @property
    def reddit(self):
        return self._reddit
