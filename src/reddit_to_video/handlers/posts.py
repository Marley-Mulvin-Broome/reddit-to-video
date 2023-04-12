import logging
import time

from os.path import isfile as is_file
from os.path import join as path_join
from multiprocessing.pool import Pool
from sys import exit as exit_program

from praw.models.reddit.submission import Submission
from tqdm import tqdm
from proglog import default_bar_logger

from reddit_to_video.scraping.validator import get_clip_service_from_url, ClipService
from reddit_to_video.scraping.scraper import download_reddit_video, download_by_service
from reddit_to_video.video.compose import composeVideoVideo
from reddit_to_video.video.scriptelement import ScriptElement
from reddit_to_video.video.script import VideoScript
from reddit_to_video.video.config import VideoConfig
from reddit_to_video.prompts import prompt_bool, prompt_write_file, prompt_preview_vid
from reddit_to_video.exceptions import ScriptElementTooLongError
from reddit_to_video.logging.handle import setup_logging, remove_logger


POST_VIDEO_OUTPUT = "output/posts/"


def get_video_from_post(post: Submission) -> ScriptElement:
    """Gets a video from a post"""
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

    # if post.selftext != "":
    #     urls = get_urls_from_string(post.selftext)

    #     if urls != []:
    #         url = urls[0]
    #     else:
    #         logging.warning(
    #             f"Post ({post.id}, {post.title}) has no urls in its text")
    #         return None

    clip_service = get_clip_service_from_url(url)

    if clip_service.value == ClipService.NONE.value:
        logging.warning(
            f"Post ({post.id}, {post.title}, {url}) has no supported clip service")
        return None

    try:
        download_by_service(url, clip_service, output_path)
    except Exception as e:
        logging.error(
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

    setup_logging()

    with tqdm(total=len(posts)) as pbar:
        with Pool(processes=10) as pool:
            for post in pool.imap_unordered(get_video_from_post, posts):
                pbar.update(1)

                if post is None:
                    continue

                if post.duration > config_settings.settings.max_video_length:
                    pbar.write(
                        (f"Post ({post.text}) is too long, "
                         f"skipping ({post.duration} seconds)"))
                    continue

                if video_break_element is not None:
                    script_elements.append((post, video_break_element))
                else:
                    script_elements.append(post)

    remove_logger()

    print("Finished getting videos from posts")

    if len(script_elements) == 0:
        print("No videos found, exiting...")
        exit_program(0)

    script = VideoScript(config_settings.settings.max_length,
                         config_settings.settings.min_length)
    try:
        script.add_script_element(end_card_element, True)
    except ScriptElementTooLongError:
        prompt_continue = prompt_bool(
            "End card too big, do you want to continue? (y/n): ")

        if not prompt_continue:
            exit_program(0)

        print("Skipping end card...")

    if video_break_element is not None:
        script.add_script_element_pairs(script_elements)
    else:
        script.add_script_elements(script_elements)
    if not script.finished:
        print(
            f"Script not finished, with duration of {script.cur_length} seconds.")
        proceed = prompt_bool("Do you still want to continue? (y/n): ")

        if not proceed:
            print("Exiting...")
            exit_program(0)

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
