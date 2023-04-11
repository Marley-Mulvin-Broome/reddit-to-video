import pytest
from reddit_to_video.scraping.scraper import retreieve_content_from_url
from reddit_to_video.scraping.scraper import get_soup_from_url
from reddit_to_video.scraping.scraper import download_from_video_tag
from reddit_to_video.scraping.scraper import download_kick_video
from reddit_to_video.scraping.scraper import download_reddit_video
from reddit_to_video.scraping.scraper import download_streamable_video
from reddit_to_video.scraping.scraper import get_html_from_url
from bs4 import BeautifulSoup
from os.path import isfile as is_file


def test_get_html_from_url():
    url = "https://www.google.com"
    try:
        html = get_html_from_url(url)
        assert html is not None and isinstance(html, str)
    except Exception as e:
        assert False, e


def test_get_soup_from_url():
    url = "https://www.google.com"
    try:
        soup = get_soup_from_url(url)
        assert soup is not None
        assert isinstance(soup, BeautifulSoup) is True
    except Exception as e:
        assert False, e


def test_retreieve_content_from_url():
    url = "https://pbs.twimg.com/amplify_video_thumb/1644204106809217024/img/lszz9RgvzLTdXWK7.jpg"
    try:
        content = retreieve_content_from_url(url)
        assert content is not None and isinstance(content, bytes)
    except Exception as e:
        assert False, e


@pytest.fixture(scope="session")
def test_download_reddit_video(tmp_path_factory):
    url = "https://www.reddit.com/r/fightporn/comments/e7i8op/stopped_to_appreciate_the_duck/"
    try:
        fn = tmp_path_factory.mktemp("test") / "reddit_test.mp4"
        download_reddit_video(url, fn)
        assert is_file(fn) is True
    except Exception as e:
        assert False, e


@pytest.fixture(scope="session")
def test_download_streamable_video(tmp_path_factory):
    url = "https://streamable.com/fpuv4"
    try:
        fn = tmp_path_factory.mktemp("test") / "streamable_test.mp4"
        download_streamable_video(url, fn)
        assert is_file(fn) is True
    except Exception as e:
        assert False, e


@pytest.fixture(scope="session")
def test_download_kick_video(tmp_path_factory):
    url = "https://kick.com/sam?clip=44258"
    try:
        fn = tmp_path_factory.mktemp("test") / "kick_test.mp4"
        download_kick_video(url, fn)
        assert is_file(fn) is True
    except Exception as e:
        assert False, e

# hard to test twitch clips as they can expire and many other issues
# @pytest.fixture(scope="session")
# def test_download_twitch_clip(tmp_path_factory):


@pytest.fixture(scope="session")
def test_download_from_video_tag(tmp_path_factory):
    url = "https://kick.com/sam?clip=44258"
    try:
        fn = tmp_path_factory.mktemp("test") / "video_tag_test.mp4"
        download_from_video_tag(url, fn)
        assert is_file(fn) is True
    except Exception as e:
        assert False, e
