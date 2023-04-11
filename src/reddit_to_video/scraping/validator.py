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

url_pattern = re.compile("\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b")

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


class ClipService(Enum):
    """Enum for the different clip services"""
    NONE = 0
    TWITCH = 1
    STREAMABLE = 2
    KICK = 3
    YOUTUBE = 4
    REDDIT = 5


def get_urls_from_string(string: str) -> list:
    """Returns a list of urls from a string"""
    return url_pattern.findall(string)


def get_clip_service_from_url(url: str) -> ClipService:
    """Returns the clip service from a url"""
    if is_valid_twitch_clip_url(url):
        return ClipService.TWITCH
    elif is_valid_streamable_clip(url):
        return ClipService.STREAMABLE
    elif is_valid_kick_clip(url):
        return ClipService.KICK
    elif is_valid_youtube_url(url):
        return ClipService.YOUTUBE
    elif is_valid_reddit_clip_url(url):
        return ClipService.REDDIT

    return ClipService.NONE


def is_valid_url(url: str) -> bool:
    """Returns true if the url is valid"""
    return url_pattern.match(url) is not None


def is_valid_reddit_clip_url(url: str) -> bool:
    """Returns true if the url is a reddit clip"""
    if reddit_clip_pattern.match(url) is None:
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
