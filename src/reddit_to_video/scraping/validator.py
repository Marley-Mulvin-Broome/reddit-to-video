"""Validator module used for validating urls specifically video platforms

Classes:
    ClipService: Enum representing a video platform

Functions:
    validate_url: Validates a url and returns the service it belongs to
    get_clip_service_from_url: Returns the service a url belongs to
    is_valid_twitch_clip_url: Returns true if the url is a valid twitch clip url
    is_valid_youtube_url: Returns true if the url is a valid youtube url
    is_valid_streamable_url: Returns true if the url is a valid streamable url
    is_valid_kick_url: Returns true if the url is a valid kick url

"""

import re
from enum import Enum

url_pattern = re.compile(
    ".*^https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$.*")
url_pattern_no_https = re.compile(
    ".*^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$.*")

# twitch
twitch_clip_pattern = re.compile(r".*clips\.twitch\.tv.*")
twitch_channel_clip_pattern = re.compile(r".*twitch\.tv\/.*\/clip.*")

# streamable
streamable_clip_pattern = re.compile(r".*streamable.com\/.*")

# kick
kick_clip_pattern = re.compile(r".*kick.com\/.*\?clip=.*")

# youtube
youtube_clip_pattern = re.compile(r".*youtube\.com\/watch\?v=.*")
youtube_share_clip_pattern = re.compile(r".*youtu\.be\/.*")

# reddit
reddit_clip_pattern = re.compile(r".*www.reddit.com/r/.*/comments/.*")
reddit_shortened_pattern = re.compile(
    r".*v\.redd\.it/.*")  # https://v.redd.it/yw6nan929np31


class ClipService(Enum):
    """Enum for the different clip services"""
    NONE = 0
    TWITCH = 1
    STREAMABLE = 2
    KICK = 3
    YOUTUBE = 4
    REDDIT = 5


def get_clip_service_from_url(url: str) -> ClipService:
    """Returns the clip service from a url"""
    if is_valid_twitch_clip_url(url):
        return ClipService.TWITCH
    if is_valid_streamable_clip(url):
        return ClipService.STREAMABLE
    if is_valid_kick_clip(url):
        return ClipService.KICK
    if is_valid_youtube_url(url):
        return ClipService.YOUTUBE
    if is_valid_reddit_clip_url(url):
        return ClipService.REDDIT

    return ClipService.NONE


def is_valid_url(url: str) -> bool:
    """Returns true if the url is valid"""
    return url_pattern.match(url) is not None or url_pattern_no_https.match(url) is not None


def is_valid_reddit_clip_url(url: str) -> bool:
    """Returns true if the url is a reddit clip"""
    if reddit_clip_pattern.match(url) is None and reddit_shortened_pattern.match(url) is None:
        return False

    return True


def is_valid_twitch_clip_url(url: str) -> bool:
    """Returns true if the url is a twitch clip"""
    if twitch_clip_pattern.match(url) is None and twitch_channel_clip_pattern.match(url) is None:
        return False

    return True


def is_valid_streamable_clip(url: str) -> bool:
    """Returns true if the url is a streamable clip"""
    if streamable_clip_pattern.match(url) is None:
        return False

    return True


def is_valid_kick_clip(url: str) -> bool:
    """Returns true if the url is a kick clip"""
    if kick_clip_pattern.match(url) is None:
        return False

    return True


def is_valid_youtube_url(url: str) -> bool:
    """Returns true if the url is a youtube clip"""
    if youtube_clip_pattern.match(url) is None and youtube_share_clip_pattern.match(url) is None:
        return False

    return True
