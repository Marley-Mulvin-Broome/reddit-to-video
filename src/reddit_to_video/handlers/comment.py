import time

from os.path import isfile as is_file
from sys import exit as exit_program

from proglog import default_bar_logger

from reddit_to_video.video.tts import get_tts_engine
from reddit_to_video.video.config import VideoConfig
from reddit_to_video.video.script import VideoScript
from reddit_to_video.video.scriptelement import ScriptElement
from reddit_to_video.video.compose import compose_comment_video
from reddit_to_video.post import Post
from reddit_to_video.exceptions import ScriptElementTooLongError
from reddit_to_video.prompts import prompt_bool, prompt_write_file, prompt_preview_vid


def handle_comment_post(selected_post, config: VideoConfig):
    """Handles a comment post"""
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
    except Exception:
        print("Failed to screenshot post title, is it new reddit layout?")
        print("Tryting again...")

        max_failures -= 1

        if max_failures == 0:
            print("Failed to screenshot post title")
            exit_program(1)

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
                comment.id, "output/comments/")

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
    except ScriptElementTooLongError:
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
            exit_program(0)

    print(f"Loaded {possible_comments}/{len(comments)} possible comments")

    print("Finished loading video script")

    output_location = prompt_write_file("Output location: ", overwrite=True)

    print("Exporting video...")
    start_time = time.time()
    # export video
    compose_comment_video(output_location,
                          config.settings.background_footage,
                          script,
                          config.export_settings,
                          logger=default_bar_logger('bar'))

    print(f"Finished exporting video in {time.time() - start_time} seconds")

    prompt_preview_vid(output_location)
