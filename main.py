from reddit import Reddit
from configparser import ConfigParser
from os import getcwd
from argparse import ArgumentParser
from os.path import join as path_join

default_output_dir = path_join(getcwd(), "output")
default_subreddit = "memes"
default_bg_dir = path_join(getcwd(), "bg_footage")

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

def load_args():
    parser = ArgumentParser(description="Creates a video from top posts from a subreddit", add_help=False)
    
    vid_args = parser.add_argument_group("Video Arguments")
    vid_args.add_argument("-t", "--type", help="Set type of content to create [comment|post]", type=str, required=True, default="top")
    vid_args.add_argument("-o", "--output",  help="Set output directory", type=str, required=False, default=default_output_dir)
    vid_args.add_argument("-s", "--subreddit", help="Set subreddit", type=str, required=False, default=default_subreddit)
    vid_args.add_argument("-bg", "--background", help="Set directory where the background footage is stored", type=str, required=False, default=default_bg_dir)

    system_args = parser.add_argument_group("System Arguments")
    system_args.add_argument("-h", "--help", action="help", help="Show this help message and exit")
    system_args.add_argument("-v", "--version", action="store_false", help="Show version", required=False)
    system_args.add_argument("-c", "--config", action="store_true", help="Show config", required=False)
    
    return parser.parse_args(), parser

def main():
    args, parser = load_args()
    config = load_config()
    user_agent = create_user_agent(config["reddit"]["username"], config["project"]["version"])
    # r = Reddit(config["reddit"]["client_id"], config["reddit"]["client_secret"], user_agent)
    
    print("%=============RedditToVideo=============%")

    # Handles system args here
    if args.help:
        parser.print_help()
        exit(0)

    if args.version:
        print(f"Version: {config['project']['version']}")
    if args.config:
        print(f"Config:\n[client_id:{config['reddit']['client_id']}]\n[client_secret:{config['reddit']['client_secret']}]\n[user_agent:{user_agent}]")

if __name__ == "__main__":
    main()