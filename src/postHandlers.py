from video.compose import composeCommentVideo, composeVideoVideo
from video.scriptElement import ScriptElement
from video.videoScript import VideoScript
from video.vidConfig import VideoConfig
from tts import get_tts_engine
from prompts import prompt_bool, prompt_write_file
from exceptions import ScriptElementTooLongError
from post import Post
from proglog import default_bar_logger
from os.path import isfile as is_file
from os.path import join as path_join
from os import getcwd
from scraping.urlValidator import get_clip_service_from_url, get_urls_from_string, ClipService
from scraping.scraper import download_reddit_video, download_by_service
from multiprocessing.pool import Pool
from praw.models.reddit.submission import Submission
from tqdm import tqdm
from utility import preview_video

import logging
import time


def prompt_preview_vid(output_location: str):
    will_preview = prompt_bool("Preview video? (y/n): ")

    if not will_preview:
        return

    try:
        preview_video(path_join(getcwd(), output_location))
    except Exception as e:
        print("Failed to preview video")
        print(e)


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
            exit(0)

    print(f"Loaded {possible_comments}/{len(comments)} possible comments")

    print("Finished loading video script")

    output_location = prompt_write_file("Output location: ", overwrite=True)

    print("Exporting video...")
    start_time = time.time()
    # export video
    composeCommentVideo(output_location, config.settings.background_footage,
                        script, config.export_settings, logger=default_bar_logger('bar'))

    print(f"Finished exporting video in {time.time() - start_time} seconds")

    prompt_preview_vid(output_location)


POST_VIDEO_OUTPUT = "output/posts/"


def get_video_from_post(post: Submission) -> ScriptElement:
    output_path = path_join(POST_VIDEO_OUTPUT, f"{post.id}.mp4")

    if is_file(output_path):
        return ScriptElement(post.title, output_path, None)

    if post.is_self:
        try:
            download_reddit_video(post.url, output_path)

            return ScriptElement(post.title, output_path, output_path, None)
        except Exception:
            logging.info(
                f"Post ({post.id}, {post.title}) is not a reddit video")
            return None

    url = post.url

    if post.selftext != "":
        urls = get_urls_from_string(post.selftext)

        if urls != []:
            url = urls[0]
        else:
            logging.info(
                f"Post ({post.id}, {post.title}) has no urls in its text")
            return None

    clip_service = get_clip_service_from_url(url)

    if clip_service.value == ClipService.NONE.value:
        print(
            f"Post ({post.id}, {post.title}) has no supported clip service")
        return None

    try:
        download_by_service(url, clip_service, output_path)
    except Exception as e:
        print(
            f"Post ({post.id}, {post.title}) failed to download from {clip_service.value}. ({e})")
        return None

    return ScriptElement(post.title, output_path, None)


def handle_video_post(posts, config_settings: VideoConfig, end_card_footage: str = None, video_break_footage: str = None):
    script_elements = []

    video_break_element = None
    end_card_element = None

    if video_break_footage is not None:
        video_break_element = ScriptElement("", video_break_footage, None)
    if end_card_footage is not None:
        end_card_element = ScriptElement("", end_card_footage, None)

    posts = list(posts)

    print(f"Getting videos from {len(posts)} posts on 10 threads...")

    with tqdm(total=len(posts), position=1) as pbar:
        with Pool(processes=10) as pool:
            for post in pool.imap_unordered(get_video_from_post, posts):
                pbar.update(1)

                if post is None:
                    continue

                if post.duration > config_settings.settings.max_video_length:
                    print(
                        f"Post ({post.text}) is too long, skipping ({post.duration} seconds)")
                    continue

                if video_break_element is not None:
                    script_elements.append((post, video_break_element))
                else:
                    script_elements.append(post)

    print("Finished getting videos from posts")

    script = VideoScript(config_settings.settings.max_length,
                         config_settings.settings.min_length)
    script.add_script_element(end_card_element, True)

    with tqdm(total=len(script_elements)) as pbar:
        if video_break_element is not None:
            script.add_script_element_pairs(script_elements, pbar=pbar)
        else:
            script.add_script_elements(script_elements, pbar=pbar)
    if not script.finished:
        print(
            f"Script not finished, with duration of {script.duration} seconds.")
        proceed = prompt_bool("Do you still want to continue? (y/n): ")

        if not proceed:
            print("Exiting...")
            exit(0)

    output_location = prompt_write_file("Output location: ", overwrite=True)

    target_resolution = None

    if config_settings.has_setting("target_resolution"):
        target_resolution = config_settings.settings.target_resolution

    start_time = time.time()

    composeVideoVideo(output_location, script,
                      target_resolution=(
                          target_resolution.width, target_resolution.height),
                      export_settings=config_settings.export_settings,
                      logger=default_bar_logger('bar'))

    print(f"Finished exporting video in {time.time() - start_time} seconds")

    prompt_preview_vid(output_location)
