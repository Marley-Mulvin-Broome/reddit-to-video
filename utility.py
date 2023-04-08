from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from requests import get
import re

from os.path import isfile as is_file


def remove_links_from_text(text: str) -> str:
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'www\S+', '', text)
    return text


def download_img(url, destination) -> None:
    img_data = get(url).content

    with open(destination, 'wb') as handler:
        handler.write(img_data)


def get_audio_duration(audio_path: str) -> float:
    if not is_file(audio_path):
        raise FileExistsError(
            f"get_audio_duration() audio_path {audio_path} is not a file")

    if not audio_path.endswith(".mp3"):
        raise Exception(
            f"get_audio_duration() audio_path {audio_path} is not an mp3 file")

    audio = AudioFileClip(audio_path)
    return audio.duration


def get_video_duration(video_path: str) -> float:
    video = VideoFileClip(video_path)
    return video.duration


def can_write_to_file(file_path: str) -> bool:
    try:
        f = open(file_path, "w")
        f.close()
        return True
    except:
        return False


def remove_non_words(text: str) -> str:
    text = re.sub(r'[^\w\s]|_', '', text)
    return text


# split_sentences regex from https://stackoverflow.com/questions/25735644/python-regex-for-splitting-text-into-sentences-sentence-tokenizing


def split_sentences(text: str) -> list:
    return re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
