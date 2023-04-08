from proglog import default_bar_logger
from os import listdir
from video import compression_settings
from dataclasses import dataclass
from video import Video
from moviepy.editor import ImageClip, concatenate_videoclips

COMMENT_GAP = 0.5


@dataclass
class VideoSettings:
    dimensions: tuple[int, int]
    fps: int
    compression: dict[str, str]
    max_length: int
    start_time: int
    max_img_size: tuple[int, int]
    max_comment_audio_length: int
    crop_region: tuple[int, int, int, int]
    bitrate: str
    threads: int

    def get_subsection(self, video_length) -> tuple[int, int]:
        if self.max_length == 0:
            return (0, 0)

        difference = self.start_time + self.max_length - video_length

        # since start time is out we need to truncate it
        if difference > 0 and self.start_time - video_length > 0:
            return (0, 0)

        if difference > 0:
            return (self.start_time, video_length)

        return (self.start_time, self.start_time + self.max_length)


class VideoComposer:
    def __init__(self, source_footage: str, video_settings: VideoSettings):
        self.video = Video.from_path(source_footage, True)
        self.video.cur_clip_subsection = video_settings.get_subsection(
            self.video.duration)

        self.settings = video_settings
        self.length_pointer = 0

        if self.settings.crop_region != (0, 0, 0, 0):
            self.video.crop(self.settings.crop_region)

        self.videos = []

    def check_img_size(self, img_clip: ImageClip) -> bool:
        return img_clip.w <= self.settings.max_img_size[0] and img_clip.h <= self.settings.max_img_size[1]

    def crop_img(self, img_clip: ImageClip) -> ImageClip:
        new_width = img_clip.w

        if new_width > self.settings.max_img_size[0]:
            new_width = self.settings.max_img_size[0]

        new_height = img_clip.h

        if new_height > self.settings.max_img_size[1]:
            new_height = self.settings.max_img_size[1]

        return img_clip.resize((new_width, new_height))

    def place_img(self, img_clip: ImageClip) -> ImageClip:
        # center image horizontally
        x = (self.video.width - img_clip.w) / 2
        # center image vertically
        y = (self.video.height - img_clip.h) / 2

        return img_clip.set_position((x, y))

    def add_comment(self, comment_image: str, comment_audio: str) -> bool:
        # audio_clip = self.video.load_audio_clip(
        #     comment_audio, self.length_pointer)
        audio_clip = self.video.load_audio_clip(
            comment_audio, 0)

        if self.length_pointer + audio_clip.duration > self.video.duration or audio_clip.duration > self.settings.max_comment_audio_length:
            return False

        # img_clip = self.video.load_img_clip(
        #     comment_image, self.length_pointer, audio_clip.duration)
        img_clip = self.video.load_img_clip(
            comment_image, 0, audio_clip.duration)

        if not self.check_img_size(img_clip):
            img_clip = self.crop_img(img_clip)

        img_clip = self.place_img(img_clip)

        subsection = self.video.subsect_new(
            audio_clip.start, audio_clip.end + COMMENT_GAP)

        subsection.overlay_img_with_audio(img_clip, audio_clip)
        self.videos.append(subsection)
        self.length_pointer += audio_clip.duration + COMMENT_GAP

        return True

    def export(self, output_path: str, logger=None):
        raw_vids = []

        for video in self.videos:
            video.apply_audio()
            raw_vids.append(video._clip)

        final_clip = concatenate_videoclips(raw_vids)

        # del raw_vids
        # del self.videos
        # del self.video

        final_clip = Video(final_clip)

        final_clip.export_compression_settings(output_path, self.settings.compression, logger=logger,
                                               threads=self.settings.threads, bitrate=self.settings.bitrate, fps=self.settings.fps)
