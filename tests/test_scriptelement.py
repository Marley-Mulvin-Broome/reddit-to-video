import pytest

import os
from os.path import join as path_join
from reddit_to_video.video.scriptelement import ScriptElement
from reddit_to_video.exceptions import NoAudioError


def get_current_dir() -> str:
    """Returns the current directory"""
    return os.path.dirname(os.path.realpath(__file__))


image_file = path_join(get_current_dir(), "image.png")
video_file = path_join(get_current_dir(), "video.mp4")
audio_file = path_join(get_current_dir(), "audio.mp3")

raises_error_init = [
    ("", video_file, "doesnt_exist.mp3", FileNotFoundError),  # invalid audio_path
    ("", "doesnt_exist.mp4", audio_file, FileNotFoundError),  # invalid visual_path
    ("", image_file, None, NoAudioError)  # image without audio
]


@pytest.mark.parametrize("text, visual_path, audio_path, exception", raises_error_init)
def test_init_raises_error(text, visual_path, audio_path, exception: Exception):
    with pytest.raises(exception):
        ScriptElement(text, visual_path, audio_path)


no_error_init = [
    ("", video_file, audio_file),
    ("", image_file, audio_file),
    ("", video_file, None)
]


@pytest.mark.parametrize("text, visual_path, audio_path", no_error_init)
def test_init_no_error(text, visual_path, audio_path):
    try:
        ScriptElement(text, visual_path, audio_path)
    except Exception as e:
        pytest.fail(f"ScriptElement() raised {e} unexpectedly!")


def test_calculate_duration():
    script_element = ScriptElement("", video_file, audio_file)
    assert script_element.calculate_duration() == max(
        script_element.visual_duration, script_element.audio_duration)


def test_visual_duration():
    script_element = ScriptElement("", video_file, audio_file)
    assert script_element.visual_duration >= 16 and script_element.visual_duration <= 18


def test_audio_duration():
    script_element = ScriptElement("", video_file, audio_file)
    assert script_element.audio_duration >= 208 and script_element.audio_duration <= 210


def test_audio_duration_image():
    script_element = ScriptElement("", image_file, audio_file)
    assert script_element.audio_duration >= 208 and script_element.audio_duration <= 210


def test_is_video():
    script_element = ScriptElement("", video_file, audio_file)
    assert script_element.is_video


def test_is_video_image():
    script_element = ScriptElement("", image_file, audio_file)
    assert not script_element.is_video


def test_invalid_audio_file_type():
    with pytest.raises(ValueError):
        ScriptElement("", image_file, video_file)


def test_invalid_visual_file_type():
    with pytest.raises(ValueError):
        ScriptElement("", audio_file, audio_file)


def test_invalid_text_data_type():
    with pytest.raises(TypeError):
        ScriptElement(1, image_file, audio_file)


def test_invalid_id_data_type():
    with pytest.raises(TypeError):
        ScriptElement("valid", image_file, audio_file, id="string")
