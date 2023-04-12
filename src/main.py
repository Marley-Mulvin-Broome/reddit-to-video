"""Main entry point for RedditToVideo"""

from configparser import ConfigParser
from argparse import ArgumentParser

from os import getcwd
from os import listdir as list_dir
from os import remove as remove_file
from os import makedirs as make_dir
from os.path import join as path_join
from os.path import isdir as is_dir

from sys import exit as exit_program

from reddit_to_video.reddit import Reddit
from reddit_to_video.video.config import VideoConfig
from reddit_to_video.handlers.posts import handle_video_post
from reddit_to_video.handlers.comment import handle_comment_post
from reddit_to_video.prompts import prompt_list
from reddit_to_video.video.tts import get_tts_engine
from reddit_to_video.exceptions import DirectoryNotFoundError


CONFIG_PATH = path_join(getcwd(), "user_configs/")
OUTPUT_PATH = "output/"
COMMENTS_PATH = path_join(getcwd(), "output/comments/")
POSTS_PATH = path_join(getcwd(), "output/posts/")


def load_config():
    """Loads the config file"""
    config = ConfigParser()
    try:
        config.read(path_join(getcwd(), "config.ini"))
    except FileNotFoundError:
        print(f"Config file not found in {getcwd()} directory. (config.ini)")
        exit_program(1)

    return config


def load_user_configs(dir_path):
    """Loads all user configs from a directory"""
    if not is_dir(dir_path):
        raise DirectoryNotFoundError(
            f"Config: Directory {dir_path} does not exist")

    configs = []
    for file_ in list_dir(dir_path):
        if file_.endswith(".json"):
            try:
                configs += VideoConfig.load_configs(path_join(dir_path, file_))
            except DirectoryNotFoundError as dir_error:
                print(f"{dir_error} (from {file_})")

    return configs


def create_user_agent(username, version):
    """Creates a user agent for the Reddit API"""
    return f"Python:RedditToVideo:v{version} (by /u/{username})"


def clear_cache():
    """Clears the cache of downloaded / generated videos, 
    screenshots, and audio from video creation"""
    for file_ in list_dir(COMMENTS_PATH):
        if file_.endswith(".png") or file_.endswith(".mp3"):
            remove_file(path_join(COMMENTS_PATH, file_))

    for file_ in list_dir(POSTS_PATH):
        if file_.endswith(".png") or file_.endswith(".mp3") or file_.endswith(".mp4"):
            remove_file(path_join(POSTS_PATH, file_))


def load_args():
    """Loads the arguments from the command line"""
    parser = ArgumentParser(
        description="Creates a video from top posts from a subreddit",
        add_help=False)

    system_args = parser.add_argument_group("Info Arguments")
    system_args.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this help message and exit_program")
    system_args.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="Show version and exit_program",
        required=False,
        default=False)
    system_args.add_argument(
        "-c",
        "--config",
        action="store_true",
        help="Show config and exit_program",
        required=False,
        default=False)
    system_args.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Sets the program to debug mode",
        required=False)
    system_args.add_argument(
        "-sv",
        "--system_voices",
        help="Shows the TTS voices on this system and exits",
        action="store_true",
        required=False,
        default=False)
    system_args.add_argument(
        "-cls",
        "--clear",
        help=("Clears the cached output files -"
              "this means ALL media will be generated from the next time this is run"),
        action="store_true",
        required=False,
        default=False)

    return parser.parse_args(), parser


def handle_system_args(parser, args, config, user_agent):
    """Handles the system arguments"""
    # Handles system args here
    if 'help' in args:
        parser.print_help()
        exit_program(0)
    if args.version:
        print(f"Version: {config['project']['version']}")
        exit_program(0)
    if args.config:
        print(
            f"""Config:
            [client_id:{config['reddit']['client_id']}]
            [client_secret:{config['reddit']['client_secret']}]
            [user_agent:{user_agent}]""")
        exit_program(0)
    if args.system_voices:
        print("System voices:")
        tts = get_tts_engine("s")
        voices = tts.get_voices()

        for voice in voices:
            print(voice)

        # print("Coqui voices:")
        # tts = get_tts_engine("c")
        # voices = tts.get_voices()

        # for voice in voices:
        #     print(voice)

        exit_program(0)
    if args.clear:
        print("Clearing cache...")
        clear_cache()
        print("Cache cleared!")


def check_ouput_dir():
    """Checks if the output directories exist, and creates them if they don't"""
    if not is_dir(OUTPUT_PATH):
        print(f"Creating output path @ {OUTPUT_PATH}")
        make_dir(OUTPUT_PATH)

    if not is_dir(POSTS_PATH):
        print(f"Creating posts path @ {POSTS_PATH}")
        make_dir(POSTS_PATH)

    if not is_dir(COMMENTS_PATH):
        print(f"Creating comments path @ {COMMENTS_PATH}")
        make_dir(COMMENTS_PATH)


def main():
    """Entry point for reddit to video"""
    config = load_config()
    args, parser = load_args()
    user_agent = create_user_agent(
        config["reddit"]["username"], config["project"]["version"])

    # debug = args.debug

    handle_system_args(parser, args, config, user_agent)

    check_ouput_dir()

    print("RedditToVideo v" + config["project"]["version"])

    if not is_dir(CONFIG_PATH):
        print(f"Creating user configs directory at {CONFIG_PATH}")
        make_dir(CONFIG_PATH)
        print("Please create a user config and try again!")
        exit_program(1)

    print("Loading video configs...")
    video_configs = load_user_configs(CONFIG_PATH)

    if len(video_configs) == 0:
        print(f"No video configs found in {CONFIG_PATH}")
        exit_program(1)

    chosen_config: VideoConfig = prompt_list(
        list(
            map(lambda config: (config.name, config), video_configs)),
        "Select a video config: ")

    reddit = Reddit(config["reddit"]["client_id"], config["reddit"]
                    ["client_secret"], user_agent, debug=False)

    if chosen_config.settings["type"].lower() == "comment":
        posts = reddit.get_top_posts(
            chosen_config.settings.subreddit, limit=10)

        chosen_post = prompt_list(
            list(map(lambda post: (post.title, post), posts)), "Select a post: ")

        handle_comment_post(chosen_post, chosen_config)

    elif chosen_config.settings["type"].lower() == "video":
        print("Loading top posts from Reddit...")
        posts = reddit.get_top_posts(
            chosen_config.settings.subreddit,
            limit=chosen_config.settings.limit,
            time_filter=chosen_config.settings.time)

        end_card_footage = None

        if chosen_config.has_setting("end_card_footage"):
            end_card_footage = chosen_config.settings["end_card_footage"]

        video_break_footage = None

        if chosen_config.has_setting("video_break_footage"):
            video_break_footage = chosen_config.settings["video_break_footage"]

        handle_video_post(
            posts,
            chosen_config,
            end_card_footage=end_card_footage,
            video_break_footage=video_break_footage,)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        exit_program(0)
