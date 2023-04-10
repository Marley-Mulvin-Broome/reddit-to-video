from .videoScript import VideoScript
from .scriptElement import ScriptElement
from .videoScript import VideoScript
from .exportSettings import ExportSettings
from os.path import isfile as is_file

from exceptions import EmptyCollectionError, OutputPathValidationError
from utility import can_write_to_file

# DO NOT import from moviepy.editor (has overhead)
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip, VideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.fx.resize import resize


def createCommentClip(script_element: ScriptElement):
    if not is_file(script_element.visual_path):
        raise Exception(
            f"createClip() visual path {script_element.visual_path} is not a file")

    audio_clip = None

    # external audio can be optional if video
    if is_file(script_element.audio_path):
        audio_clip = AudioFileClip(script_element.audio_path)
    elif not script_element.is_video:
        raise Exception(
            f"createClip() audio path {script_element.audio_path} is not a file and visual is not a video")

    if script_element.is_video:
        visual_clip = VideoFileClip(
            script_element.visual_path)

        if audio_clip is not None:
            visual_clip = visual_clip.set_audio(
                audio_clip).set_duration(script_element.duration)

        return visual_clip

    img = ImageClip(
        script_element.visual_path, duration=audio_clip.duration).set_audio(audio_clip)
    img.fps = 1

    return img


def composeCommentVideo(output_file: str, background_footage: str, script: VideoScript, export_settings: ExportSettings = None, logger=None):
    if not is_file(background_footage):
        raise FileExistsError(
            f"composeCommentVideo() background footage {background_footage} is not a file")

    if len(script) == 0:
        raise EmptyCollectionError("composeCommentVideo() script is empty")

    if export_settings is None:
        # create default export settings
        export_settings = ExportSettings()

    if not can_write_to_file(output_file):
        raise OutputPathValidationError(
            f"composeCommentVideo() output file {output_file} is not valid")

    # create background clip
    background_clip: VideoFileClip = VideoFileClip(
        background_footage, audio=False).set_fps(export_settings.fps)

    # create overlaying clips
    clips = []

    for script_element in script.script_elements:
        clips.append(createCommentClip(script_element))

    # merge clips into single track
    overlay = concatenate_videoclips(clips).set_position("center", "center")

    # create final clip
    final_clip = CompositeVideoClip(
        clips=[background_clip, overlay], size=background_clip.size).set_audio(overlay.audio).set_duration(overlay.duration)

    # export video
    final_clip.write_videofile(
        output_file, logger=logger, **export_settings.unbox())


def composeVideoVideo(output_file: str, script: VideoScript, target_resolution: tuple[int, int] = None, export_settings: ExportSettings = None, logger=None):
    if len(script) == 0:
        raise EmptyCollectionError("composeVideoVideo() script is empty")

    if export_settings is None:
        # create default export settings
        export_settings = ExportSettings()

    if not can_write_to_file(output_file):
        raise OutputPathValidationError(
            f"composeVideoVideo() output file {output_file} is not valid")

    clips = []

    cur_time = 0

    for script_element in script.all:
        clips.append(VideoFileClip(
            script_element.visual_path, target_resolution=(1080, 1920)).set_position("center", "center").set_start(cur_time))
        cur_time += script_element.duration

    # final_clip: VideoClip = concatenate_videoclips(
    #     clips).set_fps(export_settings.fps)

    final_clip = CompositeVideoClip(clips).set_fps(export_settings.fps)

    # if target_resolution is not None:
    #     resize(
    #         final_clip, width=target_resolution[0], height=target_resolution[1])

    final_clip.write_videofile(
        output_file, logger=logger, **export_settings.unbox())
