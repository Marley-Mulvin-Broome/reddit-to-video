import pytest
from bs4 import BeautifulSoup
from os.path import isfile as is_file
from moviepy.video.io.VideoFileClip import VideoFileClip

from reddit_to_video.scraping.scraper import retreieve_content_from_url
from reddit_to_video.scraping.scraper import get_soup_from_url
from reddit_to_video.scraping.scraper import download_from_video_tag
from reddit_to_video.scraping.scraper import download_reddit_video
from reddit_to_video.scraping.scraper import get_html_from_url
from reddit_to_video.scraping.scraper import download_youtube_video


def successfully_downloaded_video_file(fn: str) -> bool:
    if not is_file(fn):
        return False

    try:
        clip = VideoFileClip(fn)
        return clip.duration > 0
    except:
        return False


def test_get_html_from_url():
    url = "https://www.google.com"
    try:
        html = get_html_from_url(url)
        assert html is not None and isinstance(html, str)
    except Exception as e:
        assert False, e


def test_get_html_from_invalid_url():
    url = "https://www.google.com/invalid"

    with pytest.raises(Exception):
        get_html_from_url(url)


def test_get_soup_from_url():
    url = "https://www.google.com"
    try:
        soup = get_soup_from_url(url)
        assert soup is not None
        assert isinstance(soup, BeautifulSoup) is True
    except Exception as e:
        assert False, e


def test_get_soup_from_invalid_url():
    url = "https://www.google.com/invalid"

    with pytest.raises(Exception):
        get_soup_from_url(url)


def test_retreieve_content_from_url():
    url = "https://pbs.twimg.com/amplify_video_thumb/1644204106809217024/img/lszz9RgvzLTdXWK7.jpg"
    try:
        content = retreieve_content_from_url(url)
        assert content is not None and isinstance(content, bytes)
    except Exception as e:
        assert False, e


def test_retrieve_content_from_url_invalid_url():
    url = "https://www.google.com/invalid"
    with pytest.raises(Exception):
        retreieve_content_from_url(url)


# def test_download_reddit_video(tmp_path):
#     url = "https://www.reddit.com/r/fightporn/comments/e7i8op/stopped_to_appreciate_the_duck/"
#     try:
#         file_path = str(tmp_path / "test_reddit.mp4")

#         download_reddit_video(url, str(file_path))
#         assert successfully_downloaded_video_file(str(file_path))
#     except Exception as e:
#         assert False, e


def test_download_youtube_video(tmp_path):
    url = "https://www.youtube.com/watch?v=6ZfuNTqbHE8"
    try:
        file_path = str(tmp_path / "test_youtube.mp4")
        download_youtube_video(url, file_path)
        assert successfully_downloaded_video_file(file_path)
    except Exception as e:
        assert False, e


# def test_download_streamable_video(tmp_path):
#     url = "https://streamable.com/fpuv4"
#     try:
#         file_path = tmp_path / "streamable_test.mp4"
#         download_streamable_video(url, file_path)
#         assert successfully_downloaded_video_file(file_path)
#     except Exception as e:
#         assert False, e


# def test_download_kick_video(tmp_path):
#     url = "https://kick.com/sam?clip=44258"
#     try:
#         file_path = tmp_path / "kick_test.mp4"
#         download_kick_video(url, file_path)
#         assert successfully_downloaded_video_file(file_path)

#     except Exception as e:
#         assert False, e

# # hard to test twitch clips as they can expire and many other issues
# # @pytest.fixture(scope="session")
# # def test_download_twitch_clip(tmp_path_factory):


# def test_download_from_video_tag(tmp_path):
#     url = "https://kick.com/sam?clip=44258"
#     try:
#         file_path = tmp_path / "test_video.mp4"
#         download_from_video_tag(url, file_path)
#         assert successfully_downloaded_video_file(file_path)
#     except Exception as e:
#         assert False, e
