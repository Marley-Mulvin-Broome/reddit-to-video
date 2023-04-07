from moviepy.editor import VideoFileClip, ImageClip, AudioFileClip, CompositeAudioClip, CompositeVideoClip

compression_settings = {
    "Low": {
        "codec": "libx264",
        "preset": "veryfast",
        "audio_codec": "aac",
        "audio_bitrate": "192k"
    },
    "Medium": {
        "codec": "libx264",
        "preset": "fast",
        "audio_codec": "aac",
        "audio_bitrate": "192k"
    },
    "High": {
        "codec": "libx264",
        "preset": "medium",
        "audio_codec": "aac",
        "audio_bitrate": "192k"
    },
    "Ultra": {
        "codec": "libx264",
        "preset": "veryslow",
        "audio_codec": "aac",
        "audio_bitrate": "192k"
    }
}


class Video:
    def __init__(self, source_clip: str, load_video_audio: bool = False, subsection=(0, 0)):
        # source and subclip will be the same unless there is a subsection
        self._source_clip: VideoFileClip = VideoFileClip(
            source_clip, audio=load_video_audio)
        self._clip: VideoFileClip = self._source_clip
        self.subsection = subsection
        self.audio = []

    @property
    def subsection(self) -> tuple:
        return self._subsection

    @subsection.setter
    def subsection(self, subsection):
        self._subsection = subsection

        if subsection[0] != 0 or subsection[1] != 0:
            self._clip = self._source_clip.subclip(
                subsection[0], subsection[1])

    @property
    def width(self) -> int:
        return self._clip.w

    @property
    def height(self) -> int:
        return self._clip.h

    @property
    def duration(self) -> int:
        return self._clip.duration

    def crop(self, region: tuple) -> None:
        self._clip = self._clip.crop(region)

    def load_img_clip(self, img: str, start_time, duration, pos=(0, 0), size=(0, 0)) -> ImageClip:
        if (size[0] == 0 and size[1] == 0):
            size = (self.width, self.height)

        return ImageClip(img).set_start(start_time).set_duration(
            duration).resize(width=size[0], height=size[1]).set_pos(pos)

    def load_audio_clip(self, audio: str, start_time: int = 0, duration: int = 0, volume=1.0) -> AudioFileClip:
        audio_clip = AudioFileClip(audio).set_start(
            start_time).volumex(volume)

        if duration != 0:
            return audio_clip.set_duration(duration)

        return audio_clip

    def overlay_img(self, img: str, start_time: int, duration: int, pos=(0, 0), size=(0, 0)) -> None:
        img_clip = self.load_img_clip(img, start_time, duration, pos, size)
        self._clip = CompositeVideoClip([self._clip, img_clip])

    def overlay_audio(self, audio: str, start_time: int, duration: int) -> None:
        audio_clip = self.load_audio_clip(audio, start_time, duration)
        self.audioappend(audio_clip)

    def overlay_img_with_audio(self, img: str, audio: str, start_time: int, duration: int, pos=(0, 0), size=(0, 0)) -> None:
        img_clip = self.load_img_clip(img, start_time, duration, pos, size)
        audio_clip = self.load_audio_clip(audio, start_time, duration)
        self._clip = CompositeVideoClip([self._clip, img_clip])
        self.audio.append(audio_clip)

    def overlay_img_with_audio(self, img: ImageClip, audio: AudioFileClip):
        self.audio.append(audio)
        self._clip = CompositeVideoClip([self._clip, img])

    def export_compression_settings(self, output, compression_settings, bitrate="8M", threads=16, fps=60, logger=None) -> None:
        self.export(output, **compression_settings, fps=fps, logger=logger, bitrate=bitrate,
                    threads=threads)

    def export(self, output: str, logger=None, bitrate="8M", threads=16, fps=60, codec="libx264", preset="veryslow", audio_codec="aac", audio_bitrate="192k") -> None:
        self._clip = self._clip.set_audio(CompositeAudioClip(self.audio))
        self._clip.write_videofile(output, fps=fps, codec=codec, preset=preset,
                                   audio_codec=audio_codec, audio_bitrate=audio_bitrate, bitrate=bitrate, threads=threads, logger=logger)

    def close(self) -> None:
        self._clip.close()
        self._source_clip.close()
