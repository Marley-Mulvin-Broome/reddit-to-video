from moviepy.editor import VideoFileClip, ImageClip, AudioFileClip, CompositeVideoClip

compression_settings = {
    "Low": {
        "codec": "mpeg4",
        "preset": "veryfast",
        "audio_codec": "aac",
        "audio_bitrate": "192k"
    },
    "Medium": {
        "codec": "mpeg4",
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
    def __init__(self, source_clip: str, subsection=(0, 0)):
        self._source_clip = VideoFileClip(source_clip)
        self._clip = self._source_clip
        self.subsection = subsection

    @property
    def subsection(self) -> tuple:
        return self._subsection

    @subsection.setter
    def subsection(self, subsection):
        self._subsection = subsection

        if subsection[0] != 0 and subsection[1] != 0:
            self._clip = self._source_clip.subclip(
                subsection[0], subsection[1])

    @property
    def width(self) -> int:
        return self._clip.w

    @property
    def height(self) -> int:
        return self._clip.h

    def load_img_clip(self, img: str, start_time, duration, pos=(0, 0), size=(0, 0)) -> ImageClip:
        if (size[0] == 0 and size[1] == 0):
            size = (self.width, self.height)

        return ImageClip(img).set_start(start_time).set_duration(
            duration).resize(size).set_pos(pos)

    def load_audio_clip(self, audio: str, start_time: int, duration: int = 0, volume=1.0) -> AudioFileClip:
        audio_clip = AudioFileClip(audio).set_start(
            start_time).set_volume(volume)

        if duration != 0:
            return audio_clip.set_duration(duration)

        return AudioFileClip

    def overlay_img(self, img: str, start_time: int, duration: int, pos=(0, 0), size=(0, 0)) -> None:
        img_clip = self.load_img_clip(img, start_time, duration, pos, size)
        self._clip = CompositeVideoClip([self._clip, img_clip])

    def overlay_audio(self, audio: str, start_time: int, duration: int) -> None:
        audio_clip = self.load_audio_clip(audio, start_time, duration)
        self._clip = CompositeVideoClip([self._clip, audio_clip])

    def overlay_img_with_audio(self, img: str, audio: str, start_time: int, duration: int, pos=(0, 0), size=(0, 0)) -> None:
        img_clip = self.load_img_clip(img, start_time, duration, pos, size)
        audio_clip = self.load_audio_clip(audio, start_time, duration)
        self._clip = CompositeVideoClip([self._clip, img_clip, audio_clip])

    def export(self, output, compression_settings, fps=60, logger=None) -> None:
        self.export(output, fps, compression_settings["codec"], compression_settings["preset"],
                    compression_settings["audio_codec"], compression_settings["audio_bitrate"])

    def export(self, output: str, logger=None, fps=60, codec="libx264", preset="veryslow", audio_codec="aac", audio_bitrate="192k", threads=None) -> None:
        self._clip.write_videofile(output, fps=fps, codec=codec, preset=preset,
                                   audio_codec=audio_codec, audio_bitrate=audio_bitrate, threads=threads, logger=logger)

    def close(self) -> None:
        self._clip.close()
        self._source_clip.close()
