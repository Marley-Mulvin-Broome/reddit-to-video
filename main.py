from reddit import Reddit
from configparser import ConfigParser
from os import getcwd

def load_config():
    config = ConfigParser()
    try:
        config.read("config.ini")
    except FileNotFoundError:
        print(f"Config file not found in {getcwd()} directory. (config.ini)")
        exit(1)

    return config

def create_user_agent(username, version):
    return f"Python:RedditToVideo:v{version} (by /u/{username})"

def main():
    config = load_config()
    user_agent = create_user_agent(config["reddit"]["username"], config["project"]["version"])
    r = Reddit(config["reddit"]["client_id"], config["reddit"]["client_secret"], user_agent)
    
    for submission in r.subreddit("python"):
        print(submission.title)

if __name__ == "__main__":
    main()