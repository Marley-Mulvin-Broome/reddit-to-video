from reddit_to_video.exceptions import NoAudioError
from reddit_to_video.utility import get_video_duration, get_audio_duration

from os.path import isfile as is_file


class ScriptElement:
    def __init__(self, text, visual_path, audio_path, id_=-1):
        if not is_file(visual_path):
            raise Exception(
                f"ScriptElement() visual_path {visual_path} is not a file")
        if audio_path is not None and audio_path != "":
            if not is_file(audio_path):
                raise Exception(
                    f"ScriptElement() audio_path {audio_path} is not a file")

        self.id = id_
        self.text = text
        self.visual_path = visual_path
        self.audio_path = audio_path

        self.duration = self.calculate_duration()

    def calculate_duration(self):
        return max(self.visual_duration, self.audio_duration)

    @property
    def visual_duration(self):
        if not self.is_video:
            return 0

        return get_video_duration(self.visual_path)

    @property
    def audio_duration(self):
        if self.audio_path is None or self.audio_path == "":
            if self.is_video:
                return self.visual_duration
            else:
                raise NoAudioError(
                    "ScriptElement() has no audio but is not a video")

        return get_audio_duration(self.audio_path)

    @property
    def is_video(self):
        return self.visual_path.endswith(".mp4") or self.visual_path.endswith(".avi")
