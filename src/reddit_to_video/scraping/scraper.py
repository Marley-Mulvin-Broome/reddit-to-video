from os import rename as rename_file

from requests import get
from redvid import Downloader
from pytube import YouTube
from bs4 import BeautifulSoup

from reddit_to_video.scraping.validator import is_valid_kick_clip, is_valid_streamable_clip, is_valid_twitch_clip_url, ClipService
from reddit_to_video.exceptions import DurationTooLongError
from reddit_to_video.utility import can_write_to_file


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
    # if not can_write_to_file(output):
    #     raise Exception(
    #         f"download_youtube_video() output {output} is not a path that can be written to")

    youtube_obj = YouTube(url)
    youtube_obj.streams.get_highest_resolution().download(filename=output)


def download_streamable_video(url: str, output: str):
    """Downloads a streamable video to a file. 
    The output must be a path that can be written to"""
    if not is_valid_streamable_clip(url):
        raise Exception(
            f"download_streamable_video() url {url} is not a valid streamable url")

    return download_from_video_tag(url, output)


def download_kick_video(url: str, output: str):
    """Downloads a kick video to a file. 
    The output must be a path that can be written to"""
    if not is_valid_kick_clip(url):
        raise Exception(
            f"download_kick_video() url {url} is not a valid kick url")

    return download_from_video_tag(url, output)


def download_twitch_clip(url: str, output: str):
    """Downloads a twitch clip to a file. 
    The output must be a path that can be written to"""
    if not is_valid_twitch_clip_url(url):
        raise Exception(
            f"download_twitch_clip() url {url} is not a valid twitch clip url")

    return download_from_video_tag(url, output)


def download_from_video_tag(url: str, output: str):
    """Downloads a video from a video tag to a file. 
    The output must be a path that can be written to"""
    if not can_write_to_file(output):
        raise Exception(
            (f"download_from_video_tag() output {output} "
             "is not a path that can be written to"))

    # get html
    html = get_soup_from_url(url)
    # find video tag in entire html
    video = html.find_all("video")[0]

    if video is None:
        raise Exception(
            "download_from_video_tag() could not find video tag in html")

    # get the src attribute
    src = video['src']
    # download the that src
    content = retreieve_content_from_url(src)
    # write to file
    with open(output, "wb") as f:
        f.write(content)


def download_reddit_video(url: str, output: str) -> str:
    """Downloads a reddit video to a file. 
    The output must be a path that can be written to"""

    split_output = output.split("/")

    file_name = split_output[-1]

    file_path = "/".join(split_output[:-1])

    if len(split_output) <= 2:
        file_path += "/"

    downloader = Downloader(url=url, path=file_path,
                            max_q=True, log=False).download()

    if isinstance(downloader, str):
        rename_file(downloader, file_path + file_name)
        return downloader

    if downloader == 0:
        raise RuntimeError(
            "download_reddit_video() Video is too big to download")
    if downloader == 1:
        raise DurationTooLongError(
            "download_reddit_video() Video is too long to download")
    if downloader == 2:
        raise FileExistsError("download_reddit_video() File already exists")


def download_by_service(url: str, clip_server: ClipService, output_path: str) -> None:
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
