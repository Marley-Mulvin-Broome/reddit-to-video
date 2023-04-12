from os import rename as rename_file
from os.path import join as path_join

from requests import get
from redvid import Downloader
from pytube import YouTube
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from reddit_to_video.scraping.validator import is_valid_kick_clip, is_valid_streamable_clip, is_valid_twitch_clip_url, ClipService
from reddit_to_video.exceptions import DurationTooLongError


DEFAULT_REQ_TIMEOUT = 3000


def retreieve_content_from_url(url: str, timeout: int = DEFAULT_REQ_TIMEOUT) -> bytes:
    """Retreives the content of a url and returns it as bytes.
    Used for downloading img or video files"""
    response = get(url, timeout=timeout)

    if response.status_code != 200:
        raise Exception(
            f"retreieve_content_from_url() response status code is {response.status_code}")

    return response.content


def get_html_from_url(url: str, timeout: int = 3000) -> str:
    """Retreives the html of a url and returns it as a string"""
    response = get(url, timeout=timeout)

    if response.status_code != 200:
        raise Exception(
            f"get_html_from_url() response status code is {response.status_code}")

    return response.text


def get_soup_from_url(url: str, timeout: int = 3000) -> BeautifulSoup:
    """Retreives the html of a url and returns it as a BeautifulSoup object"""
    html = get_html_from_url(url, timeout=timeout)
    return BeautifulSoup(html, "html.parser")


def download_youtube_video(url: str, output: str):
    """Downloads a youtube video to a file.
    The output must be a path that can be written to"""
    youtube_obj = YouTube(url)
    youtube_obj.streams.get_highest_resolution().download(filename=output)


def download_streamable_video(url: str, output: str):  # pragma: no cover
    """Downloads a streamable video to a file.
    The output must be a path that can be written to"""
    if not is_valid_streamable_clip(url):
        raise Exception(
            f"download_streamable_video() url {url} is not a valid streamable url")

    return download_from_video_tag_js(url, output)


def download_kick_video(url: str, output: str):  # pragma: no cover
    """Downloads a kick video to a file.
    The output must be a path that can be written to"""
    if not is_valid_kick_clip(url):
        raise Exception(
            f"download_kick_video() url {url} is not a valid kick url")

    return download_from_video_tag_js(url, output)


def download_twitch_clip(url: str, output: str) -> None:  # pragma: no cover
    """Downloads a twitch clip to a file.
    The output must be a path that can be written to"""
    if not is_valid_twitch_clip_url(url):
        raise Exception(
            f"download_twitch_clip() url {url} is not a valid twitch clip url")

    return download_from_video_tag_js(url, output)


def download_from_video_tag_js(url: str, output: str) -> None:  # pragma: no cover
    """Downloads a video from a video tag to a file using selenium to load the javascript"""
    # load page with selenium then wait for it to load
    src = ""

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    with webdriver.Chrome('chromedriver', chrome_options=options) as driver:
        driver.get(url)

        delay = 3

        video_element = WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.TAG_NAME, "video")))

        src = video_element.get_attribute("src")

    download_from_link(src, output)


def download_from_link(src: str, output: str):
    """Downloads the contents of a response to a file."""
    # get the video content
    video_content = retreieve_content_from_url(src)

    # write the video content to a file
    with open(output, "wb") as f:
        f.write(video_content)


def download_from_video_tag(url: str, output: str):  # pragma: no cover
    """Downloads a video from a video tag to a file.
    The output must be a path that can be written to"""
    # get html
    html = get_soup_from_url(url)
    # find video tag in entire html
    video = html.find_all("video", recursive=True)[0]

    if video is None:
        raise Exception(
            "download_from_video_tag() could not find video tag in html")

    # get the src attribute
    src = video['src']

    download_from_link(src, output)


def download_reddit_video(url: str, output: str) -> str:  # pragma: no cover
    """Downloads a reddit video to a file.
    The output must be a path that can be written to"""

    split_output = output.split("/")

    file_name = split_output[-1]

    file_path = "/".join(split_output[:-1]) + "/"

    downloader = Downloader(url=url, path=file_path,
                            max_q=True, log=False).download()

    if isinstance(downloader, str):
        rename_file(downloader, path_join(file_path, file_name))
        return downloader

    if downloader == 0:
        raise RuntimeError(
            "download_reddit_video() Video is too big to download")
    if downloader == 1:
        raise DurationTooLongError(
            "download_reddit_video() Video is too long to download")
    if downloader == 2:
        raise FileExistsError("download_reddit_video() File already exists")


def download_by_service(url: str, clip_server: ClipService, output_path: str) -> None:  # pragma: no cover
    """Downloads a clip from a url to a file.
    The output must be a path that can be written to"""
    if clip_server.value == ClipService.TWITCH.value:
        download_twitch_clip(url, output_path)
    elif clip_server.value == ClipService.STREAMABLE.value:
        download_streamable_video(url, output_path)
    elif clip_server.value == ClipService.KICK.value:
        download_kick_video(url, output_path)
    elif clip_server.value == ClipService.YOUTUBE.value:
        download_youtube_video(url, output_path)
    elif clip_server.value == ClipService.REDDIT.value:
        download_reddit_video(url, output_path)
    else:
        raise Exception(
            (f"download_by_service() clip_server {clip_server}"
             "is not a valid clip server"))
