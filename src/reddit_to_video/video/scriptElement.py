"""Module for representing elements of a script

Classes:
    ScriptElement: 
        Represents a single element in a VideoScript
"""

from os.path import isfile as is_file
from typing import Union

from reddit_to_video.exceptions import NoAudioError
from reddit_to_video.utility import get_video_duration, get_audio_duration, get_file_extension

valid_audio_file_types = [".mp3", ".wav"]
valid_visual_file_types = [".mp4", ".avi", ".png", ".jpg", ".jpeg"]


class ScriptElement:
    """Represents a single element in a VideoScript"""

    def __init__(self, text: str, visual_path: str, audio_path: Union[str, None], id_: int = -1):
        """Initialises a ScriptElement object"""
        if not isinstance(text, str):
            raise TypeError(
                f"ScriptElement() text '{text}' is not a string")

        if not isinstance(id_, int):
            raise TypeError(
                f"ScriptElement() id_ '{id_}' is not an integer")

        if not is_file(visual_path):
            raise FileNotFoundError(
                f"ScriptElement() visual_path {visual_path} is not a file")
        if get_file_extension(visual_path) not in valid_visual_file_types:
            raise ValueError(
                f"ScriptElement() visual_path {visual_path} is not a valid visual file type")
        if audio_path is not None and audio_path != "":
            if not is_file(audio_path):
                raise FileNotFoundError(
                    f"ScriptElement() audio_path {audio_path} is not a file")

            if get_file_extension(audio_path) not in valid_audio_file_types:
                raise ValueError(
                    f"ScriptElement() audio_path {audio_path} is not a valid audio file type")

        self.id = id_
        self.text = text
        self.visual_path = visual_path
        self.audio_path = audio_path

        self.duration = self.calculate_duration()

    def calculate_duration(self):
        """Calculates the duration of the ScriptElement, choosing the highest duration out of the visuald and audio if present"""
        return max(self.visual_duration, self.audio_duration)

    @property
    def visual_duration(self):
        """Returns the duration of the visual in seconds, or 0 if not a video"""
        if not self.is_video:
            return 0

        return get_video_duration(self.visual_path)

    @property
    def audio_duration(self):
        """Returns the duration of the audio in seconds, or the visual duration if not a video"""
        if self.audio_path is None or self.audio_path == "":
            if self.is_video:
                return self.visual_duration
            else:
                raise NoAudioError(
                    "ScriptElement() has no audio but is not a video")

        return get_audio_duration(self.audio_path)

    @property
    def is_video(self):
        """Returns True if the visual is a video, False otherwise"""
        return self.visual_path.endswith(".mp4") or self.visual_path.endswith(".avi")
