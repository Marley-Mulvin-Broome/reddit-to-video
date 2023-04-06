from reddit import Reddit
from configparser import ConfigParser
from os import getcwd
from argparse import ArgumentParser
from os.path import join as path_join
from tts import TTS, google_accents
from traceback import print_exc

default_output_dir = path_join(getcwd(), "output/out.mp4")
default_subreddit = "?"
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
    parser = ArgumentParser(
        description="Creates a video from top posts from a subreddit", add_help=False)

    vid_args = parser.add_argument_group("Video Arguments")
    vid_args.add_argument(
        "-t", "--type", help="Set type of content to create [comment|post]", type=str, required=False, default="none")
    vid_args.add_argument("-o", "--output",  help="Set output directory",
                          type=str, required=False, default=default_output_dir)
    vid_args.add_argument("-s", "--subreddit", help="Set subreddit",
                          type=str, required=False, default=default_subreddit)
    vid_args.add_argument("-bg", "--background", help="Set directory where the background footage is stored",
                          type=str, required=False, default=default_bg_dir)

    system_args = parser.add_argument_group("System Arguments")
    system_args.add_argument(
        "-h", "--help", action="help", help="Show this help message and exit")
    system_args.add_argument(
        "-v", "--version", action="store_false", help="Show version", required=False, default=False)
    system_args.add_argument(
        "-c", "--config", action="store_true", help="Show config", required=False, default=False)
    system_args.add_argument("-d", "--debug", action="store_true",
                             help="Sets the program to debug mode", required=False)

    return parser.parse_args(), parser


def prompt_type():
    print("Enter type of content to create [comment|post]: ", end="")

    result = input()

    while result != "comment" and result != "post":
        print(
            "Invalid type. Enter type of content to create [comment|post]: ", end="")
        input()

    return result


def prompt_subreddit():
    print("Enter a subreddit: ", end="")
    return input()


def prompt_voice(voices):
    print("Enter a voice:\n", end="")

    for i, voice in enumerate(voices):
        print(f"[{i}] {voice.name}")

    voice_num = -1

    while voice_num < 0 or voice_num > len(voices):
        print("Enter voice number: ", end="")
        voice_num = int(input())

    return voices[voice_num]


def prompt_tts_engine():
    print("Would you like to use google translate or your systems engine? (g/s): ", end="")
    result = input()

    while result != "g" and result != "s":
        print("Invalid type. Would you like to use google translate or your systems engine? (g/s): ", end="")
        result = input()

    return result


def prompt_google_accent():
    print("Enter a google accent number: ", end="")

    accents = []

    for i, accent in enumerate(google_accents.keys()):
        print(f"[{i}] {accent}")
        accents.append(google_accents[accent])

    accent_num = -1

    while accent_num < 0 or accent_num > len(accents):
        print("Enter accent number: ", end="")
        accent_num = int(input())

    return accents[accent_num]


def handle_comment_post(selected_post):
    selected_engine = prompt_tts_engine()

    tts = None

    if selected_engine == "g":
        tts = TTS(selected_engine, accent=prompt_google_accent())
    elif selected_engine == "s":
        tts = TTS(selected_engine)
        tts.select_voice(prompt_voice(tts.get_voices()))

    for comment in selected_post.comments:
        tts.save_audio(
            comment.body, f"output/comments/comment - {comment.id}.mp3")
    # r.create_comment_video(posts[post_num], args.output, args.background)

    if tts.selected_engine == "systemTTS":
        tts.run()


def handle_post_post(selected_post):
    print(selected_post.title)
    # r.create_post_video(posts[post_num], args.output, args.background)


def main():
    args, parser = load_args()
    config = load_config()
    user_agent = create_user_agent(
        config["reddit"]["username"], config["project"]["version"])

    debug = args.debug

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

    print("RedditToVideo v" + config["project"]["version"])

    r = Reddit(config["reddit"]["client_id"], config["reddit"]
               ["client_secret"], user_agent, debug=debug)

    if args.type == "none":
        args.type = prompt_type()

    if args.subreddit == default_subreddit:
        args.subreddit = prompt_subreddit()

    posts = r.get_top_posts(args.subreddit, limit=10)

    cur_posts = []

    for i, post in enumerate(posts):
        cur_posts.append(post)
        print(f"[{i}] {post.title} ({post.score})")

    post_num = -1

    while post_num < 0 or post_num > 9:
        print("Enter post number: ", end="")
        post_num = int(input())

    selected_post = cur_posts[post_num]

    if args.type == "comment":
        handle_comment_post(selected_post)

    elif args.type == "post":
        handle_post_post(selected_post)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)
    except Exception as e:
        print_exc()
        exit(1)
