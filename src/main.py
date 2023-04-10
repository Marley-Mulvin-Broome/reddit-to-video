from reddit import Reddit
from configparser import ConfigParser
from os import getcwd
from argparse import ArgumentParser
from os.path import join as path_join
from os.path import isdir as is_dir
from os.path import isfile as is_file
from os import listdir as list_dir
from os import remove as remove_file
from traceback import print_exc
from post import Post
from proglog import default_bar_logger
from video.vidConfig import VideoConfig
from os import makedirs as make_dir

from tts import get_tts_engine

from prompts import prompt_list, prompt_list, prompt_bool, prompt_write_file

from video.videoScript import VideoScript
from video.scriptElement import ScriptElement
from video.compose import composeVideo

from exceptions import CommentTooBigError

import time

import logging
logging.basicConfig(level=logging.WARNING)


CONFIG_PATH = path_join(getcwd(), "user_configs/")
OUTPUT_PATH = "output/"
COMMENTS_PATH = path_join(getcwd(), "output/comments/")
POSTS_PATH = path_join(getcwd(), "output/posts/")


def load_config():
    config = ConfigParser()
    try:
        config.read("config.ini")
    except FileNotFoundError:
        print(f"Config file not found in {getcwd()} directory. (config.ini)")
        exit(1)

    return config


def load_user_configs(dir_path):
    if not is_dir(dir_path):
        raise Exception(f"Config: Directory {dir_path} does not exist")

    configs = []
    for file_ in list_dir(dir_path):
        if file_.endswith(".json"):
            configs += VideoConfig.load_configs(path_join(dir_path, file_))

    return configs


def create_user_agent(username, version):
    return f"Python:RedditToVideo:v{version} (by /u/{username})"


def clear_cache():
    for file_ in list_dir(COMMENTS_PATH):
        if file_.endswith(".png") or file_.endswith(".mp3"):
            remove_file(path_join(COMMENTS_PATH, file_))

    for file_ in list_dir(POSTS_PATH):
        if file_.endswith(".png") or file_.endswith(".mp3"):
            remove_file(path_join(POSTS_PATH, file_))


def load_args():
    parser = ArgumentParser(
        description="Creates a video from top posts from a subreddit", add_help=False)

    system_args = parser.add_argument_group("Info Arguments")
    system_args.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit")
    system_args.add_argument(
        "-v", "--version", action="store_true", help="Show version and exit", required=False, default=False)
    system_args.add_argument(
        "-c", "--config", action="store_true", help="Show config and exit", required=False, default=False)
    system_args.add_argument("-d", "--debug", action="store_true",
                             help="Sets the program to debug mode", required=False)
    system_args.add_argument("-sv", "--system_voices", help="Shows the TTS voices on this system and exits",
                             action="store_true", required=False, default=False)
    system_args.add_argument(
        "-cls", "--clear", help="Clears the cached output files - this means ALL media will be generated from the next time this is run", action="store_true", required=False, default=False)

    return parser.parse_args(), parser


def prompt_file_name():
    print("Enter a file name for output (no extension): ", end="")
    return input()


def handle_comment_post(selected_post, config: VideoConfig):
    tts = get_tts_engine(config.tts.engine, **config.tts.kwargs)

    print(f"Loaded {repr(tts)} TTS engine")

    comments = []

    print(f"Loaded post: '{selected_post.title}' media")

    post = Post(selected_post.url, selected_post.id, not selected_post.is_self)

    post_screenshot_out = f"output/posts/post - {selected_post.id}.png"
    post_audio_out = f"output/posts/post - {selected_post.id}.mp3"

    max_failures = 3

    try:
        post.screenshot_title(post_screenshot_out)
    except Exception as e:
        print("Failed to screenshot post title, is it new reddit layout?")
        print("Tryting again...")

        max_failures -= 1

        if max_failures == 0:
            print("Failed to screenshot post title")
            exit(1)

        post.reload()

    if not is_file(post_audio_out):
        tts.save_audio(selected_post.title, post_audio_out)

    selected_post.comments.replace_more(limit=0)

    for i, comment in enumerate(selected_post.comments):
        if i > config.settings.limit:
            break

        audio_out = f"output/comments/comment - {comment.id}.mp3"
        screenshot_out = f"output/comments/comment - {comment.id}.png"

        comments.append((comment.body, screenshot_out, audio_out))

        # sometimes we might have these in cache already
        if not is_file(audio_out):
            tts.save_audio(
                comment.body, audio_out)
        if not is_file(screenshot_out):
            post.screenshot_comment(
                comment.id, f"output/comments/")

    post.close()

    print("Finished loading comments media")

    # r.create_comment_video(posts[post_num], args.output, args.background)

    if repr(tts) == "SystemTTS":
        print("Running system TTS engine")
        tts.run()
        print("Finished running system TTS engine")

    print("Creating video script...")
    # create video script
    script = VideoScript(int(config.settings.max_length),
                         int(config.settings.min_length))

    # add post title
    post_title_element = ScriptElement(
        selected_post.title, post_screenshot_out, post_audio_out)

    try:
        script.add_script_element(post_title_element)
    except CommentTooBigError:
        print("Post title too big, skipping")

    possible_comments = len(comments)

    # add comments
    for comment_data in comments:
        comment_element = ScriptElement(
            comment_data[0], comment_data[1], comment_data[2])

        print(f"Adding comment {i}/{possible_comments}", end="\r")

        if not script.can_add_script_element(comment_element):
            possible_comments -= 1
            continue

        script.add_script_element(comment_element)

    if (not script.finished):
        print(
            f"Script not finished, with duration of {script.duration} seconds.")
        proceed = prompt_bool("Do you still want to continue? (y/n): ")

        if not proceed:
            print("Exiting...")
            exit(0)

    print(f"Loaded {possible_comments}/{len(comments)} possible comments")

    print("Finished loading video script")

    output_location = prompt_write_file("Output location: ", overwrite=True)

    print("Exporting video...")
    start_time = time.time()
    # export video
    composeVideo(output_location, config.settings.background_footage,
                 script, config.export_settings, logger=default_bar_logger('bar'))

    print(f"Finished exporting video in {time.time() - start_time} seconds")


def handle_post_post(selected_post):
    print(selected_post.title)
    # r.create_post_video(posts[post_num], args.output, args.background)


def handle_system_args(parser, args, config, user_agent):
    # Handles system args here
    if 'help' in args:
        parser.print_help()
        exit(0)
    if args.version:
        print(f"Version: {config['project']['version']}")
        exit(0)
    if args.config:
        print(
            f"Config:\n[client_id:{config['reddit']['client_id']}]\n[client_secret:{config['reddit']['client_secret']}]\n[user_agent:{user_agent}]")
        exit(0)
    if args.system_voices:
        print("System voices:")
        tts = get_tts_engine("s")
        voices = tts.get_voices()

        for voice in voices:
            print(voice)

        print("Coqui voices:")
        tts = get_tts_engine("c")
        voices = tts.get_voices()

        for voice in voices:
            print(voice)

        exit(0)
    if args.clear:
        print("Clearing cache...")
        clear_cache()
        print("Cache cleared!")


def check_ouput_dir():
    if not is_dir(OUTPUT_PATH):
        print(f"Creating output path @ {OUTPUT_PATH}")
        make_dir(OUTPUT_PATH)
        make_dir(POSTS_PATH)
        make_dir(COMMENTS_PATH)


def main():
    args, parser = load_args()
    config = load_config()
    user_agent = create_user_agent(
        config["reddit"]["username"], config["project"]["version"])

    debug = args.debug

    handle_system_args(parser, args, config, user_agent)

    check_ouput_dir()

    print("RedditToVideo v" + config["project"]["version"])

    if not is_dir(CONFIG_PATH):
        print(f"Creating user configs directory at {CONFIG_PATH}")
        make_dir(CONFIG_PATH)
        print(f"Please create a user config and try again!")
        exit(1)

    print("Loading video configs...")
    video_configs = load_user_configs(CONFIG_PATH)

    if len(video_configs) == 0:
        print(f"No video configs found in {CONFIG_PATH}")
        exit(1)

    chosen_config: VideoConfig = prompt_list(
        list(map(lambda config: (config.name, config), video_configs)), "Select a video config: ")

    r = Reddit(config["reddit"]["client_id"], config["reddit"]
               ["client_secret"], user_agent, debug=False)

    posts = r.get_top_posts(chosen_config.settings.subreddit, limit=10)

    chosen_post = prompt_list(
        list(map(lambda post: (post.title, post), posts)), "Select a post: ")

    if chosen_config.settings["type"].lower() == "comment":
        handle_comment_post(chosen_post, chosen_config)

    elif chosen_config.settings["type"].lower() == "post":
        raise Exception("Post type not implemented yet")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)
    except Exception as e:
        print_exc()
        exit(1)
