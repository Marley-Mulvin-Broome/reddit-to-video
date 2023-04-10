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
reddit_clip_patter = re.compile(r"")


class ClipService(Enum):
    NONE = 0
    TWITCH = 1
    STREAMABLE = 2
    KICK = 3
    YOUTUBE = 4
    REDDIT = 5


def get_urls_from_string(string: str) -> list:
    return url_pattern.findall(string)


def get_clip_service_from_url(url: str) -> ClipService:
    if is_valid_twitch_clip_url(url):
        return ClipService.TWITCH
    elif is_valid_streamable_clip(url):
        return ClipService.STREAMABLE
    elif is_valid_kick_clip(url):
        return ClipService.KICK
    elif is_valid_youtube_url(url):
        return ClipService.YOUTUBE

    return ClipService.NONE


def is_valid_url(url: str) -> bool:
    return url_pattern.match(url) is not None


def is_valid_twitch_clip_url(url: str) -> bool:
    if twitch_clip_pattern.match(url) is None and twitch_channel_clip_pattern.match(url) is None:
        return False

    return True


def is_valid_streamable_clip(url: str) -> bool:
    if streamable_clip_pattern.match(url) is None:
        return False

    return True


def is_valid_kick_clip(url: str) -> bool:
    if kick_clip_pattern.match(url) is None:
        return False

    return True


def is_valid_youtube_url(url: str) -> bool:
    if youtube_clip_pattern.match(url) is None and youtube_share_clip_pattern.match(url) is None:
        return False

    return True
