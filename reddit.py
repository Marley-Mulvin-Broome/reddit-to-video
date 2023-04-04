import praw

class Reddit:
    def __init__(self, client_id, client_secret, user_agent):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent

        self._reddit = praw.Reddit(client_id=self.client_id,
                            client_secret=self.client_secret,
                            user_agent=self.user_agent)
        
    def __repr__(self):
        return f"Reddit({self.client_id}, {self.client_secret}, {self.user_agent})"
    
    @property
    def user(self):
        return self._reddit.user.me()
    
    @property
    def reddit(self):
        return self._reddit
    
    def subreddit(self, subreddit):
        return self._reddit.subreddit(subreddit).hot(limit=10)
