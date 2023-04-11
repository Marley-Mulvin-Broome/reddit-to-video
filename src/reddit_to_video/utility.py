"""Utility functions for reddit_to_video

Functions:
    remove_links_from_text(text: str) -> str: 
        Removes links from text

    download_img(url, destination) -> None: 
        Downloads an image from a url to a destination

    get_audio_duration(audio_path: str) -> float: 
        Returns the duration of an audio file in seconds

    get_video_duration(video_path: str) -> float: 
        Returns the duration of a video file in seconds
    
    can_write_to_file(file_path: str) -> bool: 
        Returns True if the file can be written to, False otherwise

    remove_non_words(text: str) -> str: 
        Removes non-word characters from text

    split_sentences(text: str) -> list: 
        Splits text into sentences

    preview_video(video_path: str) -> None: 
        Opens the video in the default video player

    write_temp(file_name: str, content) -> str: 
        Writes content to a temporary file

"""
import os
import subprocess
import re

from os.path import isfile as is_file
from os.path import isdir as is_dir
from os.path import join as path_join
from os import makedirs as make_dir

from requests import get

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

from reddit_to_video.exceptions import OsNotSupportedError

GLOBAL_TIMEOUT = 3000


def remove_links_from_text(text: str) -> str:
    """Removes links from text"""
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www\S+', '', text)
    return text


def download_img(url: str, destination: str) -> None:
    """Downloads an image from a url to a destination"""
    img_data = get(url, timeout=GLOBAL_TIMEOUT).content

    with open(destination, 'wb') as handler:
        handler.write(img_data)


def get_audio_duration(audio_path: str) -> float:
    """Returns the duration of an audio file in seconds"""
    if not is_file(audio_path):
        raise FileNotFoundError(
            f"get_audio_duration() audio_path {audio_path} is not a file")

    if not audio_path.endswith(".mp3"):
        raise TypeError(
            f"get_audio_duration() audio_path {audio_path} is not an mp3 file")

    audio = AudioFileClip(audio_path)
    return audio.duration


def get_video_duration(video_path: str) -> float:
    """Returns the duration of a video file in seconds"""
    video = VideoFileClip(video_path)
    return video.duration


def can_write_to_file(file_path: str) -> bool:
    """Returns True if the file can be written to, False otherwise"""
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            is_writable = file.writable()

        return is_writable
    except:
        return False


def remove_non_words(text: str) -> str:
    """Removes non-word characters from text"""
    text = re.sub(r'[^\w\s]|_', '', text)
    return text


def split_sentences(text: str) -> list:
    """Splits text into sentences"""
    return re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)


def preview_video(video_path: str) -> None:
    """Opens a video file in the default video player"""
    if not is_file(video_path):
        raise FileNotFoundError(
            f"preview_video() video_path {video_path} is not a file")

    if os.name == "nt":
        os.startfile(video_path)
    elif os.name == "posix":
        subprocess.Popen(["xdg-open", video_path])
    else:
        raise OsNotSupportedError(
            f"preview_video() os {os.name} is not supported for previewing videos")


TEMP_PATH = "output/temp"


def write_temp(file_name: str, content) -> str:
    """Writes content to a file in the temp directory"""
    if not is_dir(TEMP_PATH):
        make_dir(TEMP_PATH)

    file_path = path_join(TEMP_PATH, file_name)

    with open(file_path, "w") as file:
        file.write(content)

    return file_path
