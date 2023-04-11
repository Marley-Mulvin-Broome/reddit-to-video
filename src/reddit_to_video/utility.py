from reddit_to_video.exceptions import OsNotSupportedError


import os
import sys
import subprocess
import re

from os.path import isfile as is_file
from os.path import isdir as is_dir
from os.path import join as path_join
from os import makedirs as make_dir

from contextlib import contextmanager

from requests import get

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip


def remove_links_from_text(text: str) -> str:
    """Removes links from text"""
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www\S+', '', text)
    return text


def download_img(url, destination) -> None:
    """Downloads an image from a url to a destination"""
    img_data = get(url).content

    with open(destination, 'wb') as handler:
        handler.write(img_data)


def get_audio_duration(audio_path: str) -> float:
    """Returns the duration of an audio file in seconds"""
    if not is_file(audio_path):
        raise FileExistsError(
            f"get_audio_duration() audio_path {audio_path} is not a file")

    if not audio_path.endswith(".mp3"):
        raise Exception(
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
        f = open(file_path, "w")
        f.close()
        return True
    except:
        return False


def remove_non_words(text: str) -> str:
    """Removes non-word characters from text"""
    text = re.sub(r'[^\w\s]|_', '', text)
    return text


# split_sentences regex from https://stackoverflow.com/questions/25735644/python-regex-for-splitting-text-into-sentences-sentence-tokenizing


def split_sentences(text: str) -> list:
    """Splits text into sentences"""
    return re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)


# from https://stackoverflow.com/questions/2125702/how-to-suppress-console-output-in-python


@contextmanager
def suppress_stdout():
    """Suppresses stdout"""
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def preview_video(video_path: str) -> None:
    """Opens a video file in the default video player"""
    if not is_file(video_path):
        raise FileExistsError(
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

    with open(file_path, "w") as f:
        f.write(content)

    return file_path
